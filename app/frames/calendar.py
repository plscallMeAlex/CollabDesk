import customtkinter as ctk
from datetime import datetime, timedelta
import requests
from app.frames.frame import Frame
import calendar


class TaskCalendarWidget(Frame):
    def __init__(self, master, configuration, guildId=None, **kwargs):
        super().__init__(master, configuration, guildId, **kwargs)

        # Set initial date to current time
        self.current_date = datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month
        self._configuration = configuration

        # Tasks and events storage with mock data based on current date
        current_day = self.current_date.day
        self.tasks = self.__formating_tasks_data()

        # Configure grid to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Callbacks
        self.on_day_click_callback = None

        # Create the calendar layout
        self.create_widgets()

    def __fetch_tasks(self):
        try:
            params = {
                "guild_id": self._guildId,
            }
            response = requests.get(
                f"{self._configuration.api_url}/tasks/in_guild", params=params
            )
            return response.json()
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return []

    def __formating_tasks_data(self):
        tasks = self.__fetch_tasks()
        formatted_tasks = []
        current_date = datetime.now()

        for task in tasks:
            due_date = self.__format_to_datetime(task["due_date"])
            if due_date is None:
                continue

            # Calculate days until due
            days_until_due = (due_date - current_date).days

            # Determine priority based on days until due
            if days_until_due < 0:  # Overdue
                priority = "high"
                color = "#ff7f7f"  # Red
            elif days_until_due <= 1:  # Due today or tomorrow
                priority = "high"
                color = "#ff7f7f"  # Red
            elif days_until_due <= 3:  # Due within 3 days
                priority = "medium"
                color = "#ffd700"  # Yellow
            else:  # Due in more than 3 days
                priority = "low"
                color = "#90EE90"  # Green

            task_details = {
                "title": task["title"],
                "priority": priority,
                "color": color,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "day": due_date.day,
                "month": due_date.month,
                "year": due_date.year,
            }
            formatted_tasks.append(task_details)

        return formatted_tasks

    def __format_to_datetime(self, date):
        if date is None:
            return None
        try:
            # Handle different date formats
            if "." in date:  # Format with milliseconds
                return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:  # Format without milliseconds
                return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as e:
            print(f"Error parsing date {date}: {e}")
            return None

    def set_on_day_click(self, callback):
        """Set callback function for day click events"""
        self.on_day_click_callback = callback

    def set_guildId(self, guildId):
        """Set the guild ID for the calendar"""
        self._guildId = guildId
        # Fetch tasks for the new guild ID
        self.tasks = self.__formating_tasks_data()
        self.update_calendar()  # Update the calendar display

    def create_widgets(self):
        # Create header with month/year and navigation
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)

        # Month and year label
        month_name = calendar.month_name[self.month]
        self.header_label = ctk.CTkLabel(
            header_frame, text=f"{month_name} {self.year}", font=("Arial", 18, "bold")
        )
        self.header_label.grid(row=0, column=0, sticky="w", padx=10)

        # Navigation buttons
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="e", padx=10)

        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="<",
            width=30,
            corner_radius=5,
            fg_color="transparent",
            text_color="black",
            hover_color="#e0e0e0",
            command=self.prev_month,
        )
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = ctk.CTkButton(
            nav_frame,
            text=">",
            width=30,
            corner_radius=5,
            fg_color="transparent",
            text_color="black",
            hover_color="#e0e0e0",
            command=self.next_month,
        )
        self.next_btn.pack(side="left", padx=5)

        # Main calendar container
        main_calendar = ctk.CTkFrame(
            self, fg_color="transparent", border_width=1, border_color="#dee2e6"
        )
        main_calendar.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Configure the main calendar container to expand
        for i in range(7):  # 7 columns for days
            main_calendar.grid_columnconfigure(i, weight=1)
        for i in range(7):  # 1 row for headers + 6 rows for days (max needed)
            main_calendar.grid_rowconfigure(i, weight=1)

        # Create weekday headers
        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        # Grid for days of week headers
        for col, day in enumerate(weekdays):
            day_label = ctk.CTkLabel(
                main_calendar, text=day, font=("Arial", 12, "bold"), anchor="center"
            )
            day_label.grid(row=0, column=col, padx=1, pady=3, sticky="nsew")

        # Store reference to calendar frame for updates
        self.calendar_frame = main_calendar

        # Populate calendar
        self.update_calendar()

    def update_calendar(self):
        # Clear existing calendar days (except headers)
        for widget in self.calendar_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        # Update header label
        month_name = calendar.month_name[self.month]
        self.header_label.configure(text=f"{month_name} {self.year}")

        # Get first day of month and number of days
        first_day = datetime(self.year, self.month, 1)
        days_in_month = calendar.monthrange(self.year, self.month)[1]

        # Adjust first weekday (0 is Monday in our calendar)
        first_weekday = first_day.weekday()  # 0 = Monday, 6 = Sunday

        # Get days from previous month
        if first_weekday > 0:
            prev_month = self.month - 1 if self.month > 1 else 12
            prev_year = self.year if self.month > 1 else self.year - 1
            prev_days = calendar.monthrange(prev_year, prev_month)[1]

        # Populate calendar grid
        day = 1
        for row in range(1, 7):  # Start from row 1 (after headers)
            if day > days_in_month and row > 1:
                break

            for col in range(7):  # 7 days per week
                if row == 1 and col < first_weekday:
                    # Previous month days
                    prev_day = prev_days - first_weekday + col + 1
                    day_frame = self.create_day_cell(prev_day, False)
                    day_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                elif day <= days_in_month:
                    # Current month days
                    # Filter tasks for this day
                    day_tasks = [
                        task
                        for task in self.tasks
                        if task["day"] == day
                        and task["month"] == self.month
                        and task["year"] == self.year
                    ]

                    # Create day cell
                    day_frame = self.create_day_cell(
                        day,
                        True,
                        has_tasks=len(day_tasks) > 0,
                        tasks=day_tasks,
                        is_today=(
                            day == self.current_date.day
                            and self.month == self.current_date.month
                            and self.year == self.current_date.year
                        ),
                    )
                    day_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                    day += 1
                else:
                    # Next month days
                    next_day = day - days_in_month
                    day_frame = self.create_day_cell(next_day, False)
                    day_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                    day += 1

    def create_day_cell(
        self, day, current_month, has_tasks=False, tasks=None, is_today=False
    ):
        # Create frame for the day cell
        cell_frame = ctk.CTkFrame(
            self.calendar_frame,
            corner_radius=0,
            fg_color="#f8f9fa" if not current_month else ("white"),
            border_width=1,
            border_color="#dee2e6",
        )

        # Configure cell to fill space
        cell_frame.grid_columnconfigure(0, weight=1)

        # Today indicator
        if is_today:
            day_container = ctk.CTkFrame(
                cell_frame, corner_radius=15, fg_color="#007bff", width=30, height=30
            )
            day_container.place(x=5, y=5)

            day_label = ctk.CTkLabel(
                day_container,
                text=str(day),
                text_color="white",
                font=("Arial", 12, "bold"),
                width=30,
                height=30,
            )
            day_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # Day number label
            day_label = ctk.CTkLabel(
                cell_frame,
                text=str(day),
                text_color="gray" if not current_month else "black",
                font=("Arial", 12, "bold" if current_month else "normal"),
                anchor="nw",
            )
            day_label.place(x=5, y=5)

        # Add event container that will expand with the cell
        task_container = ctk.CTkFrame(
            cell_frame, corner_radius=0, fg_color="transparent"
        )
        task_container.place(x=0, y=30, relwidth=1, relheight=0.8)

        # Make the cell clickable if it's in the current month
        if current_month:
            cell_frame.bind("<Button-1>", lambda e, d=day: self._on_day_click(d))
            day_label.bind("<Button-1>", lambda e, d=day: self._on_day_click(d))
            task_container.bind("<Button-1>", lambda e, d=day: self._on_day_click(d))

        # Add tasks if present
        if has_tasks and current_month and tasks:
            self._display_tasks(task_container, tasks)

        return cell_frame

    def _display_tasks(self, container, tasks):
        """Display tasks in the container"""
        # Create a scrollable frame if many tasks
        if len(tasks) > 3:
            scrollable_frame = ctk.CTkScrollableFrame(
                container,
                fg_color="transparent",
                scrollbar_button_color="#dee2e6",
                scrollbar_button_hover_color="#ced4da",
            )
            scrollable_frame.pack(fill="both", expand=True, padx=2, pady=2)
            task_frame = scrollable_frame
        else:
            task_frame = container

        # Add tasks
        for i, task in enumerate(tasks):
            task_bg = ctk.CTkFrame(
                task_frame, corner_radius=3, fg_color=task["color"], height=20
            )
            task_bg.pack(fill="x", expand=False, padx=2, pady=1)

            # Add task text
            task_text = ctk.CTkLabel(
                task_bg,
                text=task["title"],
                text_color="black",
                font=("Arial", 10),
                anchor="w",
                padx=5,
            )
            task_text.pack(fill="x", expand=True)

            # Make task clickable to edit
            task_bg.bind(
                "<Button-1>", lambda e, t=task, idx=i: self._on_task_click(t, idx)
            )
            task_text.bind(
                "<Button-1>", lambda e, t=task, idx=i: self._on_task_click(t, idx)
            )

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()


# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Task Management Calendar")
    app.geometry("800x600")

    # Configure the main window to expand
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # Create the calendar with specified year and month
    calendar_widget = TaskCalendarWidget(app, year=2025, month=5)
    calendar_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Example of setting a callback for day clicks
    def on_day_clicked(day, month, year):
        print(f"Day clicked: {day}/{month}/{year}")

    calendar_widget.set_on_day_click(on_day_clicked)

    app.mainloop()
