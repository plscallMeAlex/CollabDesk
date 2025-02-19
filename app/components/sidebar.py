import customtkinter as ctk
from PIL import Image, ImageTk

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # delete it after finish side bar
        self.configure(border_width=2, border_color="black")

        self.logo_image = Image.open("app/assets/logo.png")  
        self.logo_image = self.logo_image.resize((100, 100), Image.Resampling.LANCZOS) 
        self.logo_tk = ImageTk.PhotoImage(self.logo_image)  
        self.logo_label = ctk.CTkLabel(self, image=self.logo_tk, text="") 
        self.logo_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.sidebar_component = SidebarComponent(self)
        self.sidebar_component.grid(row=1, column=0, pady=0)


class SidebarComponent(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Load the images for the button (normal and hover)
        self.normal_image = Image.open("app/assets/plus.png")  # Path to your plus.png image
        self.normal_image = self.normal_image.resize((60, 60))  # Resize image as needed
        self.normal_tk = ImageTk.PhotoImage(self.normal_image)

        self.hover_image = Image.open("app/assets/plus_hover.png")  # Path to your hover image
        self.hover_image = self.hover_image.resize((60, 60))  # Resize image as needed
        self.hover_tk = ImageTk.PhotoImage(self.hover_image)

        # Create a label to display the image
        self.plus_label = ctk.CTkLabel(
            self, 
            image=self.normal_tk,  # Default image for the label
            text="",  # No text, just the image
            fg_color="transparent",  # Set background color to transparent
            bg_color="#d9d9d9"  # Set background color to transparent
        )
        
        # Bind the hover events
        self.plus_label.grid(row=0, column=0, pady=0)
        self.plus_label.bind("<Button-1>", self.on_image_click)  
        self.plus_label.bind("<Enter>", self.on_hover_enter) 
        self.plus_label.bind("<Leave>", self.on_hover_leave)  

    def on_image_click(self, event):
        print("Sidebar Image Clicked")

    def on_hover_enter(self, event):
        self.plus_label.configure(image=self.hover_tk)

    def on_hover_leave(self, event):
        self.plus_label.configure(image=self.normal_tk)


if __name__ == "__main__":
    app = ctk.CTk()
    
    sidebar_frame = SidebarFrame(app)
    sidebar_frame.pack(side="left", padx=0, pady=0)

    app.mainloop()
