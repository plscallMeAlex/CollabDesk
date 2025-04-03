import customtkinter as ctk


class Header(ctk.CTkFrame):
    def __init__(
        self, master, memberbar_callback, title="📊 Dashboard", height=30, **kwargs
    ):
        super().__init__(master, corner_radius=0, border_width=0, **kwargs)
        self.memberbar_callback = memberbar_callback
        # Configure the header appearance - add a specific border_width=0 to eliminate the line
        self.configure(height=height, fg_color="#ffffff", border_width=0)

        # Use a specific height and don't propagate to maintain consistent sizing
        self.pack_propagate(False)

        # Make sure the header expands horizontally
        self.columnconfigure(0, weight=1)  # Title column expands
        self.columnconfigure(1, weight=0)  # Right frame stays fixed width

        # Dashboard text on left with customizable title
        self.title_label = ctk.CTkLabel(
            self, text=title, font=("Inter", 14, "bold"), anchor="w"  # Left alignment
        )
        self.title_label.grid(
            row=0, column=0, sticky="w", padx=15, pady=(height // 2 - 10, 0)
        )

        # Right frame for icons - set a specific height to match
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent", height=height)
        self.right_frame.grid(row=0, column=1, sticky="e", padx=15, pady=0)
        self.right_frame.pack_propagate(False)  # Keep consistent height

        # Member/people icon button
        self.members_button = ctk.CTkButton(
            self.right_frame,
            text="👥",
            width=30,
            height=height,  # Match parent height
            fg_color="transparent",
            text_color="black",
            corner_radius=8,
            hover_color="#f0f0f0",
            command=self.memberbar_callback,
        )
        self.members_button.pack(side="right", padx=5, pady=0)

        # Notification bell icon button
        self.notification_button = ctk.CTkButton(
            self.right_frame,
            text="🔔",
            width=30,
            height=height,  # Match parent height
            fg_color="transparent",
            text_color="black",
            corner_radius=8,
            hover_color="#f0f0f0",
        )
        self.notification_button.pack(side="right", padx=5, pady=0)

        # Add Bottom Border (Thin Frame)
        self.bottom_border = ctk.CTkFrame(
            self,
            height=1,
            fg_color="#cccccc",
        )
        self.bottom_border.pack(side="bottom", fill="x", pady=(20, 0))

    def set_title(self, title):
        """Update the header title"""
        self.title_label.configure(text=title)

    def add_button(self, text, command=None, **kwargs):
        """Add a custom button to the right side of the header"""
        button = ctk.CTkButton(
            self.right_frame,
            text=text,
            width=30,
            height=self.winfo_height(),  # Use parent height
            fg_color="transparent",
            hover_color="#f0f0f0",
            corner_radius=8,
            command=command,
            **kwargs
        )
        button.pack(side="right", padx=5)
        return button
