import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps  # Add ImageOps here

# Sidebar Frame containing Sidebar Component
class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Set the border for SidebarFrame
        self.configure(border_width=2, border_color="black")

        # Load image as logo (Ensure the image path is correct)
        logo_image = Image.open("app/assets/logo.png")  # Replace with your image file path
        logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
        # Use CTkImage instead of ImageTk.PhotoImage
        self.logo_ctk = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))

        # Create logo label with image
        self.logo_label = ctk.CTkLabel(self, image=self.logo_ctk, text="")
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Label for SidebarFrame
        self.label = ctk.CTkLabel(self, text="Sidebar Frame")
        self.label.grid(row=1, column=0, pady=10)

        # Create SidebarComponent inside SidebarFrame
        self.sidebar_component = SidebarComponent(self)
        self.sidebar_component.grid(row=2, column=0, pady=20)

# Sidebar Component with a button inside the SidebarFrame
class SidebarComponent(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        try:
            # Try to load plus.png
            plus_image = Image.open("app/assets/plus.png")
            # Resize if needed
            plus_image = ImageOps.fit(plus_image, (40, 40), Image.Resampling.LANCZOS)
            
            # Create a background canvas matching button color
            button_img = Image.new("RGB", (60, 60), (59, 142, 208))
            
            # Paste plus.png in the center
            paste_position = ((60 - plus_image.width) // 2, (60 - plus_image.height) // 2)
            button_img.paste(plus_image, paste_position, plus_image if plus_image.mode == 'RGBA' else None)
            
        except Exception as e:
            # Fallback to drawing the plus if image load fails
            print(f"Error loading plus.png: {e}. Using drawn plus instead.")
            button_img = Image.new("RGB", (60, 60), (59, 142, 208))
            draw = ImageDraw.Draw(button_img)
            
            # Draw the plus symbol
            line_color = (255, 255, 255)  # White color
            draw.rectangle([(15, 28), (45, 32)], fill=line_color)  # Horizontal
            draw.rectangle([(28, 15), (32, 45)], fill=line_color)  # Vertical
        
        # Convert to CTkImage - save as instance attribute to prevent garbage collection
        self.plus_ctk = ctk.CTkImage(light_image=button_img, dark_image=button_img, size=(60, 60))

        # Button inside SidebarComponent
        self.button = ctk.CTkButton(
            self,
            image=self.plus_ctk,
            text="",
            width=60,
            height=60,
            corner_radius=30,
            fg_color="#3B8ED0",
            hover_color="#36719F",
            command=self.on_button_click
        )
        
        # Grid method
        self.button.grid(row=0, column=0, pady=20)
    
    def on_button_click(self):
        print("Sidebar Button Clicked")
