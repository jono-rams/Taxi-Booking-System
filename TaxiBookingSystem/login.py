from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginWidget(QWidget):

    # Function to display a message box with "Hello World!" content
    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email:
            QMessageBox.warning(None, "Error", "Please enter an email address.")
            return

        if not password:
            QMessageBox.warning(None, "Error", "Please enter a password.")
            return

        # TODO: Check email and password combination against database
        QMessageBox.information(None, "Login Successful", "Welcome")

    def __init__(self):
        super().__init__()

        # Create Main Window
        self.setWindowTitle("Login")
        self.setFixedSize(600, 450)

        # Create Vertical Layout
        v_layout = QVBoxLayout()

        # Create Label Widget
        label = QLabel("Login to the Taxi Booking System!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(20)
        font.setFamily("TimesNewRoman")
        label.setFont(font)
        label.setFixedHeight(30)

        # Add Label to Vertical Layout
        v_layout.addWidget(label)

        # Create Horizontal Layout for Email
        email_layout = QHBoxLayout()

        # Create Email Textbox
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        # Add Email widgets to Layout
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)

        # Create Horizontal Layout for Password
        password_layout = QHBoxLayout()

        # Create Password Textbox
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Add Password widgets to Layout
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)

        # Create Vertical Layout for Fields
        fields_layout = QVBoxLayout()
        fields_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add Email and Password Layouts to Fields Layout
        fields_layout.addLayout(email_layout)
        fields_layout.addLayout(password_layout)

        # Add Fields Layout to Vertical Layout
        v_layout.addLayout(fields_layout)

        # Create Horizontal Layout for Buttons
        buttons_layout = QHBoxLayout()

        # Create Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)

        # Add Login Button to Button Layout
        buttons_layout.addWidget(self.login_btn)

        # Create Close Button
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        # Add Close Button to Button Layout
        buttons_layout.addWidget(self.close_btn)

        # Add Buttons to Vertical Layout
        v_layout.addLayout(buttons_layout)

        # Set Vertical Layout to Main Window
        self.setLayout(v_layout)
