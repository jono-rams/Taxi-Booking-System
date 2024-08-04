from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from login import LoginWidget


class HomeWidget(QWidget):

    # Function to display a message box with "Hello World!" content
    @staticmethod
    def display_msg():
        QMessageBox.information(None, "Message", "Hello World!")

    # Function to open a login dialog
    def open_login_dialog(self):
        self.login_dialog = LoginWidget()
        self.login_dialog.show()

    def __init__(self, app):
        super().__init__()

        # Create Main Window
        self.setWindowTitle("Taxi Booking System")
        self.setFixedSize(800, 600)

        # Create Background Image
        background_image = QLabel(self)
        background_image.setGeometry(0, 0, 800, 600)
        background_image.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        background_image.setPixmap(QPixmap("assets/images/bg.jpg"))

        # Create Vertical Layout
        v_layout = QVBoxLayout()

        # Create Label Widget
        label = QLabel("Welcome to the Taxi Booking System!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(20)
        font.setFamily("TimesNewRoman")
        label.setFont(font)

        # Add Label to Vertical Layout
        v_layout.addWidget(label)

        # Create Horizontal Layout for Buttons
        h_layout = QHBoxLayout()

        # Add Horizontal Layout to Vertical Layout
        v_layout.addLayout(h_layout)

        # Create Login Button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.open_login_dialog)

        # Add Login Button to Horizontal Layout
        h_layout.addWidget(login_btn)

        # Create Register Button
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.display_msg)

        # Add Register Button to Horizontal Layout
        h_layout.addWidget(register_btn)

        # Create Exit Button
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(app.quit)

        # Add Exit Button to Horizontal Layout
        h_layout.addWidget(exit_btn)

        # Add Vertical Layout to Main Window
        self.setLayout(v_layout)
