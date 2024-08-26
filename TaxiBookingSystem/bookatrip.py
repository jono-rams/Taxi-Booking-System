import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt6.QtGui import QPalette, QColor
class BookATripForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        def __init__(self):
            # Collect form data
            name = self.name_entry.text()
            phone_number = self.phone_number_entry.text()
            email = self.email_entry.text()
            pick_up_address = self.pick_up_address_entry.text()
            destination_address = self.destination_address_entry.text()
            pick_up_date = self.pick_up_date_entry.text()
            pick_up_time = self.pick_up_time_entry.text()
            payment_method = self.payment_method_combobox.currentText()

            # Validate and process the form data
            if not all([name, phone_number, email, pick_up_address, destination_address, pick_up_date, pick_up_time]):
                QMessageBox.warning(self, "Error", "Please fill in all required fields.")
                return

            # Display success message
            QMessageBox.information(self, "Hooray, Success!", "Your trip has been booked!")

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
        self.payment_method_combobox = QComboBox()
        self.payment_method_combobox.addItems(["Cash", "Debit Card", "Credit Card"]) # Dropdown menu details

        customer_info_layout.addRow(QLabel("Name"), self.name_entry)
        customer_info_layout.addRow(QLabel("Phone Number"), self.phone_number_entry)
        customer_info_layout.addRow(QLabel("Email"), self.email_entry )
        customer_info_layout.addRow(QLabel("Pick Up Address"), self.pick_up_address_entry)
        customer_info_layout.addRow(QLabel("Destination Address"), self.pick_up_date_entry)
        customer_info_layout.addRow(QLabel("Pick Up Date"), self.pick_up_time_entry)
        customer_info_layout.addRow(QLabel("Payment Method"), self.payment_method_combobox) # Applies a dropdown box

        # Customer Information
        customer_info_layout = QFormLayout()
        main_layout.addLayout(customer_info_layout)

        # Book Trip Button
        self.submit_button = QPushButton("Book Trip")
        self.submit_button.clicked.connect(self.__init__)
        main_layout.addWidget(self.submit_button)

        # Cancel Button
        self.submit_button = QPushButton("Cancel")
        self.submit_button.clicked.connect(self.__init__)
        main_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.close)  # This closes the form when clicked

        # Window settings
        self.setWindowTitle("Book A Trip")
        self.resize(400, 300)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = BookATripForm()
    form.show()
    sys.exit(app.exec())
