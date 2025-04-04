import customtkinter as ctk
import json
import threading
import websocket
import pyaudio
import asyncio
import aiortc.sdp
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
    RTCIceCandidate,
    MediaStreamTrack,
)
from aiortc.contrib.media import MediaStreamTrack, MediaBlackhole, MediaRecorder
from aiortc.mediastreams import AudioStreamTrack
import uuid
import urllib.parse
import queue
import time


class AudioReceiveTrack(MediaStreamTrack):
    """Media track for receiving audio."""

    kind = "audio"

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.sample_rate = 48000
        self.channels = 1
        self.active = True

    def add_frame(self, frame):
        if self.active:
            self.queue.put(frame)


class VoiceChannelUI(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        configuration,
        channel_id,
        channel_name,
        user_id=None,
        username=None,
    ):
        super().__init__(parent)
        self.configuration = configuration
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_id = user_id or f"user_{uuid.uuid4()}"
        self.username = username or f"User_{uuid.uuid4().hex[:6]}"
        self.is_connected = False
        self.is_muted = False

        # Event loop for WebRTC
        self.loop = asyncio.new_event_loop()
        self.thread = None

        # WebSocket and WebRTC setup
        self.ws = None
        self.peer_connections = {}  # Store RTCPeerConnection objects
        self.participants = {}  # Store participant info

        # Audio tracks
        self.local_audio_track = None
        self.remote_audio_tracks = {}

        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.audio_chunk = 1024
        self.sample_rate = 48000
        self.channels = 1

        # Set up UI
        self.setup_ui()

    def setup_ui(self):
        # Channel header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=10, pady=5)

        self.channel_label = ctk.CTkLabel(
            self.header_frame,
            text=f"🔊 {self.channel_name}",
            font=("Inter", 16, "bold"),
        )
        self.channel_label.pack(side="left", padx=10)

        # Controls
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(fill="x", padx=10, pady=5)

        self.join_button = ctk.CTkButton(
            self.controls_frame, text="Join Voice", command=self.toggle_connection
        )
        self.join_button.pack(side="left", padx=5)

        self.mute_button = ctk.CTkButton(
            self.controls_frame,
            text="🎤",
            width=40,
            command=self.toggle_mute,
            state="disabled",
        )
        self.mute_button.pack(side="left", padx=5)

        # Connection status
        self.status_label = ctk.CTkLabel(
            self.controls_frame,
            text="Disconnected",
            text_color="gray",
        )
        self.status_label.pack(side="right", padx=10)

        # Participants list
        self.participants_frame = ctk.CTkFrame(self)
        self.participants_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.participants_label = ctk.CTkLabel(
            self.participants_frame, text="Participants", font=("Inter", 14, "bold")
        )
        self.participants_label.pack(anchor="w", padx=10, pady=5)

        # This would be populated with connected users
        self.participants_list = ctk.CTkFrame(self.participants_frame)
        self.participants_list.pack(fill="both", expand=True)

    def toggle_connection(self):
        if not self.is_connected:
            self.join_voice_channel()
        else:
            self.leave_voice_channel()

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        # Update UI
        self.mute_button.configure(text="🔇" if self.is_muted else "🎤")

        # Mute/unmute audio track
        if self.input_stream:
            if self.is_muted:
                self.input_stream.stop_stream()
            else:
                self.input_stream.start_stream()

    def join_voice_channel(self):
        """Connect to WebSocket and establish WebRTC connections"""
        print(f"Joining voice channel: {self.channel_name}")

        # Start WebRTC thread if not already running
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run_event_loop)
            self.thread.daemon = True
            self.thread.start()

        # Start websocket connection with query params for identification
        query_params = urllib.parse.urlencode(
            {"user_id": self.user_id, "username": self.username}
        )
        websocket_url = (
            f"ws://localhost:8000/ws/voice/{self.channel_id}/?{query_params}"
        )

        self.start_websocket_connection(websocket_url)

        # Update UI
        self.status_label.configure(text="Connecting...", text_color="orange")

    def leave_voice_channel(self):
        """Disconnect from WebSocket and close WebRTC connections"""
        print(f"Leaving voice channel: {self.channel_name}")

        # Close all peer connections
        async def close_connections():
            for peer_id, pc in self.peer_connections.items():
                await pc.close()
            self.peer_connections = {}

        future = asyncio.run_coroutine_threadsafe(close_connections(), self.loop)
        future.result(timeout=5)  # Wait for connections to close

        # Close websocket
        if self.ws:
            self.ws.close()
            self.ws = None

        # Stop audio streams
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
            self.input_stream = None

        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
            self.output_stream = None

        self.is_connected = False
        self.join_button.configure(text="Join Voice")
        self.mute_button.configure(state="disabled")
        self.status_label.configure(text="Disconnected", text_color="gray")

        # Clear participants list
        for widget in self.participants_list.winfo_children():
            widget.destroy()
        self.participants = {}

    def add_participant(self, username, is_self=False, user_id=None):
        """Add a participant to the UI"""
        participant_frame = ctk.CTkFrame(self.participants_list)
        participant_frame.pack(fill="x", padx=5, pady=2)

        status_indicator = ctk.CTkLabel(participant_frame, text="🟢", width=20)
        status_indicator.pack(side="left")

        name_label = ctk.CTkLabel(
            participant_frame,
            text=f"{username} {'(You)' if is_self else ''}",
        )
        name_label.pack(side="left", padx=5)

        # Store participant info
        if user_id:
            self.participants[user_id] = {
                "username": username,
                "frame": participant_frame,
                "status": status_indicator,
            }

        return participant_frame

    def remove_participant(self, user_id):
        """Remove a participant from the UI"""
        if user_id in self.participants:
            self.participants[user_id]["frame"].destroy()
            del self.participants[user_id]

    # WebSocket Connection
    def start_websocket_connection(self, url):
        """Start WebSocket connection in a separate thread"""

        def on_message(ws, message):
            """Handle incoming WebSocket messages"""
            try:
                print(f"Received message: {message}")
                data = json.loads(message)
                message_type = data.get("type")

                if message_type == "user_join":
                    user_id = data.get("user_id")
                    username = data.get("username")
                    print(f"User joined: {username} ({user_id})")

                    # Don't add yourself again
                    if user_id and user_id != self.user_id:
                        # Add to UI from the main thread
                        self.after(
                            0,
                            lambda: self.add_participant(
                                username, is_self=False, user_id=user_id
                            ),
                        )
                        # Create new peer connection for this user
                        asyncio.run_coroutine_threadsafe(
                            self.create_peer_connection(user_id), self.loop
                        )
                    elif user_id == self.user_id and not self.is_connected:
                        # This is confirmation we've connected
                        self.after(0, self.connection_confirmed)

                elif message_type == "user_leave":
                    user_id = data.get("user_id")
                    print(f"User left: {user_id}")
                    if user_id in self.peer_connections:
                        asyncio.run_coroutine_threadsafe(
                            self.peer_connections[user_id].close(), self.loop
                        )
                        del self.peer_connections[user_id]
                    self.after(0, lambda: self.remove_participant(user_id))

                elif message_type == "webrtc_offer":
                    sender_id = data.get("sender_id")
                    if sender_id not in self.peer_connections:
                        asyncio.run_coroutine_threadsafe(
                            self.create_peer_connection(sender_id), self.loop
                        )

                    # Set remote description and create answer
                    asyncio.run_coroutine_threadsafe(
                        self.handle_offer(sender_id, data.get("offer")), self.loop
                    )

                elif message_type == "webrtc_answer":
                    sender_id = data.get("sender_id")
                    if sender_id in self.peer_connections:
                        asyncio.run_coroutine_threadsafe(
                            self.handle_answer(sender_id, data.get("answer")), self.loop
                        )

                elif message_type == "ice_candidate":
                    sender_id = data.get("sender_id")
                    if sender_id in self.peer_connections:
                        asyncio.run_coroutine_threadsafe(
                            self.handle_ice_candidate(sender_id, data.get("candidate")),
                            self.loop,
                        )

            except json.JSONDecodeError:
                print(f"Invalid JSON received: {message}")
            except Exception as e:
                print(f"Error processing message: {e}")

        def on_error(ws, error):
            print(f"WebSocket error: {error}")
            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Connection Error", text_color="red"
                ),
            )

        def on_close(ws, close_status_code, close_msg):
            print(f"WebSocket closed: {close_status_code} - {close_msg}")
            if self.is_connected:
                self.after(0, self.leave_voice_channel)

        def on_open(ws):
            print("WebSocket connection established")

        # Close any existing connection
        if self.ws:
            self.ws.close()

        # Create new connection
        self.ws = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )

        # Start WebSocket in a thread
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def connection_confirmed(self):
        """Update UI when connection is confirmed"""
        self.is_connected = True
        self.join_button.configure(text="Leave Voice")
        self.mute_button.configure(state="normal")
        self.status_label.configure(text="Connected", text_color="green")

        # Add yourself to participants list
        self.add_participant(self.username, is_self=True, user_id=self.user_id)

        # Set up audio
        try:
            self.setup_audio_input()  # Set up local audio
            self.setup_audio_output()  # Set up output
        except Exception as e:
            print(f"Audio setup error: {e}")

    def _run_event_loop(self):
        """Run the asyncio event loop in a separate thread"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    # WebRTC Connection Handling
    async def create_peer_connection(self, peer_id):
        """Create a new WebRTC peer connection"""
        try:
            # Create and configure the peer connection
            pc = RTCPeerConnection(configuration=self.configuration)
            self.peer_connections[peer_id] = pc

            # Set up ice candidate handling
            @pc.on("icecandidate")
            def on_ice_candidate(candidate):
                if candidate and self.ws and self.ws.sock and self.ws.sock.connected:
                    self.send_ice_candidate(peer_id, candidate)

            # Set up track handling
            @pc.on("track")
            def on_track(track):
                if track.kind == "audio":
                    print(f"Received audio track from {peer_id}")
                    self.remote_audio_tracks[peer_id] = track

            # Add local audio track if we have it
            if self.local_audio_track:
                pc.addTrack(self.local_audio_track)

            # If we're initiating the connection, create and send offer
            if self.user_id < peer_id:  # Simple way to decide who initiates
                await self.create_and_send_offer(peer_id)

            return pc

        except Exception as e:
            print(f"Error creating peer connection: {e}")
            return None

    async def create_and_send_offer(self, peer_id):
        """Create and send WebRTC offer"""
        pc = self.peer_connections.get(peer_id)
        if not pc:
            return

        try:
            # Create offer
            offer = await pc.createOffer()
            await pc.setLocalDescription(offer)

            # Wait for ICE gathering to complete
            await self.gather_candidates(pc)

            # Send the offer
            if self.ws and self.ws.sock and self.ws.sock.connected:
                message = {
                    "type": "offer",
                    "sdp": pc.localDescription.sdp,
                    "sender_id": self.user_id,
                    "target_id": peer_id,
                }
                self.ws.send(json.dumps(message))
                print(f"Sent offer to {peer_id}")
        except Exception as e:
            print(f"Error creating offer: {e}")

    async def handle_offer(self, peer_id, offer_sdp):
        """Handle incoming WebRTC offer"""
        pc = self.peer_connections.get(peer_id)
        if not pc:
            pc = await self.create_peer_connection(peer_id)
            if not pc:
                return

        try:
            # Set remote description
            offer = RTCSessionDescription(sdp=offer_sdp, type="offer")
            await pc.setRemoteDescription(offer)

            # Create answer
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)

            # Wait for ICE gathering to complete
            await self.gather_candidates(pc)

            # Send the answer
            if self.ws and self.ws.sock and self.ws.sock.connected:
                message = {
                    "type": "answer",
                    "answer": pc.localDescription.sdp,
                    "sender_id": self.user_id,
                    "target_id": peer_id,
                }
                self.ws.send(json.dumps(message))
                print(f"Sent answer to {peer_id}")
        except Exception as e:
            print(f"Error handling offer: {e}")

    async def handle_answer(self, peer_id, answer_sdp):
        """Handle incoming WebRTC answer"""
        pc = self.peer_connections.get(peer_id)
        if not pc:
            return

        try:
            answer = RTCSessionDescription(sdp=answer_sdp, type="answer")
            await pc.setRemoteDescription(answer)
            print(f"Set remote description from {peer_id}")
        except Exception as e:
            print(f"Error handling answer: {e}")

    async def handle_ice_candidate(self, peer_id, candidate_dict):
        """Handle incoming ICE candidate"""
        pc = self.peer_connections.get(peer_id)
        if not pc:
            return

        try:
            candidate = RTCIceCandidate(
                component=candidate_dict["component"],
                foundation=candidate_dict["foundation"],
                ip=candidate_dict["ip"],
                port=candidate_dict["port"],
                priority=candidate_dict["priority"],
                protocol=candidate_dict["protocol"],
                type=candidate_dict["type"],
                sdpMLineIndex=candidate_dict["sdpMLineIndex"],
                sdpMid=candidate_dict["sdpMid"],
            )
            await pc.addIceCandidate(candidate)
            print(f"Added ICE candidate from {peer_id}")
        except Exception as e:
            print(f"Error handling ICE candidate: {e}")

    def send_ice_candidate(self, peer_id, candidate):
        """Send ICE candidate to peer"""
        if not self.ws or not self.ws.sock or not self.ws.sock.connected:
            return

        try:
            message = {
                "type": "ice_candidate",
                "candidate": {
                    "candidate": candidate.candidate,
                    "sdpMid": candidate.sdpMid,
                    "sdpMLineIndex": candidate.sdpMLineIndex,
                    "component": candidate.component,
                    "foundation": candidate.foundation,
                    "ip": candidate.ip,
                    "port": candidate.port,
                    "priority": candidate.priority,
                    "protocol": candidate.protocol,
                    "type": candidate.type,
                },
                "sender_id": self.user_id,
                "target_id": peer_id,
            }
            self.ws.send(json.dumps(message))
            print(f"Sent ICE candidate to {peer_id}")
        except Exception as e:
            print(f"Error sending ICE candidate: {e}")

    async def gather_candidates(self, pc):
        """Wait for ICE gathering to complete."""
        # In a real implementation, this would use proper signaling
        # This is a simplified version
        waiter = asyncio.Future()

        @pc.on("icegatheringstatechange")
        def state_change():
            if pc.iceGatheringState == "complete":
                waiter.set_result(None)

        # Set a timeout for ICE gathering
        try:
            await asyncio.wait_for(waiter, timeout=5.0)
        except asyncio.TimeoutError:
            # Continue even if gathering isn't complete
            pass

        return

    # Audio Handling
    def setup_audio_input(self):
        """Set up audio input stream"""
        try:
            # Create a custom AudioStreamTrack
            class LocalAudioTrack(AudioStreamTrack):
                def __init__(self, audio_instance, sample_rate, channels):
                    super().__init__()
                    self.audio = audio_instance
                    self.sample_rate = sample_rate
                    self.channels = channels
                    self.pts = 0
                    self.sample_rate = sample_rate
                    self.active = True
                    self._queue = queue.Queue()
                    self._start_recording()

                def _audio_callback(self, in_data, frame_count, time_info, status):
                    self._queue.put(in_data)
                    return (None, pyaudio.paContinue)

                def _start_recording(self):
                    self.stream = self.audio.open(
                        format=pyaudio.paInt16,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=1024,
                        stream_callback=self._audio_callback,
                    )
                    self.stream.start_stream()

            # Create and store the local audio track
            self.local_audio_track = LocalAudioTrack(
                self.audio, self.sample_rate, self.channels
            )
            self.input_stream = self.local_audio_track.stream

            # Add the track to existing peer connections
            for peer_id, pc in self.peer_connections.items():
                asyncio.run_coroutine_threadsafe(
                    self._add_track_to_peer(pc, self.local_audio_track), self.loop
                )

        except Exception as e:
            print(f"Audio input setup error: {e}")
            raise

    async def _add_track_to_peer(self, pc, track):
        """Add track to peer connection"""
        pc.addTrack(track)

    def setup_audio_output(self):
        """Set up audio output for received tracks"""
        try:
            # Create output stream
            self.output_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.audio_chunk,
            )

            # Start a thread to mix and play audio from remote tracks
            threading.Thread(target=self._audio_mixer_thread, daemon=True).start()

        except Exception as e:
            print(f"Audio output setup error: {e}")
            raise

    def _audio_mixer_thread(self):
        """Thread to mix and play audio from all remote tracks"""
        while self.is_connected:
            try:
                # Simple mixer - just take audio from each remote track
                # In a real implementation, you'd properly mix audio samples
                for track_id, track in self.remote_audio_tracks.items():
                    # Get audio data from the track if available
                    # This is simplified - in reality you'd need to implement
                    # proper audio frame mixing
                    pass

                # Short sleep to prevent CPU hogging
                time.sleep(0.01)
            except Exception as e:
                print(f"Audio mixer error: {e}")
