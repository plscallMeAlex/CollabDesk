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

from app.components.memberbar import MemberBar
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
        self.__is_admin: Optional[bool] = None

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
            self.__is_admin = self.check_is_admin()
        else:
            self.__current_guild = None
            self.__is_admin = False

        # Main frame for the page
        self.__mainframe = ctk.CTkFrame(self, fg_color="transparent")
        self.__mainframe.pack(expand=True, fill="both")

        # Container for sidebar, channel bar, and main content
        self.content_container = ctk.CTkFrame(self.__mainframe, fg_color="transparent")
        self.content_container.pack(expand=True, fill="both")

        # Sidebar on the left
        self.sidebar = SidebarFrame(
            self.content_container,
            self.master.configuration,
            self.change_guild_callback,
        )
        self.sidebar.pack(side="left", fill="y", padx=5)

        # Channel bar next to sidebar
        self.channel_bar = ChannelBar(
            self.content_container,
            self.master.configuration,
            self.change_frame_callback,
            self.__current_guild,
            self.logout_callback,
            self.__is_admin,
        )
        self.channel_bar.pack(side="left", fill="y")

        # Main content area (right side)
        self.main_content = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Frame container for switching
        self.frame_container = ctk.CTkFrame(
            self.main_content, fg_color="transparent", border_width=0, corner_radius=0
        )
        self.frame_container.pack(expand=True, fill="both")
        self.header = Header(
            self.frame_container,
            self.show_member_callback,
        )
        self.header.pack(fill="x")

        self.__create_initial_frame()

        # Bind window close event
        self.bind_window_close()

    def __create_initial_frame(self):
        """Create and pack the initial frame (Dashboard)"""
        guild_id = self.__current_guild
        self.__current_frame = Dashboard(
            self.frame_container,
            self.master.configuration,
            guildId=guild_id,
            is_admin=self.__is_admin,
        )
        self.__current_frame.pack(expand=True, fill="both")

    def bind_window_close(self):
        # Try to ensure clean shutdown
        root = self.winfo_toplevel()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("Closing application...")

        try:
            # Try to clean up gracefully first
            if hasattr(self, "__current_frame") and self.__current_frame:
                if hasattr(self.__current_frame, "stop_updates"):
                    self.__current_frame.stop_updates()

            # Cancel all after events we know about
            for after_id in self.__after_ids:
                try:
                    self.after_cancel(after_id)
                except:
                    pass

            # Use a more aggressive approach - terminate all Tkinter callbacks
            try:
                # Cancel all pending after events globally
                for id in self.tk.call("after", "info"):
                    try:
                        self.tk.call("after", "cancel", id)
                    except:
                        pass
            except:
                pass

            # Destroy the main window forcefully
            try:
                if hasattr(self.master, "_root"):
                    self.master._root().quit()
                else:
                    self.master.quit()
            except:
                pass

        except Exception as e:
            print(f"Error during cleanup: {e}")

        # As a last resort, use os._exit to forcefully terminate
        print("Exiting application")
        import os

        os._exit(0)  # This forces immediate termination

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

        self.__is_admin = self.check_is_admin()
        self.channel_bar.set_is_admin(self.__is_admin)
        # Create new BulletinBoard frame
        self.__current_frame = Dashboard(
            self.frame_container,
            self.master.configuration,
            guildId=self.__current_guild,
            is_admin=self.__is_admin,
        )
        self.__current_frame.pack(expand=True, fill="both")

        # Update the is_admin status

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
                is_admin=self.__is_admin,
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

    def logout_callback(self):
        """Logout callback"""
        self.master.token_manager.destroy_token()
        from app.pages.login import LoginPage

        # Destroy current frame
        self.master.pagemanager.switch_page(LoginPage)

    def show_member_callback(self):
        """Show member callback"""
        bar = self.member_bars = MemberBar(
            self.master,
            self.master.configuration,
            self.__current_guild,
        )
        bar.grab_set()
        bar.wait_window()

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

    def check_is_admin(self):
        """Check if the user is an admin of the current guild"""
        if not self.__current_guild:
            return False

        user_id = self.master.configuration.load_user_data()
        params = {
            "guild_id": self.__current_guild,
            "user_id": user_id,
        }
        try:
            response = requests.get(
                f"{self.master.configuration.api_url}/roles/get_role_by_user/",
                params=params,
            )
            if response.status_code == 200:
                role = response.json()
                if role and "admin" in role["name"].lower():
                    return True
                else:
                    return False
        except requests.RequestException as e:
            print(f"Error fetching roles: {e}")
            return False
