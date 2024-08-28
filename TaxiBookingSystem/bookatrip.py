from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt6.QtGui import QPalette, QColor
from connection import Database


class BookATripForm(QWidget):
    def __init__(self, customer_id, db_path):
        super().__init__()
        self.db_path = db_path
        self.customer_id, = customer_id

        self.name_entry = None
        self.phone_number_entry = None
        self.email_entry = None
        self.pick_up_address_entry = None
        self.destination_address_entry = None
        self.pick_up_date_entry = None
        self.pick_up_time_entry = None

        self.submit_button = None
        self.cancel_btn = None
        self.init_ui()

    def book(self):
        # Collect form data
        name = self.name_entry.text()
        phone_number = self.phone_number_entry.text()
        email = self.email_entry.text()
        pick_up_address = self.pick_up_address_entry.text()
        destination_address = self.destination_address_entry.text()
        pick_up_date = self.pick_up_date_entry.text()
        pick_up_time = self.pick_up_time_entry.text()

        # Validate and process the form data
        if not all([name, phone_number, email, pick_up_address, destination_address, pick_up_date, pick_up_time]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        # Database connection and insertion
        db = Database()
        db.connect(self.db_path)
        insert_query = "INSERT INTO booking (PickupAddress, DestinationAddress, PickupDate, PickupTime, CustomerID) VALUES (?,?,?,?,?)"
        insert_params = (pick_up_address, destination_address, pick_up_date, pick_up_time, self.customer_id)
        db.insert_data(insert_query, insert_params)
        db.close_connection()
        # Display success message
        QMessageBox.information(self, "Hooray, Success!", "Your trip has been booked!")
        self.close()

    def init_ui(self):
        # Set up the main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(160, 185, 185)) # Applies background color to dashboard
        self.setPalette(palette)

        # User Information
        customer_info_layout = QFormLayout()
        main_layout.addLayout(customer_info_layout)

        self.name_entry = QLineEdit()
        self.phone_number_entry = QLineEdit()
        self.email_entry = QLineEdit()
        self.pick_up_address_entry = QLineEdit()
        self.destination_address_entry = QLineEdit()
        self.pick_up_date_entry = QLineEdit()
        self.pick_up_time_entry = QLineEdit()

        customer_info_layout.addRow(QLabel("Name"), self.name_entry)
        customer_info_layout.addRow(QLabel("Phone Number"), self.phone_number_entry)
        customer_info_layout.addRow(QLabel("Email"), self.email_entry)
        customer_info_layout.addRow(QLabel("Pick Up Address"), self.pick_up_address_entry)
        customer_info_layout.addRow(QLabel("Destination Address"), self.destination_address_entry)
        customer_info_layout.addRow(QLabel("Pick Up Date"), self.pick_up_date_entry)
        customer_info_layout.addRow(QLabel("Pick Up Time"), self.pick_up_time_entry)

        # Customer Information
        customer_info_layout = QFormLayout()
        main_layout.addLayout(customer_info_layout)

        # Book Trip Button
        self.submit_button = QPushButton("Book Trip")
        self.submit_button.clicked.connect(self.book)
        main_layout.addWidget(self.submit_button)

        # Cancel Button
        self.cancel_btn = QPushButton("Cancel")
        main_layout.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.close)  # This closes the form when clicked

        # Window settings
        self.setWindowTitle("Book A Trip")
        self.resize(400, 300)
