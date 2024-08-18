import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scroll Area Example")
        self.setFixedSize(800, 450)
        self.layout = QVBoxLayout(self)

        # Scroll Area to hold the content
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        # Add a few entries as examples
        for i in range(15):
            entry_layout = QHBoxLayout()
            label = QLabel(f"Booking {i}")
            entry_layout.addWidget(label)

            button1 = QPushButton("View")
            button1.setFixedSize(100, 50)
            button2 = QPushButton("Cancel")
            button2.setFixedSize(100, 50)
            entry_layout.addWidget(button1)
            entry_layout.addWidget(button2)

            scroll_layout.addLayout(entry_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Add close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedSize(100, 50)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())