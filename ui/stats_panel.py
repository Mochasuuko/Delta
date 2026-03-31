from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class StatsPanel(QWidget):

    def __init__(self, stats):

        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("DELTA ANALYSIS")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        layout.addWidget(title)

        for key, value in stats.items():

            label = QLabel(f"{key}: {value}")
            label.setStyleSheet("font-size:14px;")

            layout.addWidget(label)

        layout.addStretch()

        self.setLayout(layout)