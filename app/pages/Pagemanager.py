import customtkinter as ctk


#  The base class for all pages
# Inherit from this class to create a new page.
class Page(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

    # This function must be overridden in the child class
    def create_widgets(self):
        raise NotImplementedError("create_widgets method must be overridden")

    # This function can be overridden or not in the child class
    def navigate_to(self):
        pass


# Page manager class to manage page changes in the app
class Pagemanager:
    def __init__(self, master):
        self.master = master
        self.current_page = None

    def switch_page(self, new_page: Page):
        if self.current_page is not None:
            self.current_page.destroy()

        # delay the creation of the new page to avoid flickering
        self.master.after(100, self.__create_page, new_page)

    def switch_frame(self, old_frame: ctk.CTkFrame, new_frame: ctk.CTkFrame):
        if old_frame is not None:
            old_frame.destroy()

        new_frame.pack(expand=True, fill="both")

    def __create_page(self, new_page: Page):
        self.current_page = new_page(self.master)
        self.current_page.pack(expand=True, fill="both")
        self.current_page.create_widgets()
