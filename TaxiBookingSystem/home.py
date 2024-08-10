from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt, QSize
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

    def calculate_new_size(self, proposed_size):
        proposed_aspect_ratio = proposed_size.width() / proposed_size.height()

        if proposed_aspect_ratio > self.original_aspect_ratio:
            # Window is wider than the original aspect ratio, so constrain by height
            new_height = proposed_size.height()
            new_width = int(new_height * self.original_aspect_ratio)
        else:
            # Window is taller or matches the original aspect ratio, so constrain by width
            new_width = proposed_size.width()
            new_height = int(new_width / self.original_aspect_ratio)

        return QSize(new_width, new_height)

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
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumSize(250, 62)
        self.login_btn.setMaximumSize(500, 125)
        self.login_btn.setFont(QFont("TimesNewRoman", 16))
        self.login_btn.clicked.connect(self.open_login_dialog)
        self.login_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add Login Button to Horizontal Layout
        h_layout.addWidget(self.login_btn)

        # Create Register Button
        self.register_btn = QPushButton("Register")
        self.register_btn.setMinimumSize(250, 62)
        self.register_btn.setMaximumSize(500, 125)
        self.register_btn.setFont(QFont("TimesNewRoman", 16))
        self.register_btn.clicked.connect(self.open_register_dialog)
        self.register_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add Register Button to Horizontal Layout
        h_layout.addWidget(self.register_btn)

        # Create Exit Button
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setMinimumSize(250, 62)
        self.exit_btn.setMaximumSize(500, 125)
        self.exit_btn.setFont(QFont("TimesNewRoman", 16))
        self.exit_btn.clicked.connect(app.quit)
        self.exit_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add Exit Button to Horizontal Layout
        h_layout.addWidget(self.exit_btn)

        # Add Vertical Layout to Main Window
        self.setLayout(v_layout)

    def resizeEvent(self, event):
        new_size = self.calculate_new_size(event.size())
        self.resize(new_size)
        self.scale_background_image()
        button_size = self.calculate_button_size()

        self.login_btn.setFixedSize(button_size)
        self.register_btn.setFixedSize(button_size)
        self.exit_btn.setFixedSize(button_size)

    def calculate_button_size(self):
        # Calculate desired button size based on window size and aspect ratio
        window_width = self.width()
        window_height = self.height()

        # Adjust these factors to control the button's relative size
        width_factor = 0.25  # Button width is 25% of window width
        height_factor = 0.3  # Button height is 30% of window height

        desired_width = int(window_width * width_factor)
        desired_height = int(window_height * height_factor)

        aspect_ratio = self.login_btn.width() / self.login_btn.height()  # Original aspect ratio
        if desired_width / desired_height > aspect_ratio:
            desired_width = int(desired_height * aspect_ratio)
        else:
            desired_height = int(desired_width / aspect_ratio)

        return QSize(desired_width, desired_height)
