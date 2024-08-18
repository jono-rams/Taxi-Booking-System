from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout,
                             QVBoxLayout, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from connection import Database


class LoginWidget(QWidget):

    def handle_login(self):
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
        login_query = "SELECT * FROM users WHERE email = ? AND password = ?"
        login_params = (email, password)

        results = self.db.execute_query(query=login_query, params=login_params)

        self.db.close_connection()

        if not results:
            QMessageBox.warning(None, "Error", "Invalid email or password.")
        else:
            QMessageBox.information(None, "Login Successful", "Welcome")
            self.close()

    def __init__(self):
        super().__init__()

        self.db = Database()

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
        label.setFixedHeight(35)

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

        # Create Horizontal Layout for Options
        options_layout = QHBoxLayout()
        options_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create Label for Login Options
        options_label = QLabel("Login option:")

        # Create Combo Box to select login options
        self.options_box = QComboBox()
        self.options_box.addItems(["Customer", "Driver", "Admin"])
        self.options_box.currentIndexChanged.connect(self.on_selection_changed)
        self.selected_option = None

        # Add Options widgets to Layout
        options_layout.addWidget(options_label)
        options_layout.addWidget(self.options_box, 1)

        # Add Options Layout to Vertical Layout
        fields_layout.addLayout(options_layout)

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

    def on_selection_changed(self, index):
        self.selected_option = self.options_box.currentText()
