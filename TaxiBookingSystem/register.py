from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from connection import Database


class RegisterWidget(QWidget):

    def handle_register(self):
        db = Database()
        db.connect(self.db_path)

        # Retrieve input values
        name: str = self.name_input.text()
        address: str = self.address_input.text()
        email: str = self.email_input.text()
        phoneno: str = self.phone_input.text()
        password: str = self.password_input.text()

        # Validate inputs
        if not name:
            QMessageBox.warning(None, "Error", "Please enter your name.")
            return

        if not address:
            QMessageBox.warning(None, "Error", "Please enter your address.")
            return

        if not email:
            QMessageBox.warning(None, "Error", "Please enter an email address.")
            return

        if not phoneno:
            QMessageBox.warning(None, "Error", "Please enter your phone number.")
            return

        if not password:
            QMessageBox.warning(None, "Error", "Please enter a password.")
            return

        # Create Insert statement
        register_query = "INSERT INTO customer (name, address, email, phoneno, password) VALUES (?, ?, ?, ?, ?)"
        reg_data = (name, address, email, phoneno, password)

        results = self.db.insert_data(query=register_query, data=reg_data)  # Runs insert statement

        self.db.close_connection()  # Close database connection

        # Error handling
        if not results:
            QMessageBox.warning(None, "Error", "Unable to register")
        else:
            QMessageBox.information(None, "Successfully Registered", "Please login on the login page.")
            self.home.open_login_dialog()
            self.close()

    def __init__(self, home_widget, db_path):
        super().__init__()

        self.db_path = db_path
        self.home = home_widget

        # Create Main Window
        self.setWindowTitle("Register")
        self.setFixedSize(600, 500)  # Increased size to accommodate new fields

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

        # Create Layout for Input Fields
        fields_layout = QVBoxLayout()
        fields_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create and add Name input field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        fields_layout.addLayout(name_layout)

        # Create and add Address input field
        address_layout = QHBoxLayout()
        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)
        fields_layout.addLayout(address_layout)

        # Create and add Email input field
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        fields_layout.addLayout(email_layout)

        # Create and add Phone Number input field
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        fields_layout.addLayout(phone_layout)

        # Create and add Password input field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        fields_layout.addLayout(password_layout)

        # Add Fields Layout to Vertical Layout
        v_layout.addLayout(fields_layout)

        # Create Horizontal Layout for Buttons
        buttons_layout = QHBoxLayout()

        # Create Register Button
        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.handle_register)
        buttons_layout.addWidget(self.register_btn)

        # Create Close Button
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(self.close_btn)

        # Add Buttons to Vertical Layout
        v_layout.addLayout(buttons_layout)

        # Set Vertical Layout to Main Window
        self.setLayout(v_layout)
