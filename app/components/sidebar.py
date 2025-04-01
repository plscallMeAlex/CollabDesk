import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import ttk
import requests
from PIL import Image
import os


class ServerActionDialog(ctk.CTkToplevel):
    def __init__(self, parent, configuration, action_type="create"):
        super().__init__(parent)
        self.parent = parent
        self.action_type = action_type
        # add configuration
        self.__configuration = configuration

        self.title("Server Action")
        self.geometry("480x400")
        self.resizable(False, False)

        self.center_window()

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Server Action",
            font=("Inter", 24, "bold"),
            text_color="black",
        )
        self.title_label.pack(pady=(20, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Would you like to create a server or join an existing one?",
            font=("Inter", 14),
            text_color="#B5BAC1",
        )
        self.subtitle_label.pack(pady=(0, 20))

        self.create_button = ctk.CTkButton(
            self.main_frame,
            text="Create a Server",
            font=("Inter", 16),
            text_color="black",
            height=70,
            fg_color="transparent",
            hover_color="#404249",
            command=self.on_create_server,
            border_width=2,  # Add border width
            border_color="black",  # Set the border color
        )
        self.create_button.pack(fill="x", padx=20, pady=5)

        self.join_button = ctk.CTkButton(
            self.main_frame,
            text="Join a Server",
            text_color="black",
            font=("Inter", 16),
            height=70,
            fg_color="transparent",
            hover_color="#404249",
            command=self.on_join_server,
            border_width=2,  # Add border width
            border_color="black",  # Set the border color
        )
        self.join_button.pack(fill="x", padx=20, pady=5)

        # self.skip_button = ctk.CTkButton(
        #     self.main_frame,
        #     text="Not sure? You can skip this question for now.",
        #     font=("Inter", 12),
        #     fg_color="transparent",
        #     hover_color="#404249",
        #     text_color="#00A8FC",
        #     command=self.on_skip
        # )
        # self.skip_button.pack(pady=20)

        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="Close",
            font=("Inter", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.destroy,
        )
        self.back_button.pack(side="bottom", pady=20)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def on_create_server(self):
        self.destroy()
        ServerNameDialog(self.parent, self.__configuration, "create")

    def on_join_server(self):
        self.destroy()
        ServerNameDialog(self.parent, self.__configuration, "join")

    def on_skip(self):
        self.destroy()
        ServerNameDialog(self.parent, self.__configuration, "skipped")


class ServerNameDialog(ctk.CTkToplevel):
    def __init__(self, parent, configuration, action_type):
        super().__init__(parent)
        self.parent = parent
        self.action_type = action_type
        self.__configuration = configuration

        # Configure dialog window
        self.title("Create or Join Server")
        self.geometry("480x400")
        self.resizable(False, False)
        self.center_window()

        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Create or Join a Server",
            font=("Inter", 24, "bold"),
            text_color="#000000",
        )
        self.title_label.pack(pady=(20, 10))

        # Server name label
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="SERVER NAME",
            font=("Inter", 12),
            text_color="#B5BAC1",
        )
        self.name_label.pack(pady=(20, 5), padx=20, anchor="w")

        # Server name entry (for creating a server)
        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Inter", 14),
            fg_color="transparent",
            border_color="#1E1F22",
            text_color="black",
            placeholder_text="Enter server name",
        )

        # Invitation link entry (for joining a server)
        self.link_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Inter", 14),
            fg_color="transparent",
            border_color="#1E1F22",
            text_color="black",
            placeholder_text="Enter invitation link",
        )

        # Display the correct entry field based on the action type
        if self.action_type == "join":
            self.name_entry.pack_forget()  # Hide the server name entry
            self.link_entry.pack(fill="x", padx=20)
        else:
            self.name_entry.pack(fill="x", padx=20)
            self.link_entry.pack_forget()  # Hide the invitation link entry

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="Back",
            font=("Inter", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.on_back,
        )
        self.back_button.pack(side="left")

        self.create_button = ctk.CTkButton(
            self.button_frame,
            text="Create" if self.action_type == "create" else "Join",
            font=("Inter", 14),
            fg_color="#5865F2",
            hover_color="#4752C4",
            command=self.on_create_or_join,
        )
        self.create_button.pack(side="right")

    def center_window(self):
        """Center the dialog on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def on_back(self):
        self.destroy()
        ServerActionDialog(self.parent, self.__configuration)

    def on_create_or_join(self):
        server_name = self.name_entry.get() if self.action_type == "create" else None
        invite_link = self.link_entry.get() if self.action_type == "join" else None
        user_id = self.__configuration.load_user_data()
        server_id = None

        if self.action_type == "create" and server_name:
            print(f"Creating server: {server_name}")
            # Request to create the server
            response = requests.post(
                self.__configuration.api_url + "/guilds/create_guild/",
                json={
                    "name": server_name,
                    "user_id": user_id,
                },
            )
            if response.status_code == 201:
                server_id = response.json()["id"]
                print("Server created successfully")
            else:
                print("Failed to create server")

            # Here you could add further actions to create the guild
        elif self.action_type == "join" and invite_link:
            if invite_link.startswith(self.__configuration.join_url):
                # extract guild ID from the invite link after the join URL
                invite_token = invite_link.split("/")[-1]
                # Request to join the server
                params = {
                    "invitetoken": invite_token,
                    "user_id": user_id,
                }
                response = requests.post(
                    self.__configuration.api_url + "/guilds/join_guild/", params=params
                )
                if response.status_code == 200:
                    box = CTkMessagebox(
                        self, title="Success", message="Joined server successfully"
                    )
                    # wait until the user closes the message box
                    box.wait_window()
            else:
                box = CTkMessagebox(
                    self, title="Error", message="Invalid invite link", icon="warning"
                )
                # wait until the user closes the message box
                box.wait_window()
                return

            print(f"Joining server with invite link: {invite_link}")
            # Here you could add further actions to join the server

        if hasattr(self.parent, "add_server_icon"):
            self.parent.add_server_icon(
                server_name if server_name else invite_link, server_id
            )
        self.destroy()


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, configuration, change_guild_callback, **kwargs):
        # Remove width from kwargs if it exists to avoid conflict
        kwargs.pop("width", None)
        super().__init__(master, **kwargs)
        self.__configuration = configuration
        self.__change_guild_callback = change_guild_callback

        bg_color = (
            self.__configuration.colors["frame-color-secondary"]
            if self.__configuration
            else "#D9D9D9"
        )

        # Set width and configure grid
        self.configure(fg_color=bg_color, width=72)
        self.grid_propagate(False)  # Prevent frame from resizing to fit contents
        self.grid_rowconfigure(
            1, weight=1
        )  # Make the sidebar component expand vertically
        self.grid_columnconfigure(0, weight=1)  # Center contents horizontally

        # Adjust logo size
        logo_path = os.path.join("app", "assets", "logo.png")
        if os.path.exists(logo_path):
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path), size=(60, 60)
            )
            self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
            self.logo_label.pack(pady=5)
            # self.logo_label.grid(row=0, column=0, pady=5)
            self.logo_label.bind("<Button-1>", lambda event: print("Logo clicked"))

        # line separator
        style = ttk.Style()
        style.configure("Black.TSeparator", background="black")

        self.line_separator = ttk.Separator(
            self, orient="horizontal", style="Black.TSeparator"
        )
        self.line_separator.pack(
            fill="x",
            padx=5,
        )

        self.sidebar_component = SidebarComponent(
            self, self.__configuration, self.__change_guild_callback
        )
        self.sidebar_component.pack(pady=10)
        # self.sidebar_component.grid(
        #     row=1, column=0, sticky="nsew"
        # )  # Make it fill the space


class SidebarComponent(ctk.CTkFrame):
    def __init__(self, master, configuration, change_guild_callback, **kwargs):
        # Remove width from kwargs if it exists
        kwargs.pop("width", None)
        super().__init__(master, **kwargs)

        self.__configuration = configuration
        self.__change_guild_callback = change_guild_callback
        bg_color = (
            self.__configuration.colors["frame-color-secondary"]
            if self.__configuration
            else "#D9D9D9"
        )

        # Configure frame
        self.configure(fg_color=bg_color, width=65)
        self.grid_propagate(False)  # Prevent frame from resizing
        self.grid_columnconfigure(0, weight=1)  # Center contents horizontally

        # Create a canvas for scrolling
        self.canvas = ctk.CTkCanvas(self, bg=bg_color, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create a frame inside canvas to hold the icons
        self.icons_frame = ctk.CTkFrame(self.canvas, fg_color=bg_color)
        self.canvas.create_window((0, 0), window=self.icons_frame, anchor="nw")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.load_images()

        # Add plus button at the top
        self.plus_label = ctk.CTkLabel(
            self.icons_frame, image=self.normal_image, text="", fg_color=bg_color
        )
        self.plus_label.pack(pady=5, padx=5)

        self.plus_label.bind("<Button-1>", lambda event: self.on_button_click())
        self.plus_label.bind("<Enter>", self.on_hover_enter)
        self.plus_label.bind("<Leave>", self.on_hover_leave)

        self.created_links = []
        self.load_server()

        # Bind mouse wheel to scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Bind frame configure to update scroll region
        self.icons_frame.bind("<Configure>", self._configure_scroll_region)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.canvas.winfo_height() < self.icons_frame.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_scroll_region(self, event):
        """Update the scroll region when the frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_images(self):
        """Load all required images for the sidebar"""
        assets_path = os.path.join("app", "assets")

        plus_path = os.path.join(assets_path, "plus.png")
        plus_hover_path = os.path.join(assets_path, "plus_hover.png")
        group_path = os.path.join(assets_path, "Group.png")
        group_hover_path = os.path.join(assets_path, "Group_hover.png")

        # Adjust image sizes
        if os.path.exists(plus_path):
            self.normal_image = ctk.CTkImage(
                light_image=Image.open(plus_path), size=(48, 48)
            )
        if os.path.exists(plus_hover_path):
            self.hover_image = ctk.CTkImage(
                light_image=Image.open(plus_hover_path), size=(48, 48)
            )
        if os.path.exists(group_path):
            self.group_image = ctk.CTkImage(
                light_image=Image.open(group_path), size=(48, 48)
            )
        if os.path.exists(group_hover_path):
            self.group_hover_image = ctk.CTkImage(
                light_image=Image.open(group_hover_path), size=(48, 48)
            )

    def on_button_click(self):
        """Handle plus button click"""
        dialog = ServerActionDialog(self, self.__configuration)
        dialog.grab_set()

    def on_hover_enter_guild(self, cmp, event):
        cmp.configure(image=self.group_hover_image)

    def on_hover_leave_guild(self, cmp, event):
        cmp.configure(image=self.group_image)

    def on_hover_enter(self, event):
        self.plus_label.configure(image=self.hover_image)

    def on_hover_leave(self, event):
        self.plus_label.configure(image=self.normal_image)

    def add_server_icon(self, server_name, id=None):
        """Add a new server icon to the sidebar"""
        first_char = server_name[0].upper()
        if len(self.created_links) > 0:
            self.plus_label.pack_forget()
        new_link = ctk.CTkLabel(
            self.icons_frame,
            image=self.group_image,
            text=str(first_char),  # Remove text to keep width consistent
            fg_color=self.cget("fg_color"),
        )
        new_link.pack(pady=5, padx=5)
        self.created_links.append(new_link)

        # Bind the label with the server
        new_link.bind(
            "<Button-1>",
            lambda event, id=id: self.guild_clicked(id, event),
        )
        new_link.bind(
            "<Enter>", lambda event, cmp=new_link: self.on_hover_enter_guild(cmp, event)
        )
        new_link.bind(
            "<Leave>", lambda event, cmp=new_link: self.on_hover_leave_guild(cmp, event)
        )

        # Move plus button to the end
        self.plus_label.pack_forget()
        self.plus_label.pack(pady=5, padx=5)

    def guild_clicked(self, id, event):
        self.__change_guild_callback(id)

    def load_server(self):
        # fetch to the server to get the server
        params = {"user_id": self.__configuration.load_user_data()}
        response = requests.get(
            self.__configuration.api_url + "/guilds/get_guilds_by_user/",
            params=params,
        )

        if response.status_code == 200:
            guilds = response.json()
            for guild in guilds:
                self.add_server_icon(guild["name"], guild["id"])
        else:
            print("Failed to fetch the guilds")
