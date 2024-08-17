import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Administrator Dashboard")
        self.setGeometry(100, 100, 700, 400)  # Increased window size
        self.setStyleSheet("background-color: #333; color: white;")  # Set colors and style

        grid = QGridLayout()  # Using Grid Layout for better control

        # Create a title label
        title = QLabel("Name of Group Operations")
        title.setFont(QFont('Helvetica', 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(title, 0, 0, 1, 2)  # Span title across two columns

        # Creating buttons with icons and styling
        btn_view_all_bookings = QPushButton('View All Bookings')
        btn_view_all_bookings.setFont(QFont('Helvetica', 10))
        btn_view_all_bookings.setStyleSheet("background-color: #000000; padding: 10px; color: yellow;")
        btn_view_all_bookings.clicked.connect(self.viewAllBookings)

        btn_manage_drivers = QPushButton('Manage Drivers')
        btn_manage_drivers.setFont(QFont('Helvetica', 10))
        btn_manage_drivers.setStyleSheet("background-color: #000000; padding: 10px; color: yellow;")
        btn_manage_drivers.clicked.connect(self.manageDrivers)

        btn_confirm_booking = QPushButton(QIcon('path/to/confirm_icon.png'), ' Confirm Booking')
        btn_confirm_booking.setFont(QFont('Helvetica', 10))
        btn_confirm_booking.setStyleSheet("background-color: #000000; padding: 10px; color: yellow;")
        btn_confirm_booking.clicked.connect(self.confirmBooking)

        btn_assign_driver = QPushButton(QIcon('path/to/assign_icon.png'), ' Assign Driver to Booking')
        btn_assign_driver.setFont(QFont('Helvetica', 10))
        btn_assign_driver.setStyleSheet("background-color: #000000; padding: 10px; color: yellow;")
        btn_assign_driver.clicked.connect(self.assignDriver)

        btn_log_out = QPushButton(QIcon('path/to/logout_icon.png'), ' Log Out')
        btn_log_out.setFont(QFont('Helvetica', 10))
        btn_log_out.setStyleSheet("background-color: #000000; padding: 10px; color: red;")
        btn_log_out.clicked.connect(self.logOut)

        # Adding widgets to the grid layout
        grid.addWidget(btn_view_all_bookings, 1, 0)
        grid.addWidget(btn_manage_drivers, 1, 1)
        grid.addWidget(btn_confirm_booking, 2, 0)
        grid.addWidget(btn_assign_driver, 2, 1)
        grid.addWidget(btn_log_out, 3, 0, 1, 2)  # Span logout button across two columns

        self.setLayout(grid)

    # Placeholder methods for button actions
    def viewAllBookings(self):
        print("Viewing all bookings")

    def manageDrivers(self):
        print("Managing drivers")

    def confirmBooking(self):
        print("Confirming booking")

    def assignDriver(self):
        print("Assigning driver to booking")

    def logOut(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = AdminWindow()
    ex.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
