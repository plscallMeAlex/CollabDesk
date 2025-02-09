import customtkinter as ctk


#  The base class for all pages
class Page(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

    # This function must be overridden in the child class
    def create_widgets(self):
        raise NotImplementedError("create_widgets method must be overridden")


# Page manager class to manage page changes in the app
class Pagemanager:
    def __init__(self, master):
        self.master = master
        self.current_page = None

    def page_change(self, new_page: Page):
        if self.current_page is not None:
            self.current_page.destroy()

        self.current_page = new_page(self.master)
        self.current_page.place(relx=0.5, rely=0.5, anchor="center")
        self.current_page.create_widgets()
