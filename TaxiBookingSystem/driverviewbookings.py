import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt
import datetime
from connection import Database
from bookingdetails import BookingWidget


class ViewBookings(QWidget):
    def handle_close(self):
        self.close()
        self.dash_reference.show()

    def __init__(self, driver_id, db_path, dash_reference=None, is_admin=False):
        super().__init__()

        self.is_admin = is_admin

        self.driver_id = driver_id
        self.booking_widget = None
        self.db_path = db_path
        if dash_reference:
            self.dash_reference = dash_reference
            self.dash_reference.hide()

        self.setWindowTitle("All Bookings")
        self.setFixedSize(800, 450)
        self.layout = QVBoxLayout(self)

        # Scroll Area to hold the content
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        self.db = Database()
        self.db.connect(self.db_path)
        booking_query = "SELECT * FROM booking WHERE DriverID = ? AND PickupDate >= ? AND BookingStatus = 'Confirmed'"
        today = datetime.date.today()
        booking_params = (self.driver_id, today)
        self.bookings = self.db.execute_query(query=booking_query, params=booking_params, fetch_all=True)
        self.db.close_connection()

        # Add an entry for each booking
        for i in range(len(self.bookings)):
            entry_layout = QHBoxLayout()
            label = QLabel(f"Booking {i}")
            entry_layout.addWidget(label)

            view_btn = QPushButton("View")
            view_btn.setFixedSize(120, 50)
            view_btn.clicked.connect(lambda _, idx=i: self.handle_view_click(idx))  # Connect button to function passing its index as a parameter
            entry_layout.addWidget(view_btn)

            scroll_layout.addLayout(entry_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Add close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedSize(100, 50)
        self.close_btn.clicked.connect(self.handle_close)
        button_layout.addWidget(self.close_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def handle_view_click(self, index):
        # Call view booking data with index to pull data from bookings
        if self.is_admin:
            self.booking_widget = BookingWidget(booking=self.bookings[index], db_path=self.db_path, is_admin=True)
            self.booking_widget.show()
        else:
            self.booking_widget = BookingWidget(booking=self.bookings[index], db_path=self.db_path)
            self.booking_widget.show()
