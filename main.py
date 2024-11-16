# File: main.py

import sys
import logging
from PyQt6.QtWidgets import QApplication
from models import Department
from views import EmployeeView
from controllers import EmployeeController


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    setup_logging()
    app = QApplication(sys.argv)
    department = Department("HR")
    view = EmployeeView()
    controller = EmployeeController(department, view)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
