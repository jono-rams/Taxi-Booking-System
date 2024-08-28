import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QScrollArea,
                             QFormLayout, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
import datetime
from connection import Database
from bookingdetails import BookingWidget
from bookatrip import BookATripForm
from customerviewbookings import AllBookingsWindow


# Main customer window class
class CustomerWindow(QWidget):
    def __init__(self, customer_id, db_path):
        super().__init__()
        self.customer_id = customer_id  # Store the customer ID
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        # Set up the Customer Dashboard Window
        self.setWindowTitle("Customer Dashboard")
        self.setGeometry(100, 100, 700, 400)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(160, 185, 185))  # Applies background color to dashboard
        self.setPalette(palette)  # Set colors and style

        # Create a grid layout to arrange the buttons
        grid = QGridLayout()

        # Title label
        title = QLabel("<u>Customer Dashboard</u>")  # Underlines the label
        title.setFont(QFont('Times New Roman', 25, QFont.Weight.Bold))  # This sets the font of choice, size, bolds the context
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(title, 0, 0, 1, 2)

        # Button to book a trip
        btn_book_a_trip = QPushButton('Book A Trip')
        btn_book_a_trip.setFont(QFont('Times New Roman', 12))
        btn_book_a_trip.setStyleSheet("background-color: #000000; padding: 10px; color: white;")
        btn_book_a_trip.clicked.connect(self.bookTrip)

        # Button to view trip history
        btn_view_trip = QPushButton('My Upcoming Trips')
        btn_view_trip.setFont(QFont('Times New Roman', 12))
        btn_view_trip.setStyleSheet("background-color: #000000; padding: 10px; color: white;")
        btn_view_trip.clicked.connect(self.viewTrip)

        # Log Out button centered below the other buttons
        btn_log_out = QPushButton(QIcon('path/to/logout_icon.png'), ' Log Out')
        btn_log_out.setFont(QFont('Times New Roman', 12, QFont.Weight.Bold))
        btn_log_out.setStyleSheet("background-color: #000000; padding: 10px; color: white;")
        btn_log_out.clicked.connect(self.logOut)
        grid.addWidget(btn_log_out, 3, 0, 1, 2, Qt.AlignmentFlag.AlignBottom)  # Aligned below the other buttons
        btn_log_out.clicked.connect(self.close)  # Closes message popup and customer dashboard

        # Adding widgets to the grid layout
        grid.addWidget(btn_book_a_trip, 2, 0)  # Left aligns button above logout button
        grid.addWidget(btn_view_trip, 2, 1)  # Right aligns button above logout button
        grid.addWidget(btn_log_out, 3, 0, 1, 2)  # Span logout button across two columns

        # Set the grid layout as the main layout for the window
        self.setLayout(grid)

    def bookTrip(self):
        self.book_trip = BookATripForm(customer_id=self.customer_id, db_path=self.db_path)
        self.book_trip.show()  # Show the BookATripForm window when the button is clicked

    def viewTrip(self):
        # Open the All Bookings window for the logged-in customer
        self.all_bookings_window = AllBookingsWindow(self.customer_id, self.db_path)
        self.all_bookings_window.show()

    def logOut(self):
        # Placeholder for log out functionality
        QMessageBox.information(self, "Logout Successful!", "You have successfully logged out.")
