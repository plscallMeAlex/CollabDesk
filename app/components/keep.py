import customtkinter as ctk
from PIL import Image
import os

class ServerCreationDialog(ctk.CTkToplevel):
    def __init__(self, parent, server_action="create"):
        super().__init__(parent)
        self.parent = parent
        self.server_action = server_action
        
        self.title("Tell Us More About Your Server")
        self.geometry("480x400")
        self.resizable(False, False)
        
        self.center_window()
        
        self.main_frame = ctk.CTkFrame(self, fg_color="#313338")
        self.main_frame.pack(fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Tell Us More About Your Server",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="In order to help you with your setup, is your new server for\njust a few friends or a larger community?",
            font=("Arial", 14),
            text_color="#B5BAC1"
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        self.community_button = ctk.CTkButton(
            self.main_frame,
            text="For a club or community",
            font=("Arial", 16),
            height=70,
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.on_community_select
        )
        self.community_button.pack(fill="x", padx=20, pady=5)
        
        self.friends_button = ctk.CTkButton(
            self.main_frame,
            text="Join current had server",
            font=("Arial", 16),
            height=70,
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.on_friends_select
        )
        self.friends_button.pack(fill="x", padx=20, pady=5)
        
        self.skip_button = ctk.CTkButton(
            self.main_frame,
            text="Not sure? You can skip this question for now.",
            font=("Arial", 12),
            fg_color="transparent",  
            hover_color="#404249",  
            text_color="#00A8FC",
            command=self.on_skip
        )
        self.skip_button.pack(pady=20)
        
        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="Back",
            font=("Arial", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.destroy
        )
        self.back_button.pack(side="bottom", pady=20)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def on_community_select(self):
        self.destroy()
        ServerNameDialog(self.parent, "community")

    def on_friends_select(self):
        self.destroy()
        ServerNameDialog(self.parent, "friends")

    def on_skip(self):
        self.destroy()
        ServerNameDialog(self.parent, "skipped")


class ServerNameDialog(ctk.CTkToplevel):
    def __init__(self, parent, server_type):
        super().__init__(parent)
        self.parent = parent
        self.server_type = server_type
        
        # Configure dialog window
        self.title("Create or Join Server")
        self.geometry("480x400")
        self.resizable(False, False)
        self.center_window()
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#313338")
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Join a server",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Server name label
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="SERVER NAME",
            font=("Arial", 12),
            text_color="#B5BAC1"
        )
        self.name_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Server name entry
        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 14),
            fg_color="#1E1F22",
            border_color="#1E1F22",
            text_color="white",
            placeholder_text="Enter server name"
        
        )
        self.link_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 14),
            fg_color="#1E1F22",
            border_color="#1E1F22",
            text_color="white",
            placeholder_text="Enter invitation link"
        )
        self.name_entry.pack(fill="x", padx=20)

        self.button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.button_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="Back",
            font=("Arial", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.on_back
        )
        self.back_button.pack(side="left")
        
        self.create_button = ctk.CTkButton(
            self.button_frame,
            text="Create" if self.server_type == "community" else "Join",
            font=("Arial", 14),
            fg_color="#5865F2",
            hover_color="#4752C4",
            command=self.on_create_or_join
        )
        self.create_button.pack(side="right")

    def center_window(self):
        """Center the dialog on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def on_back(self):
        self.destroy()
        ServerCreationDialog(self.parent)

    def on_create_or_join(self):
        server_name = self.name_entry.get()
        if server_name:
            if self.server_type == "community":
                invite_link = self.link_entry.get()
                print(f"Creating community: {server_name}, Invite Link: {invite_link}")
            else:
                print(f"Joining server: {server_name}")
            if hasattr(self.parent, 'add_server_icon'):
                self.parent.add_server_icon(server_name)
            self.destroy()


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.config = getattr(master, 'config', None)
        
        bg_color = self.config.colors["frame-color-secondary"] if self.config else "#D9D9D9"
        
        self.configure(
            border_width=2,
            border_color="black",
            fg_color=bg_color,
            width=100 
        )

        logo_path = os.path.join("app", "assets", "logo.png")
        if os.path.exists(logo_path):
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                size=(100, 100)
            )
            self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
            self.logo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.sidebar_component = SidebarComponent(self)
        self.sidebar_component.grid(row=1, column=0, pady=0)


class SidebarComponent(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.config = getattr(master, 'config', None)
        bg_color = self.config.colors["frame-color-secondary"] if self.config else "#D9D9D9"
        
        self.configure(fg_color=bg_color)

        self.load_images()
        
        self.plus_label = ctk.CTkLabel(
            self, 
            image=self.normal_image,
            text="",
            fg_color=bg_color
        )
        self.plus_label.grid(row=0, column=0, pady=5)

        self.plus_label.bind("<Button-1>", lambda event: self.on_button_click())
        self.plus_label.bind("<Enter>", self.on_hover_enter)
        self.plus_label.bind("<Leave>", self.on_hover_leave)

        self.created_links = []

    def load_images(self):
        """Load all required images for the sidebar"""
        assets_path = os.path.join("app", "assets")
        
        plus_path = os.path.join(assets_path, "plus.png")
        plus_hover_path = os.path.join(assets_path, "plus_hover.png")
        group_path = os.path.join(assets_path, "Group.png")
        group_hover_path = os.path.join(assets_path, "Group_hover.png")
        
        if os.path.exists(plus_path):
            self.normal_image = ctk.CTkImage(
                light_image=Image.open(plus_path),
                size=(60, 60)
            )
        if os.path.exists(plus_hover_path):
            self.hover_image = ctk.CTkImage(
                light_image=Image.open(plus_hover_path),
                size=(60, 60)
            )
        if os.path.exists(group_path):
            self.group_image = ctk.CTkImage(
                light_image=Image.open(group_path),
                size=(60, 60)
            )
        if os.path.exists(group_hover_path):
            self.group_hover_image = ctk.CTkImage(
                light_image=Image.open(group_hover_path),
                size=(60, 60)
            )

    def on_button_click(self):
        """Handle plus button click"""
        dialog = ServerCreationDialog(self)
        dialog.focus()

    def on_hover_enter(self, event):
        self.plus_label.configure(image=self.hover_image)

    def on_hover_leave(self, event):
        self.plus_label.configure(image=self.normal_image)

    def add_server_icon(self, server_name):
        """Add a new server icon to the sidebar, keeping the '+' button at the bottom."""
        new_link = ctk.CTkLabel(
            self, 
            image=self.group_image, 
            text=server_name,
            fg_color=self.cget("fg_color")
        )
        new_link.grid(row=len(self.created_links), column=0, pady=5, sticky="w")
        self.created_links.append(new_link)
        self.plus_label.grid(row=len(self.created_links), column=0, pady=5)


