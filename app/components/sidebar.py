import customtkinter as ctk
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
            font=("Arial", 24, "bold"),
            text_color="black",
        )
        self.title_label.pack(pady=(20, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Would you like to create a server or join an existing one?",
            font=("Arial", 14),
            text_color="#B5BAC1",
        )
        self.subtitle_label.pack(pady=(0, 20))

        self.create_button = ctk.CTkButton(
            self.main_frame,
            text="Create a Server",
            font=("Arial", 16),
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
            font=("Arial", 16),
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
        #     font=("Arial", 12),
        #     fg_color="transparent",
        #     hover_color="#404249",
        #     text_color="#00A8FC",
        #     command=self.on_skip
        # )
        # self.skip_button.pack(pady=20)

        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="Close",
            font=("Arial", 14),
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
            font=("Arial", 24, "bold"),
            text_color="#000000",
        )
        self.title_label.pack(pady=(20, 10))

        # Server name label
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="SERVER NAME",
            font=("Arial", 12),
            text_color="#B5BAC1",
        )
        self.name_label.pack(pady=(20, 5), padx=20, anchor="w")

        # Server name entry (for creating a server)
        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 14),
            fg_color="transparent",
            border_color="#1E1F22",
            text_color="black",
            placeholder_text="Enter server name",
        )

        # Invitation link entry (for joining a server)
        self.link_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 14),
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
            font=("Arial", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.on_back,
        )
        self.back_button.pack(side="left")

        self.create_button = ctk.CTkButton(
            self.button_frame,
            text="Create" if self.action_type == "create" else "Join",
            font=("Arial", 14),
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

        if self.action_type == "create" and server_name:
            print(f"Creating server: {server_name}")
            # Here you could add further actions to create the server
        elif self.action_type == "join" and invite_link:
            print(f"Joining server with invite link: {invite_link}")
            # Here you could add further actions to join the server

        if hasattr(self.parent, "add_server_icon"):
            self.parent.add_server_icon(server_name if server_name else invite_link)
        self.destroy()


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, configuration, **kwargs):
        # Remove width from kwargs if it exists to avoid conflict
        kwargs.pop("width", None)
        super().__init__(master, **kwargs)
        self.__configuration = configuration

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

        self.sidebar_component = SidebarComponent(self, self.__configuration)
        self.sidebar_component.pack()
        # self.sidebar_component.grid(
        #     row=1, column=0, sticky="nsew"
        # )  # Make it fill the space


class SidebarComponent(ctk.CTkFrame):
    def __init__(self, master, configuration, **kwargs):
        # Remove width from kwargs if it exists
        kwargs.pop("width", None)
        super().__init__(master, **kwargs)

        self.__configuration = configuration
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

    def on_hover_enter(self, event):
        self.plus_label.configure(image=self.hover_image)

    def on_hover_leave(self, event):
        self.plus_label.configure(image=self.normal_image)

    def add_server_icon(self, server_name):
        """Add a new server icon to the sidebar"""
        new_link = ctk.CTkLabel(
            self.icons_frame,
            image=self.group_image,
            text="",  # Remove text to keep width consistent
            fg_color=self.cget("fg_color"),
        )
        new_link.pack(pady=5)
        self.created_links.append(new_link)

        # Move plus button to the end
        self.plus_label.pack_forget()
        self.plus_label.pack(pady=5)
