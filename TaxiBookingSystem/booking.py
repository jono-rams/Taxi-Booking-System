from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout,
                             QVBoxLayout, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from connection import Database
import sys


class BookingWidget(QWidget):
    @staticmethod
    def get_customer_name(c_id):
        db = Database()
        db.connect("db/test.db")
        name_query = "SELECT name FROM customers WHERE CustomerID = ?"
        name = db.execute_query(query=name_query, params=c_id, fetch_all=False)
        db.close_connection()
        return name if name else "Unknown"

    @staticmethod
    def get_all_drivers():
        db = Database()
        db.connect("db/test.db")
        drivers_query = "SELECT name FROM drivers"
        drivers = db.execute_query(query=drivers_query)
        db.close_connection()
        return drivers or []

    @staticmethod
    def get_driver_name(d_id):
        db = Database()
        db.connect("db/test.db")
        name_query = "SELECT name FROM drivers WHERE DriverID = ?"
        name = db.execute_query(query=name_query, params=d_id, fetch_all=False)
        db.close_connection()
        return name if name else "Unknown"

    def edit_booking(self):
        self.pickup_addr_edit.setReadOnly(False)
        self.destination_edit.setReadOnly(False)
        self.pickup_date_edit.setReadOnly(False)
        self.pickup_time_edit.setReadOnly(False)
        if self.is_admin:
            self.status_edit.setReadOnly(False)
            self.driver_name_edit.setEnabled(True)
            self.payment_status_edit.setReadOnly(False)

        self.edit_btn.setText("View")
        self.edit_btn.clicked.connect(self.view_booking)

    def view_booking(self):
        self.pickup_addr_edit.setReadOnly(True)
        self.destination_edit.setReadOnly(True)
        self.pickup_date_edit.setReadOnly(True)
        self.pickup_time_edit.setReadOnly(True)
        if self.is_admin:
            self.status_edit.setReadOnly(True)
            self.driver_name_edit.setEnabled(False)
            self.payment_status_edit.setReadOnly(True)

        self.edit_btn.setText("Edit")
        self.edit_btn.clicked.connect(self.edit_booking)

    def __init__(self, booking, editable=False, is_admin=False):
        super().__init__()
        (self.id, self.pickup_addr, self.destination, self.pickup_date, self.pickup_time, self.status, self.customer_id,
         self.driver_id, self.payment_status) = booking

        self.is_admin = is_admin

        # Create Main Window
        self.setWindowTitle("Booking Details")
        self.setFixedSize(600, 400)

        # Create Vertical Layout
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        # Create Label Widget
        label = QLabel("Booking Details!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(18)
        font.setFamily("TimesNewRoman")
        label.setFont(font)
        label.setFixedHeight(30)

        v_layout.addWidget(label)

        # Create Horizontal Layout
        details_layout = QVBoxLayout()
        v_layout.addLayout(details_layout)

        id_layout = QHBoxLayout()
        pickup_addr_layout = QHBoxLayout()
        destination_layout = QHBoxLayout()
        pickup_date_layout = QHBoxLayout()
        pickup_time_layout = QHBoxLayout()
        status_layout = QHBoxLayout()
        customer_name_layout = QHBoxLayout()
        if is_admin:
            driver_name_layout = QHBoxLayout()
            payment_status_layout = QHBoxLayout()
        else:
            driver_name_layout = None
            payment_status_layout = None

        details_layout.addLayout(id_layout)
        details_layout.addLayout(pickup_addr_layout)
        details_layout.addLayout(destination_layout)
        details_layout.addLayout(pickup_date_layout)
        details_layout.addLayout(pickup_time_layout)
        details_layout.addLayout(status_layout)
        details_layout.addLayout(customer_name_layout)
        if is_admin:
            details_layout.addLayout(driver_name_layout)
            details_layout.addLayout(payment_status_layout)

        # Create Label Widgets
        id_label = QLabel("Booking ID:")
        id_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        id_label.setStyleSheet("font-weight: bold;")
        id_layout.addWidget(id_label)

        pickup_addr_label = QLabel("Pickup Address:")
        pickup_addr_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        id_label.setStyleSheet("font-weight: bold;")
        pickup_addr_layout.addWidget(pickup_addr_label)

        destination_label = QLabel("Destination:")
        destination_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        id_label.setStyleSheet("font-weight: bold;")
        destination_layout.addWidget(destination_label)

        pickup_date_label = QLabel("Pickup Date:")
        pickup_date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        id_label.setStyleSheet("font-weight: bold;")
        pickup_date_layout.addWidget(pickup_date_label)

        pickup_time_label = QLabel("Pickup Time:")
        pickup_time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        id_label.setStyleSheet("font-weight: bold;")
        pickup_time_layout.addWidget(pickup_time_label)

        status_label = QLabel("Status:")
        status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        status_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(status_label)

        customer_name_label = QLabel("Customer Name:")
        customer_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        customer_name_label.setStyleSheet("font-weight: bold;")
        customer_name_layout.addWidget(customer_name_label)

        if is_admin:
            driver_name_label = QLabel("Driver Name:")
            driver_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            driver_name_label.setStyleSheet("font-weight: bold;")
            driver_name_layout.addWidget(driver_name_label)

            payment_status_label = QLabel("Payment Status:")
            payment_status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            driver_name_label.setStyleSheet("font-weight: bold;")
            payment_status_layout.addWidget(payment_status_label)

        # Create Line Edits (Uneditable)
        self.id_edit = QLineEdit(str(self.id))
        self.id_edit.setReadOnly(True)
        id_layout.addWidget(self.id_edit)

        self.pickup_addr_edit = QLineEdit(str(self.pickup_addr))
        self.pickup_addr_edit.setReadOnly(True)
        pickup_addr_layout.addWidget(self.pickup_addr_edit)

        self.destination_edit = QLineEdit(str(self.destination))
        self.destination_edit.setReadOnly(True)
        destination_layout.addWidget(self.destination_edit)

        self.pickup_date_edit = QLineEdit(str(self.pickup_date))
        self.pickup_date_edit.setReadOnly(True)
        pickup_date_layout.addWidget(self.pickup_date_edit)

        self.pickup_time_edit = QLineEdit(str(self.pickup_time))
        self.pickup_time_edit.setReadOnly(True)
        pickup_time_layout.addWidget(self.pickup_time_edit)

        self.status_edit = QLineEdit(self.status)
        self.status_edit.setReadOnly(True)
        status_layout.addWidget(self.status_edit)

        # name = self.get_customer_name(self.customer_id)
        name = "Unknown"  # Placeholder until customer data is available
        self.customer_name_edit = QLineEdit(str(name))
        self.customer_name_edit.setReadOnly(True)
        customer_name_layout.addWidget(self.customer_name_edit)

        if is_admin:
            # name = self.get_driver_name(self.driver_id)
            self.driver_name_edit = QComboBox()
            # self.driver_name_edit.addItems(self.get_all_drivers())  # Populate combo box with all drivers
            self.driver_name_edit.addItems(["Unknown", "Mystery"])  # Placeholder
            # index = driver_name_edit.findText(name)
            index = self.driver_name_edit.findText("Mystery")  # Placeholder

            if index != -1:
                self.driver_name_edit.setCurrentIndex(index)

            self.driver_name_edit.setEnabled(False)
            driver_name_layout.addWidget(self.driver_name_edit, 1)

            self.payment_status_edit = QLineEdit(self.payment_status)  # Placeholder until payment data is available
            self.payment_status_edit.setReadOnly(True)
            payment_status_layout.addWidget(self.payment_status_edit)
        else:
            self.driver_name_edit = None
            self.payment_status_edit = None

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        v_layout.addLayout(buttons_layout)

        # Edit Button
        if editable:
            self.edit_btn = QPushButton("Edit")
            self.edit_btn.clicked.connect(self.edit_booking)
            buttons_layout.addWidget(self.edit_btn)
        else:
            self.edit_btn = None

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)

        v_layout.addLayout(buttons_layout)
