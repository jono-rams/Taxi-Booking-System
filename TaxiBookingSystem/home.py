from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QPalette, QBrush
from login import LoginWidget
from register import RegisterWidget


class HomeWidget(QWidget):

    # Function to display a message box with "Hello World!" content
    @staticmethod
    def display_msg():
        QMessageBox.information(None, "Message", "Hello World!")

    # Function to open a login dialog
    def open_login_dialog(self):
        self.login_dialog = LoginWidget()
        self.login_dialog.show()

    def open_register_dialog(self):
        self.register_dialog = RegisterWidget(home_widget=self)
        self.register_dialog.show()

    def scale_background_image(self):
        scaled_bg = self.background_image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        palette = self.palette()
        palette.setBrush(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QBrush(scaled_bg))
        self.setPalette(palette)

    def __init__(self, app):
        super().__init__()

        self.login_dialog = None
        self.register_dialog = None

        # Create Main Window
        self.setWindowTitle("Taxi Booking System")

        # Create Background Image
        self.background_image = QPixmap("assets/images/bg.jpg")
        self.scale_background_image()
        self.original_aspect_ratio = self.background_image.width() / self.background_image.height()

        # Allow resizing but maintain aspect ratio
        self.setFixedSize(self.background_image.size())
        self.setMinimumSize(self.background_image.size() / 2)  # Set minimum size

        # Create Vertical Layout
        v_layout = QVBoxLayout()

        # Create Horizontal Layout for Buttons
        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        # Add Horizontal Layout to Vertical Layout
        v_layout.addLayout(h_layout)

        # Create Login Button
        login_btn = QPushButton("Login")
        login_btn.setMinimumSize(250, 62)
        login_btn.setMaximumSize(500, 125)
        login_btn.setFont(QFont("TimesNewRoman", 16))
        login_btn.clicked.connect(self.open_login_dialog)

        # Add Login Button to Horizontal Layout
        h_layout.addWidget(login_btn)

        # Create Register Button
        register_btn = QPushButton("Register")
        register_btn.setMinimumSize(250, 62)
        register_btn.setMaximumSize(500, 125)
        register_btn.setFont(QFont("TimesNewRoman", 16))
        register_btn.clicked.connect(self.open_register_dialog)

        # Add Register Button to Horizontal Layout
        h_layout.addWidget(register_btn)

        # Create Exit Button
        exit_btn = QPushButton("Exit")
        exit_btn.setMinimumSize(250, 62)
        exit_btn.setMaximumSize(500, 125)
        exit_btn.setFont(QFont("TimesNewRoman", 16))
        exit_btn.clicked.connect(app.quit)

        # Add Exit Button to Horizontal Layout
        h_layout.addWidget(exit_btn)

        # Add Vertical Layout to Main Window
        self.setLayout(v_layout)

    def resizeEvent(self, event):
        self.scale_background_image()
        new_width = event.size().width()
        new_height = int(new_width / self.original_aspect_ratio)
        self.resize(new_width, new_height)
