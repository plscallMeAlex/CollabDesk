import os
import sys
import ctypes


# Suppress Tkinter error messages
def suppress_tkinter_errors():
    """
    Attempt to suppress Tkinter-related error messages across different platforms
    """
    try:
        # Windows-specific error suppression
        if sys.platform.startswith("win"):
            # Disable Windows error reporting dialog
            ctypes.windll.kernel32.SetErrorMode(
                0x0001  # SEM_FAILCRITICALERRORS
                | 0x0002  # SEM_NOGCGENERRORBOX
                | 0x8000  # SEM_NOOPENFILEERRORBOX
            )

        # Redirect stderr to devnull to suppress error messages
        sys.stderr = open(os.devnull, "w")
    except Exception:
        pass


# Apply error suppression early
suppress_tkinter_errors()

import customtkinter as ctk
import tkinter as tk
import requests
from typing import Dict, Optional
from app.pages.pagemanager import Page
from app.frames.bulletinboard import BulletinBoard
from app.components.sidebar import SidebarFrame
from app.components.header import Header
from app.components.channelbar import ChannelBar
from app.frames.calendar import TaskCalendarWidget
from app.frames.dashboard import Dashboard
from app.frames.textchannel import ChatFrame


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=master.configuration.colors["frame-color-secondary"],
        )
        self.master = master
        self.__current_guild: Optional[str] = None
        self.__current_frame: Optional[ctk.CTkFrame] = None

        # Track and clean up after events
        self.__after_ids: list = []

        # Disable Tkinter error reporting
        self._disable_tk_error_reporting()

    def _disable_tk_error_reporting(self):
        """
        Additional method to disable Tkinter error reporting
        """
        try:
            # Attempt to redirect Tk error reporting
            tk.Tcl().eval("package require Tk")
            tk.Tcl().eval("proc bgerror {} {}")
        except Exception:
            pass

    def create_widgets(self):
        # Fetch the guilds
        response = self.__fetch_guilds()

        # Set the current guild to the first one in the list
        if response:
            self.__current_guild = response[0]["id"]
        else:
            self.__current_guild = None

        # Main frame for the page
        self.__mainframe = ctk.CTkFrame(self, fg_color="transparent")
        self.__mainframe.pack(expand=True, fill="both")

        # Header at the top
        # self.header = Header(self.__mainframe)
        # self.header.pack(side="top", fill="x", pady=10)

        # Container for sidebar, channel bar, and main content
        self.content_container = ctk.CTkFrame(self.__mainframe, fg_color="transparent")
        self.content_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Sidebar on the left
        self.sidebar = SidebarFrame(
            self.content_container,
            self.master.configuration,
            self.change_guild_callback,
        )
        self.sidebar.pack(side="left", fill="y")

        # Channel bar next to sidebar
        self.channel_bar = ChannelBar(
            self.content_container,
            self.master.configuration,
            self.change_frame_callback,
            self.__current_guild,
        )
        self.channel_bar.pack(side="left", fill="y")

        # Main content area (right side)
        self.main_content = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Frame container for switching
        self.frame_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.frame_container.pack(expand=True, fill="both", pady=20)

        # Initial frame
        self.__create_initial_frame()

        # Bind window close event
        self.bind_window_close()

    def __create_initial_frame(self):
        """Create and pack the initial frame (Dashboard)"""
        guild_id = self.__current_guild
        self.__current_frame = Dashboard(
            self.frame_container, self.master.configuration, guildId=guild_id
        )
        self.__current_frame.pack(expand=True, fill="both")

    def bind_window_close(self):
        # Try to ensure clean shutdown
        root = self.winfo_toplevel()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Cancel any pending after events
        for after_id in self.__after_ids:
            try:
                self.after_cancel(after_id)
            except Exception:
                pass

        # Destroy main components
        components_to_destroy = [
            self.header,
            self.sidebar,
            self.channel_bar,
            self.frame_container,
            self.main_content,
            self.content_container,
            self.__mainframe,
        ]

        for component in components_to_destroy:
            try:
                component.destroy()
            except Exception:
                pass

        # Close the window
        try:
            self.master.quit()
            self.master.destroy()
        except Exception:
            pass

    def change_guild_callback(self, guild_id):
        # Update current guild
        self.__current_guild = guild_id

        # Destroy current frame
        if self.__current_frame:
            try:
                self.__current_frame.destroy()
            except Exception:
                pass
        self.channel_bar.refresh_channels(guild_id)

        # Create new BulletinBoard frame
        self.__current_frame = Dashboard(
            self.frame_container,
            self.master.configuration,
            guildId=self.__current_guild,
        )
        self.__current_frame.pack(expand=True, fill="both")

    def change_frame_callback(self, frame_name, channel=None):
        # Destroy current frame
        if self.__current_frame:
            try:
                self.__current_frame.destroy()
            except Exception:
                pass

        # Create new frame based on frame_name
        if frame_name == "BulletinBoard":
            self.__current_frame = BulletinBoard(
                self.frame_container,
                self.master.configuration,
                guildId=self.__current_guild,
            )
        elif frame_name == "Calendar":
            self.__current_frame = TaskCalendarWidget(
                self.frame_container,
                self.master.configuration,
                guildId=self.__current_guild,
            )
        elif frame_name == "Dashboard":
            self.__current_frame = Dashboard(
                self.frame_container,
                self.master.configuration,
                guildId=self.__current_guild,
            )

        elif frame_name == "TextChannel":
            print("TextChannel")
            self.__current_frame = ChatFrame(
                self.frame_container,
                self.master.configuration,
                channel=channel,
            )
        else:
            return  # Unknown frame

        # Pack the new frame
        self.__current_frame.pack(expand=True, fill="both")

    def __fetch_guilds(self):
        params = {"user_id": self.master.configuration.load_user_data()}
        try:
            response = requests.get(
                self.master.configuration.api_url + "/guilds/get_guilds_by_user/",
                params=params,
            )

            if response.status_code == 200:
                return response.json()
        except Exception:
            pass

        return []
