import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel
from PyQt6.QtGui import QFont, QMovie
from PyQt6.QtCore import Qt, QTimer
from chat import chat_with_delta


class DeltaUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delta AI")
        self.setGeometry(100, 100, 500, 350)

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

        layout.addWidget(self.gif_label)
        layout.addWidget(self.boot_log)
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
    # Stop GIF after 1 play
    # -------------------

    def check_last_frame(self, frame_number):

        if self.movie.frameCount() > 0:
            if frame_number == self.movie.frameCount() - 1:
                self.movie.stop()
                self.gif_label.hide()

    # -------------------
    # Boot text sequence
    # -------------------

    def boot_step(self):

        if self.boot_index < len(self.boot_messages):

            current_text = self.boot_log.text()
            new_line = self.boot_messages[self.boot_index]

            self.boot_log.setText(current_text + "\n" + new_line)

            self.boot_index += 1

            QTimer.singleShot(800, self.boot_step)

        else:
            self.boot_complete()

    # -------------------
    # Boot finished
    # -------------------

    def boot_complete(self):

        self.boot_log.hide()

        self.chat.setVisible(True)
        self.input.setVisible(True)

        self.chat.append("<b>Delta:</b> System initialized. How can I assist you?")

    # -------------------
    # Chat function
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
# Run application
# -------------------

app = QApplication(sys.argv)

window = DeltaUI()
window.show()

sys.exit(app.exec())