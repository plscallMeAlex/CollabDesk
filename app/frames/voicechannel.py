import customtkinter as ctk
import json
import threading
import websocket
import pyaudio
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.contrib.media import MediaStreamTrack, MediaBlackhole, MediaRecorder
import uuid
import urllib.parse


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

        # WebSocket and WebRTC setup
        self.ws = None
        self.peer_connections = {}  # Store RTCPeerConnection objects
        self.participants = {}  # Store participant info

        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None

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

        # Mute/unmute audio track if available
        if self.input_stream:
            if self.is_muted:
                self.input_stream.stop_stream()
            else:
                self.input_stream.start_stream()

    def join_voice_channel(self):
        """Connect to WebSocket and establish WebRTC connections"""
        print(f"Joining voice channel: {self.channel_name}")

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
        for peer_id, pc in self.peer_connections.items():
            pc.close()
        self.peer_connections = {}

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
                        self.create_peer_connection(user_id)
                    elif user_id == self.user_id and not self.is_connected:
                        # This is confirmation we've connected
                        self.after(0, self.connection_confirmed)

                elif message_type == "user_leave":
                    user_id = data.get("user_id")
                    print(f"User left: {user_id}")
                    if user_id in self.peer_connections:
                        self.peer_connections[user_id].close()
                        del self.peer_connections[user_id]
                    self.after(0, lambda: self.remove_participant(user_id))

                elif message_type == "webrtc_offer":
                    sender_id = data.get("sender_id")
                    if sender_id not in self.peer_connections:
                        self.create_peer_connection(sender_id)

                    # Set remote description and create answer
                    self.handle_offer(sender_id, data.get("offer"))

                elif message_type == "webrtc_answer":
                    sender_id = data.get("sender_id")
                    if sender_id in self.peer_connections:
                        self.handle_answer(sender_id, data.get("answer"))

                elif message_type == "ice_candidate":
                    sender_id = data.get("sender_id")
                    if sender_id in self.peer_connections:
                        self.handle_ice_candidate(sender_id, data.get("candidate"))

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
            self.setup_audio_input(None)  # Set up local audio
        except Exception as e:
            print(f"Audio setup error: {e}")

    # WebRTC Connection Handling
    def create_peer_connection(self, peer_id):
        """Create a new WebRTC peer connection"""
        try:
            pc = RTCPeerConnection()
            self.peer_connections[peer_id] = pc

            @pc.on("icecandidate")
            def on_ice_candidate(candidate):
                if candidate and self.ws and self.ws.sock and self.ws.sock.connected:
                    self.send_ice_candidate(peer_id, candidate)

            @pc.on("track")
            def on_track(track):
                if track.kind == "audio":
                    # Handle incoming audio stream
                    self.setup_audio_output(track)

            # Setup and add local audio track if we have it
            if self.input_stream:
                # In a real implementation, this would add the audio track to the connection
                pass

            # If we're initiating the connection, create and send offer
            if self.user_id < peer_id:  # Simple way to decide who initiates
                self.create_and_send_offer(peer_id)

            return pc

        except Exception as e:
            print(f"Error creating peer connection: {e}")
            return None

    def create_and_send_offer(self, peer_id):
        """Create and send WebRTC offer"""
        # This is a placeholder - in a real app, you'd use asyncio correctly here
        print(f"Creating offer for peer {peer_id}")
        # Simplified for this example

    def handle_offer(self, peer_id, offer_sdp):
        """Handle incoming WebRTC offer"""
        print(f"Received offer from {peer_id}")
        # Simplified for this example

    def handle_answer(self, peer_id, answer_sdp):
        """Handle incoming WebRTC answer"""
        print(f"Received answer from {peer_id}")
        # Simplified for this example

    def handle_ice_candidate(self, peer_id, candidate_dict):
        """Handle incoming ICE candidate"""
        print(f"Received ICE candidate from {peer_id}")
        # Simplified for this example

    def send_ice_candidate(self, peer_id, candidate):
        """Send ICE candidate to peer"""
        print(f"Sending ICE candidate to {peer_id}")
        # Simplified for this example

    # Audio Handling - simplified for this example
    def setup_audio_input(self, peer_connection):
        """Set up audio input stream"""
        try:
            # Simplified audio setup for demonstration
            print("Setting up audio input")
            # In a real implementation, this would properly set up the audio devices
        except Exception as e:
            print(f"Audio input setup error: {e}")

    def setup_audio_output(self, track):
        """Set up audio output for received track"""
        try:
            # Simplified audio output setup for demonstration
            print("Setting up audio output for received track")
            # In a real implementation, this would connect the track to audio output
        except Exception as e:
            print(f"Audio output setup error: {e}")
