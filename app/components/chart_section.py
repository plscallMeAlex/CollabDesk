import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches


class ChartSection(ctk.CTkFrame):
    def __init__(self, master, title, data, colors):
        super().__init__(
            master,
            fg_color="#e0e0e0",
            corner_radius=10,
            border_width=1,
            border_color="#d0d0d0",
        )

        self.title = title
        self.data = data
        self.colors = colors

        # Set a fixed size for the frame to ensure consistent sizing
        self.configure(width=400, height=300)
        self.grid_propagate(False)  # Prevent resizing based on content

        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=("Inter", 16, "bold"),
            fg_color="transparent",
        )
        self.title_label.pack(anchor="nw", padx=20, pady=10)

        # Create chart and legend
        self.create_donut_chart()

    def create_donut_chart(self):
        # Create a frame to hold the chart and legend
        chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create chart on the left
        chart_left = ctk.CTkFrame(chart_frame, fg_color="transparent")
        chart_left.pack(side="left", fill="both", expand=True)

        # Use fixed figsize regardless of data content
        fig, ax = plt.subplots(figsize=(4, 4), facecolor="#e0e0e0")

        # Only create the pie chart if there's data
        if self.data:
            wedges, texts, autotexts = ax.pie(
                self.data.values(),
                labels=None,
                colors=self.colors.values(),
                autopct="%1.0f%%",
                startangle=90,
                wedgeprops=dict(width=0.4),  # For donut shape
                pctdistance=0.85,
                textprops={"fontsize": 9},  # Consistent text size
            )

            # Style the percentage text
            for autotext in autotexts:
                autotext.set_color("black")
                autotext.set_fontweight("bold")

        # Make the center circle for the donut
        centre_circle = plt.Circle((0, 0), 0.3, fc="white")
        ax.add_patch(centre_circle)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis("equal")

        # Remove padding around the plot
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        canvas = FigureCanvasTkAgg(fig, master=chart_left)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Create legend on the right
        legend_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        legend_frame.pack(side="right", fill="y", padx=10)

        # Add items to the legend
        for key, value in self.data.items():
            item_frame = ctk.CTkFrame(legend_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=3, anchor="e")

            # Create a color indicator
            color_indicator = ctk.CTkFrame(
                item_frame,
                width=10,
                height=10,
                fg_color=self.colors.get(key, "#cccccc"),
                corner_radius=2,
            )
            color_indicator.pack(side="left", padx=(0, 5))

            item_label = ctk.CTkLabel(item_frame, text=key, font=("Inter", 10))
            item_label.pack(side="left", padx=(0, 10))

            value_label = ctk.CTkLabel(
                item_frame, text=f"{value}%", font=("Inter", 10, "bold")
            )
            value_label.pack(side="right")
