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


# Window class to display all bookings in a scrollable list
class AllBookingsWindow(QWidget):
    def __init__(self, customer_id):
        super().__init__()
        self.db_path = r"C:\Users\user\PycharmProjects\ISD-A2\TaxiBookingSystem\db\tbs.db"
        self.db = Database()
        self.customer_id, = customer_id  # Store the customer ID for fetching bookings
        self.bookings = None
        self.booking_widget = None
        self.initUI()

    def initUI(self):
        # Set up the All Bookings window
        self.setWindowTitle("My Upcoming Bookings")
        self.setGeometry(100, 100, 600, 400)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(160, 185, 185))  # Applies background color to dashboard
        self.setPalette(palette)  # Set colors and style

        # Create a vertical layout for the scroll area and the scroll widget
        layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)  # Automatically resizes widget
        scroll_area.setWidget(scroll_widget)  # Scroll allows maneuvering of content if it does not fit in visible area
        layout.addWidget(scroll_area)

        # Load bookings and create buttons to view each booking's details
        self.db.connect(self.db_path)
        booking_query = "SELECT * FROM booking WHERE CustomerID = ? AND PickupDate >= ? AND BookingStatus = 'Confirmed'"
        today = datetime.date.today()
        booking_params = (self.customer_id, today)
        self.bookings = self.db.execute_query(query=booking_query, params=booking_params, fetch_all=True)
        self.db.close_connection()

        # Add an entry for each booking
        for i in range(len(self.bookings)):
            entry_layout = QHBoxLayout()
            label = QLabel(f"Booking {i}")
            entry_layout.addWidget(label)

            view_btn = QPushButton("View")
            view_btn.setFixedSize(120, 50)
            view_btn.clicked.connect(lambda _, idx=i: self.handle_view_click(idx))
            entry_layout.addWidget(view_btn)

            scroll_layout.addLayout(entry_layout)

        # Close button to close the All Bookings window
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def handle_view_click(self, index):
        # Call view booking data with index to pull data from bookings
        self.booking_widget = BookingWidget(booking=self.bookings[index], is_customer=True)
        self.booking_widget.show()


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
        # Placeholder for booking a trip (until linked)
        QMessageBox.information(self, "Book A Trip!", "This feature is not implemented yet =(")

    def viewTrip(self):
        # Open the All Bookings window for the logged-in customer
        self.all_bookings_window = AllBookingsWindow(self.customer_id)
        self.all_bookings_window.show()

    def logOut(self):
        # Placeholder for log out functionality
        QMessageBox.information(self, "Logout Successful!", "You have successfully logged out.")


def main():
    app = QApplication(sys.argv)
    customer_id = 1  # Replace with an actual customer ID from database
    db_path = r"C:\Users\user\PycharmProjects\ISD-A2\TaxiBookingSystem\db\tbs.db"
    ex = CustomerWindow(customer_id=customer_id, db_path=db_path)
    ex.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
