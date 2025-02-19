import customtkinter as ctk
from PIL import Image

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(border_width=2, border_color="black", fg_color="#D9D9D9")  # Set background color

        self.logo_image = ctk.CTkImage(
            light_image=Image.open("app/assets/logo.png"),
            size=(100, 100)
        )
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="", fg_color="#D9D9D9")
        self.logo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.sidebar_component = SidebarComponent(self, fg_color="#D9D9D9")
        self.sidebar_component.grid(row=1, column=0, pady=0)


class SidebarComponent(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#D9D9D9")  # Set background color

        # Plus button images
        self.normal_image = ctk.CTkImage(
            light_image=Image.open("app/assets/plus.png"),
            size=(60, 60)
        )
        self.hover_image = ctk.CTkImage(
            light_image=Image.open("app/assets/plus_hover.png"),
            size=(60, 60)
        )

        # Group button images (New hover effect added)
        self.group_image = ctk.CTkImage(
            light_image=Image.open("app/assets/Group.png"),
            size=(60, 60)
        )
        self.group_hover_image = ctk.CTkImage(
            light_image=Image.open("app/assets/Group_hover.png"),
            size=(60, 60)
        )

        self.plus_label = ctk.CTkLabel(
            self, 
            image=self.normal_image,  
            text="", 
            fg_color="#D9D9D9"
        )
        self.plus_label.grid(row=0, column=0, pady=5)

        self.plus_label.bind("<Button-1>", lambda event: self.on_button_click())
        self.plus_label.bind("<Enter>", self.on_hover_enter)
        self.plus_label.bind("<Leave>", self.on_hover_leave)

        self.created_links = []

    def on_button_click(self):
        print("Sidebar Image Clicked")

        # Temporarily remove plus_label to reposition it
        self.plus_label.grid_remove()

        new_link = ctk.CTkLabel(
            self, 
            image=self.group_image, 
            text="",
            fg_color="#D9D9D9"
        )
        new_link.image = self.group_image  # Prevent garbage collection issue

        # Bind click event to navigate function
        new_link.bind("<Button-1>", lambda event, page="group_page": self.navigate_to_page(page))

        # Add hover effect for Group.png
        new_link.bind("<Enter>", lambda event, lbl=new_link: lbl.configure(image=self.group_hover_image))
        new_link.bind("<Leave>", lambda event, lbl=new_link: lbl.configure(image=self.group_image))

        # Insert at the top
        self.created_links.insert(0, new_link)

        # Reposition all elements
        for i, link in enumerate(self.created_links):
            link.grid(row=i, column=0, pady=5)

        # Put the plus_label at the last row
        self.plus_label.grid(row=len(self.created_links), column=0, pady=5)

    def on_hover_enter(self, event):
        self.plus_label.configure(image=self.hover_image)

    def on_hover_leave(self, event):
        self.plus_label.configure(image=self.normal_image)

    def navigate_to_page(self, page_name):
        """Handles page navigation logic"""
        print(f"Navigating to {page_name}")


if __name__ == "__main__":
    app = ctk.CTk()
    app.configure(fg_color="#D9D9D9")  # Set background color

    sidebar_frame = SidebarFrame(app)
    sidebar_frame.pack(side="left", padx=0, pady=0)

    app.mainloop()
