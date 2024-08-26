from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout,
                             QVBoxLayout, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from connection import Database
from approvebooking import ApproveBookingWidget


class BookingWidget(QWidget):
    def cancel_booking(self):
        cancel_query = "UPDATE booking SET status = 'Cancelled' WHERE bookingID = ?"
        cancel_params = (self.booking_id,)

        db = Database()
        db.connect("db/test.db")
        db.insert_data(query=cancel_query, data=cancel_params)
        db.close_connection()

    def decline_booking(self):
        decline_query = "UPDATE booking SET status = 'Declined' WHERE bookingID = ?"
        decline_params = (self.booking_id,)

        db = Database()
        db.connect("db/test.db")
        db.insert_data(query=decline_query, data=decline_params)
        db.close_connection()

    def approve_booking(self):
        approve_widget = ApproveBookingWidget(self.booking_id)
        approve_widget.show()
        self.close()

    def update_booking(self):
        db = Database()
        db.connect("db/test.db")

        self.pickup_addr = self.pickup_addr_edit.text()
        self.destination = self.destination_edit.text()
        self.pickup_date = self.pickup_date_edit.text()
        self.pickup_time = self.pickup_time_edit.text()
        if self.is_admin:
            self.status = self.status_edit.text()
            self.payment_status = self.payment_status_edit.text()
            idx = self.driver_name_edit.currentIndex()
            driver_id = self.drivers[idx][1]

        if self.is_customer:
            update_query = "UPDATE booking SET pickupAddress =?, destinationAddress =?, " \
                       "pickupDate =?, pickupTime =?, WHERE bookingID =?"
            update_params = (self.pickup_addr, self.destination, self.pickup_date, self.pickup_time)
            db.insert_data(query=update_query, data=update_params)
        elif self.is_admin:
            update_query = "UPDATE booking SET pickupAddress =?, destinationAddress =?, " \
                       "pickupDate =?, pickupTime =?, DriverID =?, status =?, paymentStatus =? WHERE bookingID =?"
            update_params = (self.pickup_addr, self.destination, self.pickup_date, self.pickup_time,
                             driver_id, self.status, self.payment_status, self.booking_id)
            db.insert_data(query=update_query, data=update_params)

        db.close_connection()

    @staticmethod
    def one_or_none_true(a, b, c):
        """Checks if at most one of the three booleans is True."""

        return not ((a and not b and not c) or
            (not a and b and not c) or
            (not a and not b and c) or
            (not a and not b and not c))

    @staticmethod
    def get_customer_name(c_id):
        db = Database()
        db.connect("db/test.db")
        name_query = "SELECT name FROM customer WHERE CustomerID = ?"
        name = db.execute_query(query=name_query, params=(c_id,), fetch_all=False)
        db.close_connection()
        return name if name else "Unknown"

    @staticmethod
    def get_all_drivers():
        db = Database()
        db.connect("db/test.db")
        drivers_query = "SELECT name, driverID FROM driver WHERE status = 'Active'"
        drivers = db.execute_query(query=drivers_query)
        db.close_connection()
        return drivers or []

    @staticmethod
    def get_driver_name(d_id):
        db = Database()
        db.connect("db/test.db")
        name_query = "SELECT name FROM driver WHERE DriverID = ?"
        name = db.execute_query(query=name_query, params=(d_id,), fetch_all=False)
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
        self.third_btn.setText("Update")
        self.third_btn.clicked.connect(self.update_booking)
        self.third_btn.show()
        self.third_btn.setEnabled(False)

    def on_edited(self):
        self.third_btn.setEnabled(True)

    def view_booking(self):
        self.pickup_addr_edit.setReadOnly(True)
        self.pickup_addr_edit.setText(self.pickup_addr)
        self.destination_edit.setReadOnly(True)
        self.destination_edit.setText(self.destination)
        self.pickup_date_edit.setReadOnly(True)
        self.pickup_date_edit.setText(self.pickup_date)
        self.pickup_time_edit.setReadOnly(True)
        self.pickup_time_edit.setText(self.pickup_time)
        if self.is_admin:
            self.status_edit.setReadOnly(True)
            self.status_edit.setText(self.status)

            self.driver_name_edit.setEnabled(False)
            index = self.driver_name_edit.findText(self.name)
            if index != -1:
                self.driver_name_edit.setCurrentIndex(index)

            self.payment_status_edit.setReadOnly(True)
            self.payment_status_edit.setText(self.payment_status)

        self.edit_btn.setText("Edit")
        self.edit_btn.clicked.connect(self.edit_booking)
        self.third_btn.setText("Cancel")
        self.third_btn.clicked.connect(self.cancel_booking)
        self.third_btn.setEnabled(True)
        if self.is_admin:
            self.third_btn.hide()

    def __init__(self, booking, is_customer=False, is_admin=False, is_to_approve=False):
        super().__init__()
        (self.booking_id, self.pickup_addr, self.destination, self.pickup_date, self.pickup_time, self.status, self.customer_id,
         self.driver_id, self.payment_status) = booking

        self.is_admin = is_admin
        self.is_customer = is_customer
        self.is_to_approve = is_to_approve

        if self.one_or_none_true(is_admin, is_customer, is_to_approve):
            raise ValueError("NONE or ONLY ONE of is_admin, is_customer, and is_to_approve should be True.")

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
        driver_name_layout = QHBoxLayout()
        if is_admin:
            payment_status_layout = QHBoxLayout()
        else:
            payment_status_layout = None

        details_layout.addLayout(id_layout)
        details_layout.addLayout(pickup_addr_layout)
        details_layout.addLayout(destination_layout)
        details_layout.addLayout(pickup_date_layout)
        details_layout.addLayout(pickup_time_layout)
        details_layout.addLayout(status_layout)
        details_layout.addLayout(customer_name_layout)
        details_layout.addLayout(driver_name_layout)
        if is_admin:
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

        if not is_to_approve:
            driver_name_label = QLabel("Driver Name:")
            driver_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            driver_name_label.setStyleSheet("font-weight: bold;")
            driver_name_layout.addWidget(driver_name_label)

        if is_admin:
            payment_status_label = QLabel("Payment Status:")
            payment_status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            payment_status_layout.addWidget(payment_status_label)

        # Create Line Edits (Uneditable)
        self.id_edit = QLineEdit(str(self.booking_id))
        self.id_edit.setReadOnly(True)
        id_layout.addWidget(self.id_edit)

        self.pickup_addr_edit = QLineEdit(str(self.pickup_addr))
        self.pickup_addr_edit.setReadOnly(True)
        pickup_addr_layout.addWidget(self.pickup_addr_edit)
        self.pickup_addr_edit.textEdited.connect(self.on_edited)

        self.destination_edit = QLineEdit(str(self.destination))
        self.destination_edit.setReadOnly(True)
        destination_layout.addWidget(self.destination_edit)
        self.destination_edit.textEdited.connect(self.on_edited)

        self.pickup_date_edit = QLineEdit(str(self.pickup_date))
        self.pickup_date_edit.setReadOnly(True)
        pickup_date_layout.addWidget(self.pickup_date_edit)
        self.pickup_date_edit.textEdited.connect(self.on_edited)

        self.pickup_time_edit = QLineEdit(str(self.pickup_time))
        self.pickup_time_edit.setReadOnly(True)
        pickup_time_layout.addWidget(self.pickup_time_edit)
        self.pickup_time_edit.textEdited.connect(self.on_edited)

        self.status_edit = QLineEdit(self.status)
        self.status_edit.setReadOnly(True)
        status_layout.addWidget(self.status_edit)
        self.status_edit.textEdited.connect(self.on_edited)

        name = self.get_customer_name(self.customer_id)
        self.customer_name_edit = QLineEdit(str(name[0]))
        self.customer_name_edit.setReadOnly(True)
        customer_name_layout.addWidget(self.customer_name_edit)

        if is_admin:
            self.name = self.get_driver_name(self.driver_id)
            self.drivers = self.get_all_drivers()
            self.driver_name_edit = QComboBox()
            driver_names = (driver[0] for driver in self.drivers)
            self.driver_combobox.addItems(driver_names)
            index = self.driver_name_edit.findText(self.name)

            if index != -1:
                self.driver_name_edit.setCurrentIndex(index)

            self.driver_name_edit.setEnabled(False)
            driver_name_layout.addWidget(self.driver_name_edit, 1)
            self.driver_name_edit.currentTextChanged.connect(self.on_edited)

            self.payment_status_edit = QLineEdit(self.payment_status)
            self.payment_status_edit.setReadOnly(True)
            payment_status_layout.addWidget(self.payment_status_edit)
            self.payment_status_edit.textEdited.connect(self.on_edited)
        elif is_to_approve:
            self.driver_name_edit = None
        else:
            if self.driver_id == -1:
                name = "Unassigned"
            else:
                name = self.get_driver_name(self.driver_id)

            self.driver_name_edit = QLineEdit(str(name[0]))
            self.driver_name_edit.setReadOnly(True)
            driver_name_layout.addWidget(self.driver_name_edit)
            self.payment_status_edit = None

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        v_layout.addLayout(buttons_layout)

        # Edit Button
        if is_customer or is_admin:
            self.edit_btn = QPushButton("Edit")
            self.edit_btn.clicked.connect(self.edit_booking)
            buttons_layout.addWidget(self.edit_btn)
        elif is_to_approve:
            self.edit_btn = QPushButton("Approve")
            self.edit_btn.clicked.connect(self.approve_booking)
            buttons_layout.addWidget(self.edit_btn)
        else:
            self.edit_btn = None

        if is_customer:
            self.third_btn = QPushButton("Cancel")
            self.third_btn.clicked.connect(self.cancel_booking)
            buttons_layout.addWidget(self.third_btn)
        elif is_admin and not is_to_approve:
            self.third_btn = QPushButton("Update")
            self.third_btn.clicked.connect(self.update_booking)
            buttons_layout.addWidget(self.third_btn)
            self.third_btn.hide()
        elif is_to_approve:
            self.third_btn = QPushButton("Decline")
            self.third_btn.clicked.connect(self.decline_booking)
            buttons_layout.addWidget(self.third_btn)

        close_layout = QHBoxLayout()
        # Close Button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_layout.addWidget(close_btn)

        v_layout.addLayout(buttons_layout)
        v_layout.addLayout(close_layout)
