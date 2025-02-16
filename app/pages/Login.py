import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import requests
from app.pages.Pagemanager import Page
from PIL import Image


class LoginPage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=master.config.colors["frame-color-main"],
            corner_radius=10,
        )
        self.master = master

    def create_widgets(self):
        self.__frame0 = ctk.CTkFrame(self, fg_color="transparent")
        my_image = ctk.CTkImage(
            light_image=Image.open("app/assets/logo.png"), size=(70, 70)
        )
        self.image_label = ctk.CTkLabel(self.__frame0, image=my_image, text="")
        self.project_name_label = ctk.CTkLabel(
            self.__frame0,
            text="CollabDesk",
            font=(self.master.config.font, 28, "bold"),
            text_color=self.master.config.colors["green-program"],
        )
        self.__frame0_description = ctk.CTkFrame(self, fg_color="transparent")

        self.description = ctk.CTkLabel(
            self.__frame0_description,
            text="Login to continue to CollabDesk",
            font=(self.master.config.font, 12),
            text_color=self.master.config.colors["black-text"],
            fg_color="transparent",
        )

        self.__frame1 = ctk.CTkFrame(self, fg_color="transparent")
        self.username_entry = ctk.CTkEntry(
            self.__frame1,
            placeholder_text="Enter your username or email",
            font=(self.master.config.font, 12, "normal"),
        )
        self.password_entry = ctk.CTkEntry(
            self.__frame1, show="*", placeholder_text="Password"
        )
        self.login_button = ctk.CTkButton(
            self.__frame1,
            text="Get Started",
            font=(self.master.config.font, 12),
            command=self.login,
            fg_color=self.master.config.colors["green-program"],
            text_color=self.master.config.colors["white-text"],
        )

        self.__frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.register_label = ctk.CTkLabel(
            self.__frame2,
            text="Don't have an account?",
            font=(self.master.config.font, 10),
            text_color=self.master.config.colors["grey-text"],
        )
        self.register_button = ctk.CTkButton(
            self.__frame2,
            text="Register",
            font=(self.master.config.font, 12),
            fg_color="transparent",
            text_color=self.master.config.colors["green-program"],
            command=self.navigate_to,
            hover_color="lightgrey",
        )

        # Pack the widgets
        self.__frame0.pack(pady=(20, 5))  # Logo and title frame
        self.__frame0_description.pack(pady=(0, 10))
        self.__frame1.pack(pady=10)  # Login form frame
        self.__frame2.pack(pady=10)  # Register section frame

        # Frame 0 - Logo and title section
        self.image_label.pack(side="left")
        self.project_name_label.pack(side="left")
        self.description.pack()

        # Frame 1 - Login form section
        self.username_entry.pack(pady=10, fill="x", padx=20)
        self.password_entry.pack(pady=10, fill="x", padx=20)
        self.login_button.pack(pady=10, fill="x", padx=20)

        # Frame 2 - Register section
        self.register_label.pack(side="left", padx=5)
        self.register_button.pack(side="right")

        self.username_entry.configure(width=300)  # Make entries wider
        self.password_entry.configure(width=300)

    def navigate_to(self):
        from app.pages.Register import RegisterPage

        self.master.pagemanager.switch_page(RegisterPage)

    def login(self):
        endpoint = f"{self.master.config.api_url}/login/"
        print(endpoint)
        username = self.username_entry.get()
        password = self.password_entry.get()
        payload = {"username": username, "password": password}

        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                print("Login successful!")
                CTkMessagebox(
                    title="Login",
                    message="Login successful!",
                    icon="check",
                )
            else:
                print("Login failed!")
                CTkMessagebox(
                    title="Login",
                    message="Login failed!",
                    icon="cancel",
                )
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server!")
            CTkMessagebox(
                title="Connection Error",
                message="Unable to connect to the server!",
                icon="error",
            )

        # Clear the entries
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.username_entry.focus_set()
        self.password_entry.focus_set()
