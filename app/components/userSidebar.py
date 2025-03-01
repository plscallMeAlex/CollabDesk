import customtkinter as ctk

class UserSideBar(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)  # Pass the master to the parent constructor
        self.configure(fg_color="white")  # Set background color to white
        self.create_user_sidebar()

    def create_user_sidebar(self):
        # User list sidebar (fill the full height of the window)
        user_sidebar = ctk.CTkFrame(self, fg_color="white", corner_radius=0, width=240)
        user_sidebar.pack(side="left", fill="y")  # This will make the sidebar fill the full height

        # User list header
        user_header = ctk.CTkFrame(user_sidebar, fg_color="transparent", height=48)
        user_header.pack(fill="x", padx=0, pady=0)

        # Search box
        search_box = ctk.CTkEntry(
            user_header,
            placeholder_text="Search",
            width=200,
            height=28,
            corner_radius=4,
            border_width=0,
            fg_color="#f1f1f1",  # Lighter gray background for the search box
            text_color="black",  # Text color set to black for better visibility on light background
            placeholder_text_color="#72767d"
        )
        search_box.place(relx=0.5, rely=0.5, anchor="center")

        # User list container
        user_list_frame = ctk.CTkScrollableFrame(user_sidebar, fg_color="white")
        user_list_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Online users category
        online_category = ctk.CTkFrame(user_list_frame, fg_color="transparent", height=30)
        online_category.pack(fill="x", padx=10, pady=(10, 2))

        online_label = ctk.CTkLabel(online_category, text="ONLINE — 3", font=("Arial", 12), text_color="#333333")
        online_label.pack(side="left", padx=5)

        # Add online users
        users = ["User1", "User2", "Yourself"]
        for user in users:
            user_frame = ctk.CTkFrame(user_list_frame, fg_color="transparent", height=42)
            user_frame.pack(fill="x", padx=10, pady=2)

            # Status indicator (green dot for online)
            status = ctk.CTkButton(
                user_frame,
                text="",
                width=10,
                height=10,
                corner_radius=5,
                fg_color="#43b581",  # Green for online status
                hover_color="#43b581"
            )
            status.place(x=2, y=16)

            # User avatar (placeholder)
            avatar = ctk.CTkButton(
                user_frame,
                text="",
                width=32,
                height=32,
                corner_radius=16,
                fg_color="#7289da" if user != "Yourself" else "#43b581",  # Blue for others, green for yourself
                hover_color="#7289da" if user != "Yourself" else "#43b581"
            )
            avatar.place(x=20, y=5)

            # Username
            username = ctk.CTkLabel(user_frame, text=user, font=("Arial", 14), text_color="black")  # Black text color for readability
            username.place(x=60, y=10)

# Main application window
if __name__ == "__main__":
    app = ctk.CTk()
    app.configure(fg_color="white")  # Set the window background to white
    sidebar = UserSideBar(master=app)
    sidebar.pack(fill="both", expand=True)
    app.mainloop()
