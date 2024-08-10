from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from connection import Database


class RegisterWidget(QWidget):

    def handle_register(self):
        self.db.connect("db/test.db")
        email: str = self.email_input.text()
        password: str = self.password_input.text()

        if not email:
            QMessageBox.warning(None, "Error", "Please enter an email address.")
            return

        if not password:
            QMessageBox.warning(None, "Error", "Please enter a password.")
            return

        # Check email and password combination against database
        register_query = "INSERT INTO users (email, password) VALUES (?, ?)"
        reg_data = (email, password)

        results = self.db.insert_data(query=register_query, data=reg_data)

        self.db.close_connection()

        if not results:
            QMessageBox.warning(None, "Error", "Unable to register")
        else:
            QMessageBox.information(None, "Successfully Registered", "Please login on the login page.")
            self.home.open_login_dialog()
            self.close()

    def __init__(self, home_widget):
        super().__init__()

        self.db = Database()
        self.home = home_widget

        # Create Main Window
        self.setWindowTitle("Login")
        self.setFixedSize(600, 450)

        # Create Vertical Layout
        v_layout = QVBoxLayout()

        # Create Label Widget
        label = QLabel("Register for the Taxi Booking System!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(18)
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
        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.handle_register)

        # Add Login Button to Button Layout
        buttons_layout.addWidget(self.register_btn)

        # Create Close Button
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        # Add Close Button to Button Layout
        buttons_layout.addWidget(self.close_btn)

        # Add Buttons to Vertical Layout
        v_layout.addLayout(buttons_layout)

        # Set Vertical Layout to Main Window
        self.setLayout(v_layout)
