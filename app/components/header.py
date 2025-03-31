import customtkinter as ctk


class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(height=40, fg_color="#ffffff")
        self.pack_propagate(False)

        # Dashboard text on left
        ctk.CTkLabel(self, text="📊 Dashboard", font=("Inter", 14, "bold")).pack(
            side="left", padx=15
        )

        # Icons on right
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="right", padx=15)

        # Member/people icon
        ctk.CTkButton(
            right_frame,
            text="👥",
            width=30,
            fg_color="transparent",
            hover_color="#f0f0f0",
        ).pack(side="right", padx=5)

        # Notification bell icon
        ctk.CTkButton(
            right_frame,
            text="🔔",
            width=30,
            fg_color="transparent",
            hover_color="#f0f0f0",
        ).pack(side="right", padx=5)


# Example usage:
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")

    # Create and pack the header
    header = Header(root)
    header.pack(side="top", fill="x", pady=0)

    root.mainloop()
