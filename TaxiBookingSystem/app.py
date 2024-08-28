import sys
from PyQt6.QtWidgets import QApplication
from home import HomeWidget


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db_path = "db/tbs.db"
        self.home_window = HomeWidget(app=self.app, db_path=self.db_path)

    def run_app(self):
        self.home_window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = App()
    app.run_app()
