import sys
from ui.delta_engine import analyze_scenario
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QLabel, QProgressBar
)
from PyQt6.QtGui import QFont, QMovie
from PyQt6.QtCore import Qt, QTimer

from ui.chat import chat_with_delta


class DeltaUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delta AI")
        self.setGeometry(100, 100, 500, 520)

        self.scenario_active = False  # Tracks if a scenario is in progress

        layout = QVBoxLayout()

        # -------------------
        # DELTA GIF
        # -------------------
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie = QMovie("DELTA.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.frameChanged.connect(self.check_last_frame)
        self.movie.start()

        # -------------------
        # Boot log
        # -------------------
        self.boot_log = QLabel("")
        self.boot_log.setFont(QFont("Consolas", 10))
        self.boot_log.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -------------------
        # HUD TITLE
        # -------------------
        self.hud_title = QLabel("Delta Probability Analysis")
        self.hud_title.setFont(QFont("Consolas", 11))
        self.hud_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hud_title.hide()

        # -------------------
        # HUD PROBABILITY BARS
        # -------------------
        self.proceed_label = QLabel("Proceed")
        self.proceed_bar = QProgressBar()
        self.wait_label = QLabel("Wait")
        self.wait_bar = QProgressBar()
        self.abort_label = QLabel("Abort")
        self.abort_bar = QProgressBar()

        for widget in [self.proceed_label, self.proceed_bar,
                       self.wait_label, self.wait_bar,
                       self.abort_label, self.abort_bar]:
            widget.hide()

        # -------------------
        # HUD RECOMMENDATION
        # -------------------
        self.recommendation = QLabel("Recommendation: --")
        self.recommendation.setFont(QFont("Consolas", 11))
        self.recommendation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recommendation.hide()

        # -------------------
        # Chat window
        # -------------------
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setFont(QFont("Segoe UI", 11))
        self.chat.setVisible(False)

        # -------------------
        # Input box
        # -------------------
        self.input = QLineEdit()
        self.input.setPlaceholderText("Message Delta...")
        self.input.returnPressed.connect(self.send_message)
        self.input.setVisible(False)

        # -------------------
        # Layout
        # -------------------
        layout.addWidget(self.gif_label)
        layout.addWidget(self.boot_log)
        layout.addWidget(self.hud_title)

        layout.addWidget(self.proceed_label)
        layout.addWidget(self.proceed_bar)
        layout.addWidget(self.wait_label)
        layout.addWidget(self.wait_bar)
        layout.addWidget(self.abort_label)
        layout.addWidget(self.abort_bar)

        layout.addWidget(self.recommendation)
        layout.addWidget(self.chat)
        layout.addWidget(self.input)

        self.setLayout(layout)

        # -------------------
        # Dark UI styling
        # -------------------
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f0f;
                color: #4EC9B0;
            }

            QTextEdit {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 10px;
                color: white;
            }

            QLineEdit {
                background-color: #333333;
                border-radius: 8px;
                padding: 10px;
                border: none;
                color: white;
            }

            QProgressBar {
                background-color: #1e1e1e;
                border-radius: 5px;
                text-align: center;
                color: white;
            }

            QProgressBar::chunk {
                background-color: #4EC9B0;
            }
        """)

        # -------------------
        # Boot sequence
        # -------------------
        self.boot_messages = [
            "Initializing reasoning engine...",
            "Loading probability module...",
            "Loading memory system...",
            "Connecting interface...",
            "Delta ready."
        ]
        self.boot_index = 0
        QTimer.singleShot(1500, self.boot_step)

    # -------------------
    # Stop GIF after one play
    # -------------------
    def check_last_frame(self, frame_number):
        if self.movie.frameCount() > 0:
            if frame_number == self.movie.frameCount() - 1:
                self.movie.stop()
                self.gif_label.hide()

    # -------------------
    # Boot sequence
    # -------------------
    def boot_step(self):
        if self.boot_index < len(self.boot_messages):
            current = self.boot_log.text()
            new_line = self.boot_messages[self.boot_index]
            self.boot_log.setText(current + "\n" + new_line)
            self.boot_index += 1
            QTimer.singleShot(800, self.boot_step)
        else:
            self.boot_complete()

    def boot_complete(self):
        self.boot_log.hide()
        self.hud_title.show()
        for widget in [self.proceed_label, self.proceed_bar,
                       self.wait_label, self.wait_bar,
                       self.abort_label, self.abort_bar,
                       self.recommendation]:
            widget.show()

        self.chat.setVisible(True)
        self.input.setVisible(True)
        self.chat.append("<b>Delta:</b> System initialized. How can I assist you?")

    # -------------------
    # Reset HUD
    # -------------------
    def reset_hud(self):
        for bar in [self.proceed_bar, self.wait_bar, self.abort_bar]:
            bar.setValue(0)
        self.proceed_label.setText("Proceed")
        self.wait_label.setText("Wait")
        self.abort_label.setText("Abort")
        self.recommendation.setText("Recommendation: --")

    # -------------------
    # Update HUD
    # -------------------
    def update_hud(self, user_text, response):
        probs = analyze_scenario(user_text, response)

        proceed = probs["Proceed"]
        wait = probs["Wait"]
        abort = probs["Abort"]

        self.proceed_bar.setValue(proceed)
        self.wait_bar.setValue(wait)
        self.abort_bar.setValue(abort)

        self.proceed_label.setText(f"Proceed ({proceed}%)")
        self.wait_label.setText(f"Wait ({wait}%)")
        self.abort_label.setText(f"Abort ({abort}%)")

        best = max(probs, key=probs.get)
        self.recommendation.setText(f"Recommendation: {best}")

    # -------------------
    # Chat system
    # -------------------
    def send_message(self):
        user_text = self.input.text()
        if not user_text:
            return

        self.chat.append(f"<b>You:</b> {user_text}")
        self.input.clear()
        response = chat_with_delta(user_text)
        self.chat.append(f"<span style='color:#4EC9B0'><b>Delta:</b> {response}</span><br>")

        # -------------------
        # Scenario detection
        # -------------------
        new_scenario_keywords = [
            "new scenario", "let's run a scenario", "start scenario", "let's run a new scenario",
        ]
        scenario_keywords = [
            "scenario", "if", "what if", "suppose",
            "should", "would", "could",
            "fire", "shooter", "danger",
            "emergency", "attack", "run", "leave", "stay"
        ]

        user_lower = user_text.lower()

        if any(word in user_lower for word in new_scenario_keywords):
            # Reset HUD for new scenario
            self.reset_hud()
            self.scenario_active = True
            self.update_hud(user_text, response)
        elif self.scenario_active or any(word in user_lower for word in scenario_keywords):
            # Continue current scenario
            self.update_hud(user_text, response)
        else:
            # No scenario, reset HUD
            self.scenario_active = False
            self.reset_hud()


# -------------------
# Run application
# -------------------
app = QApplication(sys.argv)
window = DeltaUI()
window.show()
sys.exit(app.exec())