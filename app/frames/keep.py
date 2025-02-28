import customtkinter as ctk
from app.frames.frame import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from datetime import datetime

class Dashboard(Frame):
    def __init__(self, master, configuration, **kwargs):
        super().__init__(master, configuration, **kwargs)
        
        # Sample data
        self.announcements = [
            {
                "title": "Sprint 5 Kickoff",
                "content": "Team,\n\nWe're making great progress on our current sprint. As you can see from our dashboard, we still have 50% of tasks in the backlog, but we're moving steadily with 30% of tasks currently in progress.\n\nRemember our upcoming deadline on March 15th. Alex and D are handling most of the workload, so please offer support where needed.\n\nGreat job everyone!",
                "author": "Project Manager",
                "date": "Feb 25, 2025"
            },
            {
                "title": "New Team Member Onboarding",
                "content": "Please welcome Jon to our development team. He'll be focusing on frontend tasks starting next week.",
                "author": "HR Department",
                "date": "Feb 24, 2025" 
            },
            {
                "title": "Infrastructure Update",
                "content": "Server maintenance scheduled for this weekend. Please save all work by Friday 5PM.",
                "author": "IT Support",
                "date": "Feb 23, 2025"
            }
        ]
        
        self.activities = [
            {"user": "Alex", "action": "updated task 'Database integration' to 'In Progress'", "time": "Feb 26, 2025 - 10:45 AM"},
            {"user": "Jon", "action": "completed task 'User authentication flow'", "time": "Feb 26, 2025 - 09:30 AM"},
            {"user": "D", "action": "added comments to task 'API documentation'", "time": "Feb 25, 2025 - 04:15 PM"},
            {"user": "Thun", "action": "created new task 'Frontend testing'", "time": "Feb 25, 2025 - 02:20 PM"},
            {"user": "Alex", "action": "completed task 'Login page design'", "time": "Feb 25, 2025 - 11:05 AM"},
            {"user": "D", "action": "updated task 'Backend optimization' to 'In Progress'", "time": "Feb 24, 2025 - 03:40 PM"},
            {"user": "Jon", "action": "commented on task 'Mobile responsiveness'", "time": "Feb 24, 2025 - 01:15 PM"},
            {"user": "Thun", "action": "assigned task 'Security audit' to Alex", "time": "Feb 24, 2025 - 11:30 AM"},
            {"user": "Alex", "action": "updated task 'User profile page' to 'Done'", "time": "Feb 23, 2025 - 04:50 PM"},
            {"user": "D", "action": "created task 'Database optimization'", "time": "Feb 23, 2025 - 02:10 PM"},
        ]
        
        self.current_announcement = 0
        self.current_activity_page = 0
        self.activities_per_page = 5
        
        self.create_widgets()
        
    def create_widgets(self):
        # Configure the main layout
        self.configure(fg_color="#f5f5f5")
        
        # Main content area - split into left and right sections
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left section
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Team Leader Announcement
        announcement_frame = ctk.CTkFrame(left_frame, fg_color="#e0e0e0", corner_radius=10)
        announcement_frame.pack(fill="x", pady=(0, 20))
        
        announcement_header = ctk.CTkFrame(announcement_frame, fg_color="transparent", height=40)
        announcement_header.pack(fill="x")
        
        announcement_label = ctk.CTkLabel(announcement_header, text="Team Leader Announcement", 
                                         font=("Arial", 16, "bold"), fg_color="transparent")
        announcement_label.pack(side="left", padx=20, pady=10)
        
        # Navigation buttons for announcements
        nav_buttons_frame = ctk.CTkFrame(announcement_header, fg_color="transparent")
        nav_buttons_frame.pack(side="right", padx=20)
        
        self.prev_announcement_btn = ctk.CTkButton(nav_buttons_frame, text="◀", width=30, 
                                               fg_color="#d0d0d0", text_color="black", 
                                               corner_radius=5, command=self.prev_announcement)
        self.prev_announcement_btn.pack(side="left", padx=5)
        
        self.next_announcement_btn = ctk.CTkButton(nav_buttons_frame, text="▶", width=30, 
                                               fg_color="#d0d0d0", text_color="black", 
                                               corner_radius=5, command=self.next_announcement)
        self.next_announcement_btn.pack(side="left", padx=5)
        
        # Announcement content
        self.announcement_content_frame = ctk.CTkFrame(announcement_frame, fg_color="white", corner_radius=5)
        self.announcement_content_frame.pack(fill="both", padx=20, pady=(0, 20), ipady=10)
        
        # Title
        self.announcement_title = ctk.CTkLabel(self.announcement_content_frame, text="", 
                                          font=("Arial", 14, "bold"), fg_color="transparent")
        self.announcement_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Content
        self.announcement_text = ctk.CTkTextbox(self.announcement_content_frame, fg_color="transparent", 
                                           height=150, wrap="word", activate_scrollbars=True)
        self.announcement_text.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Author and date
        self.announcement_footer = ctk.CTkLabel(self.announcement_content_frame, text="", 
                                           font=("Arial", 10), fg_color="transparent", text_color="gray")
        self.announcement_footer.pack(anchor="e", padx=15, pady=(5, 15))
        
        # Recent Activities
        activities_frame = ctk.CTkFrame(left_frame, fg_color="#e0e0e0", corner_radius=10)
        activities_frame.pack(fill="both", expand=True)
        
        activities_header = ctk.CTkFrame(activities_frame, fg_color="transparent", height=40)
        activities_header.pack(fill="x")
        
        activities_label = ctk.CTkLabel(activities_header, text="Recent Activities", 
                                       font=("Arial", 16, "bold"), fg_color="transparent")
        activities_label.pack(side="left", padx=20, pady=10)
        
        # Navigation buttons for activities
        activities_nav = ctk.CTkFrame(activities_header, fg_color="transparent")
        activities_nav.pack(side="right", padx=20)
        
        self.prev_activities_btn = ctk.CTkButton(activities_nav, text="◀", width=30, 
                                             fg_color="#d0d0d0", text_color="black", 
                                             corner_radius=5, command=self.prev_activities_page)
        self.prev_activities_btn.pack(side="left", padx=5)
        
        self.next_activities_btn = ctk.CTkButton(activities_nav, text="▶", width=30, 
                                             fg_color="#d0d0d0", text_color="black", 
                                             corner_radius=5, command=self.next_activities_page)
        self.next_activities_btn.pack(side="left", padx=5)
        
        # Activities content
        self.activities_content = ctk.CTkFrame(activities_frame, fg_color="white", corner_radius=5)
        self.activities_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Right section
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Current Progress Chart
        progress_frame = ctk.CTkFrame(right_frame, fg_color="#e0e0e0", corner_radius=10, border_width=1, border_color="#d0d0d0")
        progress_frame.pack(fill="x", pady=(0, 20), ipady=20)
        
        progress_label = ctk.CTkLabel(progress_frame, text="Current Progress", 
                                     font=("Arial", 16, "bold"), fg_color="transparent")
        progress_label.pack(anchor="nw", padx=20, pady=10)
        
        # Create progress chart figure
        self.create_donut_chart(progress_frame, 
                               {"Todo": 50, "Doing": 30, "DONE": 10, "Requirement": 10},
                               {"Todo": "#3483eb", "Doing": "#4dc6ff", "DONE": "#57e5a1", "Requirement": "#e5e5e5"})
        
        # Task ownership chart
        ownership_frame = ctk.CTkFrame(right_frame, fg_color="#e0e0e0", corner_radius=10, border_width=1, border_color="#d0d0d0")
        ownership_frame.pack(fill="both", expand=True)
        
        ownership_label = ctk.CTkLabel(ownership_frame, text="Each task take owner", 
                                      font=("Arial", 16, "bold"), fg_color="transparent")
        ownership_label.pack(anchor="nw", padx=20, pady=10)
        
        # Create ownership chart
        self.create_donut_chart(ownership_frame, 
                               {"Alex": 50, "D": 30, "Jon": 10, "Thun": 10},
                               {"Alex": "#3483eb", "D": "#4dc6ff", "Jon": "#57e5a1", "Thun": "#e5e5e5"})
        
        # Settings button at bottom
        settings_frame = ctk.CTkFrame(self, height=40, fg_color="transparent")
        settings_frame.pack(fill="x", side="bottom")
        
        settings_button = ctk.CTkButton(settings_frame, text="⚙️", width=30, fg_color="transparent", text_color="black")
        settings_button.pack(side="left", padx=20, pady=10)
        
        # Initialize with first announcement and activities
        self.display_announcement(0)
        self.display_activities(0)
    
    def create_donut_chart(self, parent_frame, data, colors):
        # Create a frame to hold the chart and legend
        chart_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        chart_frame.pack(fill="x", padx=10, pady=5)  # Reduced padding
    
        # Create chart on the left
        chart_left = ctk.CTkFrame(chart_frame, fg_color="transparent")
        chart_left.pack(side="left", fill="both", expand=True)
    
        fig, ax = plt.subplots(figsize=(2.5, 1.5), facecolor='#e0e0e0')  # Smaller figure size
        wedges, texts, autotexts = ax.pie(
            data.values(), 
            labels=None, 
            colors=colors.values(),
            autopct='%1.0f%%', 
            startangle=90,
            wedgeprops=dict(width=0.4),  # For donut shape
            pctdistance=0.85
        )
    
        # Make the center circle for the donut
        centre_circle = plt.Circle((0, 0), 0.3, fc='white')
        ax.add_patch(centre_circle)
    
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        plt.tight_layout()
    
        canvas = FigureCanvasTkAgg(fig, master=chart_left)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
        # Create legend on the right
        legend_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        legend_frame.pack(side="right", fill="y", padx=10)  # Reduced padding
    
        # Add items to the legend
        for key, value in data.items():
            item_frame = ctk.CTkFrame(legend_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=3, anchor="e")  # Reduced vertical spacing
        
            item_label = ctk.CTkLabel(item_frame, text=key, font=("Arial", 10))  # Smaller font size
            item_label.pack(side="left", padx=(0, 10))
        
            value_label = ctk.CTkLabel(item_frame, text=f"{value}%", font=("Arial", 10, "bold"))
            value_label.pack(side="right")

    
    def display_announcement(self, index):
        if 0 <= index < len(self.announcements):
            announcement = self.announcements[index]
            
            self.announcement_title.configure(text=announcement["title"])
            
            # Clear and update text
            self.announcement_text.delete("0.0", "end")
            self.announcement_text.insert("0.0", announcement["content"])
            
            # Update footer
            self.announcement_footer.configure(text=f"{announcement['author']} • {announcement['date']}")
            
            # Update current index
            self.current_announcement = index
            
            # Update button states
            self.prev_announcement_btn.configure(state="normal" if index > 0 else "disabled")
            self.next_announcement_btn.configure(state="normal" if index < len(self.announcements) - 1 else "disabled")
    
    def prev_announcement(self):
        if self.current_announcement > 0:
            self.display_announcement(self.current_announcement - 1)
    
    def next_announcement(self):
        if self.current_announcement < len(self.announcements) - 1:
            self.display_announcement(self.current_announcement + 1)
    
    def display_activities(self, page):
        # Clear existing activities
        for widget in self.activities_content.winfo_children():
            widget.destroy()
        
        # Calculate start and end indices
        start_idx = page * self.activities_per_page
        end_idx = min(start_idx + self.activities_per_page, len(self.activities))
        
        # Display activities for current page
        for i in range(start_idx, end_idx):
            activity = self.activities[i]
            
            # Create activity item frame
            activity_item = ctk.CTkFrame(self.activities_content, fg_color="transparent", 
                                         height=60, corner_radius=0)
            activity_item.pack(fill="x", padx=10, pady=5)
            activity_item.pack_propagate(False)
            
            # Add separator except for first item
            if i > start_idx:
                separator = ctk.CTkFrame(activity_item, fg_color="#e5e5e5", height=1)
                separator.pack(fill="x", pady=(0, 5))
            
            # User and action
            user_label = ctk.CTkLabel(activity_item, text=activity["user"], 
                                     font=("Arial", 12, "bold"), text_color="#3483eb")
            user_label.pack(anchor="w", padx=5, pady=(5, 0))
            
            action_label = ctk.CTkLabel(activity_item, text=activity["action"], 
                                       font=("Arial", 11))
            action_label.pack(anchor="w", padx=5,pady=(5, 0))
            
            # Timestamp
            time_label = ctk.CTkLabel(activity_item, text=activity["time"], 
                                     font=("Arial", 10), text_color="gray")
            time_label.pack(anchor="w", padx=5, pady=(5, 0))
        
        # Update current page
        self.current_activity_page = page
        
        # Update button states
        self.prev_activities_btn.configure(state="normal" if page > 0 else "disabled")
        self.next_activities_btn.configure(state="normal" if end_idx < len(self.activities) else "disabled")
        
        # Show "Show More" button if there are more pages
        if end_idx < len(self.activities):
            show_more_btn = ctk.CTkButton(self.activities_content, text="Show More", 
                                         fg_color="#3483eb", corner_radius=5,
                                         command=self.next_activities_page)
            show_more_btn.pack(pady=10)
    
    def prev_activities_page(self):
        if self.current_activity_page > 0:
            self.display_activities(self.current_activity_page - 1)
    
    def next_activities_page(self):
        total_pages = (len(self.activities) + self.activities_per_page - 1) // self.activities_per_page
        if self.current_activity_page < total_pages - 1:
            self.display_activities(self.current_activity_page + 1)

if __name__ == "__main__":
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Create the main window
    root = ctk.CTk()
    root.geometry("1200x800")
    root.title("CollabDesk Dashboard")
    
    # Create a simple configuration object
    config = {}
    
    # Create and pack the dashboard
    app = Dashboard(root, config)
    app.pack(fill="both", expand=True)
    
    # Start the main event loop
    root.mainloop()