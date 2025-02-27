import customtkinter as ctk


class Frame(ctk.CTkFrame):
    def __init__(self, master, configuration, guildId, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self._configuration = configuration
        self._guildId = guildId

    # This function must be overridden in the child class
    def create_widgets(self):
        raise NotImplementedError("create_widgets method must be overridden")
