import asyncio
import websockets
import json
import tkinter as tk
import customtkinter as ctk
from threading import Thread

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")
        
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20)

        self.chat_display = ctk.CTkTextbox(self.frame, width=300, height=200)
        self.chat_display.pack()

        self.message_entry = ctk.CTkEntry(self.frame, width=250)
        self.message_entry.pack(pady=10)

        self.send_button = ctk.CTkButton(self.frame, text="Send", command=self.send_message)
        self.send_button.pack()

        self.websocket = None
        self.room_name = "room123"  # Change this as needed
        self.ws_url = f"ws://127.0.0.1:8000/ws/chat/{self.room_name}/"

        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_ws())

    async def connect_ws(self):
        async with websockets.connect(self.ws_url) as ws:
            self.websocket = ws
            async for message in ws:
                data = json.loads(message)
                self.chat_display.insert(tk.END, f"{data['message']}\n")

    def send_message(self):
        if self.websocket:
            message = self.message_entry.get()
            self.loop.create_task(self.websocket.send(json.dumps({"message": message})))
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatApp(root)
    root.mainloop()
