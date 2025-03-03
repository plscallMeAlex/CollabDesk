import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import requests
from app.make_request import make_request
from app.pages.pagemanager import Page
from PIL import Image


class RegisterPage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent",
        )
        self.master = master
        self.__localframe = ctk.CTkFrame(
            self,
            fg_color=self.master.config.colors["frame-color-main"],
            corner_radius=10,
        )
        self.__localframe.place(relx=0.5, rely=0.5, anchor="center")

    def create_widgets(self):
        # Center the main frame
        self.__main_frame = ctk.CTkFrame(
            self.__localframe, fg_color="white", corner_radius=20
        )
        self.__main_frame.pack(padx=20, pady=20, ipadx=20, ipady=20)

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

        # Form container
        self.__form_frame = ctk.CTkFrame(self.__main_frame, fg_color="transparent")

        # Create form fields with labels
        # Username
        self.__username_frame = ctk.CTkFrame(self.__form_frame, fg_color="transparent")
        self.username_label = ctk.CTkLabel(
            self.__username_frame,
            text="Username:",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
            width=100,
            anchor="e",
        )
        self.username_entry = ctk.CTkEntry(
            self.__username_frame,
            font=(self.master.config.font, 14),
            width=300,
        )

        # First name
        self.__firstname_frame = ctk.CTkFrame(self.__form_frame, fg_color="transparent")
        self.firstname_label = ctk.CTkLabel(
            self.__firstname_frame,
            text="First Name:",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
            width=100,
            anchor="e",
        )
        self.firstname_entry = ctk.CTkEntry(
            self.__firstname_frame,
            font=(self.master.config.font, 14),
            width=300,
        )

        # Last name
        self.__lastname_frame = ctk.CTkFrame(self.__form_frame, fg_color="transparent")
        self.lastname_label = ctk.CTkLabel(
            self.__lastname_frame,
            text="Last Name:",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
            width=100,
            anchor="e",
        )
        self.lastname_entry = ctk.CTkEntry(
            self.__lastname_frame,
            font=(self.master.config.font, 14),
            width=300,
        )

        # Email
        self.__email_frame = ctk.CTkFrame(self.__form_frame, fg_color="transparent")
        self.email_label = ctk.CTkLabel(
            self.__email_frame,
            text="Email:",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
            width=100,
            anchor="e",
        )
        self.email_entry = ctk.CTkEntry(
            self.__email_frame,
            font=(self.master.config.font, 14),
            width=300,
        )

        # Password
        self.__password_frame = ctk.CTkFrame(self.__form_frame, fg_color="transparent")
        self.password_label = ctk.CTkLabel(
            self.__password_frame,
            text="Password:",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
            width=100,
            anchor="e",
        )
        self.password_entry = ctk.CTkEntry(
            self.__password_frame,
            show="*",
            font=(self.master.config.font, 14),
            width=300,
        )

        # Confirm Password
        self.__confirm_password_frame = ctk.CTkFrame(
            self.__form_frame, fg_color="transparent"
        )
        self.confirm_password_label = ctk.CTkLabel(
            self.__confirm_password_frame,
            text="Confirm:",
            font=(self.master.config.font, 14),
            text_color=self.master.config.colors["black-text"],
            width=100,
            anchor="e",
        )
        self.confirm_password_entry = ctk.CTkEntry(
            self.__confirm_password_frame,
            show="*",
            font=(self.master.config.font, 14),
            width=300,
        )

        self.password_status = ctk.CTkLabel(
            self.__main_frame, text="", text_color="red"
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

        # Pack form container
        self.__form_frame.pack(pady=5)

        # Pack form fields
        self.__username_frame.pack(pady=5)
        self.username_label.pack(side="left", padx=(0, 10))
        self.username_entry.pack(side="left")

        self.__firstname_frame.pack(pady=5)
        self.firstname_label.pack(side="left", padx=(0, 10))
        self.firstname_entry.pack(side="left")

        self.__lastname_frame.pack(pady=5)
        self.lastname_label.pack(side="left", padx=(0, 10))
        self.lastname_entry.pack(side="left")

        self.__email_frame.pack(pady=5)
        self.email_label.pack(side="left", padx=(0, 10))
        self.email_entry.pack(side="left")

        self.__password_frame.pack(pady=5)
        self.password_label.pack(side="left", padx=(0, 10))
        self.password_entry.pack(side="left")

        self.__confirm_password_frame.pack(pady=5)
        self.confirm_password_label.pack(side="left", padx=(0, 10))
        self.confirm_password_entry.pack(side="left")

        self.password_status.pack(pady=5)
        self.register_button.pack(pady=15)

        self.__footer_frame.pack(pady=10)
        self.login_label.pack(side="left", padx=5)
        self.login_button.pack(side="left")

        # Track changes in confirm password entry
        self.confirm_password_var = ctk.StringVar()
        self.confirm_password_entry.configure(textvariable=self.confirm_password_var)
        self.confirm_password_var.trace_add("write", self.check_password_match)

    def navigate_to(self):
        from app.pages.login import LoginPage

        self.master.pagemanager.switch_page(LoginPage)

    def register(self):
        username = self.username_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if password != self.confirm_password_entry.get() or len(password) < 8:
            return

        api_url = f"{self.master.config.api_url}/users/register/"
        data = {
            "username": username,
            "first_name": firstname,
            "last_name": lastname,
            "email": email,
            "password": password,
        }

        try:
            response = make_request(api_url, method="POST", json=data)
            if response.status_code == 201:
                CTkMessagebox(
                    title="Success",
                    message="Account created successfully",
                    icon="check",
                    option_1="OK",
                )
                self.navigate_to()
            else:
                CTkMessagebox(
                    "Error",
                    "Account not created please try again T_T",
                    icon="cancel",
                    option_1="OK",
                )
        except requests.exceptions.RequestException as e:
            CTkMessagebox(
                title="Error",
                message="Unable to connect to the server",
                icon="cancel",
                option_1="OK",
            )

    def check_password_match(self, *args):
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if len(password) < 8:
            self.password_status.configure(
                text="❌ Password must be at least 8 characters", text_color="red"
            )
        elif password == confirm_password:
            self.password_status.configure(
                text="✅ Passwords match", text_color="green"
            )
        else:
            self.password_status.configure(
                text="❌ Passwords do not match", text_color="red"
            )
