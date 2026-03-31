import tkinter as tk
from tkinter import ttk
import random

class DeltaHUD:

    def __init__(self, root):
        self.root = root
        self.root.title("DELTA HUD")
        self.root.geometry("420x300")
        self.root.configure(bg="black")

        title = tk.Label(
            root,
            text="DELTA ANALYSIS HUD",
            fg="#00ffcc",
            bg="black",
            font=("Consolas", 16, "bold")
        )
        title.pack(pady=10)

        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(pady=10)

        # Probability bars
        self.options = ["Proceed", "Wait", "Abort"]

        self.bars = {}
        for option in self.options:

            row = tk.Frame(self.frame, bg="black")
            row.pack(fill="x", pady=4)

            label = tk.Label(
                row,
                text=option,
                fg="white",
                bg="black",
                width=10,
                anchor="w"
            )
            label.pack(side="left")

            bar = ttk.Progressbar(
                row,
                orient="horizontal",
                length=200,
                mode="determinate"
            )
            bar.pack(side="left", padx=5)

            percent = tk.Label(
                row,
                text="0%",
                fg="#00ffcc",
                bg="black"
            )
            percent.pack(side="left")

            self.bars[option] = (bar, percent)

        # Recommendation display
        self.recommendation = tk.Label(
            root,
            text="Recommendation: --",
            fg="yellow",
            bg="black",
            font=("Consolas", 12, "bold")
        )
        self.recommendation.pack(pady=20)

        # Manual update button (for testing)
        btn = tk.Button(
            root,
            text="New Information",
            command=self.update_analysis
        )
        btn.pack()

    def update_analysis(self):
        """
        Simulates Delta receiving new information
        and recalculating probabilities
        """

        probs = {
            "Proceed": random.randint(0,100),
            "Wait": random.randint(0,100),
            "Abort": random.randint(0,100)
        }

        best = max(probs, key=probs.get)

        for option, value in probs.items():
            bar, label = self.bars[option]
            bar["value"] = value
            label["text"] = f"{value}%"

        self.recommendation.config(
            text=f"Recommendation: {best}"
        )