import customtkinter as ctk
from app.pages.Pagemanager import Page
from PIL import Image


class RegisterPage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=master.config.colors["frame-color-main"],
            corner_radius=15,
        )
        self.master = master

    def create_widgets(self):
        # Center the main frame
        self.__main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.__main_frame.pack(
            padx=20, pady=20, ipadx=20, ipady=20
        )  # Padding around the form

        # Header Section
        self.__header_frame = ctk.CTkFrame(self.__main_frame, fg_color="transparent")
        my_image = ctk.CTkImage(
            light_image=Image.open("app/assets/logo.png"), size=(70, 70)
        )
        self.image_label = ctk.CTkLabel(self.__header_frame, image=my_image, text="")
        self.project_name_label = ctk.CTkLabel(
            self.__header_frame,
            text="CollabDesk",
            font=(self.master.config.font, 28, "bold"),
            text_color=self.master.config.colors["green-program"],
        )
        self.description_label = ctk.CTkLabel(
            self.__main_frame,
            text="Register to continue to CollabDesk",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
        )

        # Register Form Section
        self.username_entry = ctk.CTkEntry(
            self.__main_frame,
            placeholder_text="Enter your username",
            font=(self.master.config.font, 14),
            width=300,
        )
        self.firstname_entry = ctk.CTkEntry(
            self.__main_frame,
            placeholder_text="Enter your firstname",
            font=(self.master.config.font, 14),
            width=300,
        )
        self.lastname_entry = ctk.CTkEntry(
            self.__main_frame,
            placeholder_text="Enter your lastname",
            font=(self.master.config.font, 14),
            width=300,
        )
        self.email_entry = ctk.CTkEntry(
            self.__main_frame,
            placeholder_text="Enter your email",
            font=(self.master.config.font, 14),
            width=300,
        )
        self.password_entry = ctk.CTkEntry(
            self.__main_frame,
            show="*",
            placeholder_text="Password",
            font=(self.master.config.font, 14),
            width=300,
        )
        self.confirm_password_entry = ctk.CTkEntry(
            self.__main_frame,
            show="*",
            placeholder_text="Confirm Password",
            font=(self.master.config.font, 14),
            width=300,
        )
        self.register_button = ctk.CTkButton(
            self.__main_frame,
            text="Register",
            font=(self.master.config.font, 14, "bold"),
            command=self.register,
            fg_color=self.master.config.colors["green-program"],
            text_color=self.master.config.colors["white-text"],
            corner_radius=10,
        )

        # Footer Section
        self.__footer_frame = ctk.CTkFrame(self.__main_frame, fg_color="transparent")
        self.login_label = ctk.CTkLabel(
            self.__footer_frame,
            text="Already have an account?",
            font=(self.master.config.font, 10),
            text_color=self.master.config.colors["grey-text"],
        )
        self.login_button = ctk.CTkButton(
            self.__footer_frame,
            text="Login",
            font=(self.master.config.font, 12),
            fg_color="transparent",
            text_color=self.master.config.colors["green-program"],
            command=self.navigate_to,
            hover_color="lightgrey",
        )

        # Layout
        self.__header_frame.pack(pady=10)
        self.image_label.pack(side="left", padx=5)
        self.project_name_label.pack(side="left", padx=5)
        self.description_label.pack(pady=(0, 20))

        self.username_entry.pack(pady=5)
        self.firstname_entry.pack(pady=5)
        self.lastname_entry.pack(pady=5)
        self.email_entry.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.confirm_password_entry.pack(pady=5)
        self.register_button.pack(pady=15)

        self.__footer_frame.pack(pady=10)
        self.login_label.pack(side="left", padx=5)
        self.login_button.pack(side="left")

    def navigate_to(self):
        from app.pages.Login import LoginPage

        self.master.pagemanager.switch_page(LoginPage)
