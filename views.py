# File: views.py

from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMenuBar, QGroupBox, QGridLayout, QToolBar, QAbstractItemView
)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont
from PyQt6.QtCore import Qt


class EmployeeView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 1000, 700)

        # Apply a harmonious color palette
        self.apply_color_palette()

        # Set global font
        self.set_global_font()

        # Create Menu Bar
        self.create_menu()

        # Create Toolbar
        self.create_toolbar()

        # Create Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Manage Employees Tab
        self.manage_tab = QWidget()
        self.tabs.addTab(self.manage_tab, "Manage Employees")
        self.create_manage_section()

        # Employee List Tab
        self.list_tab = QWidget()
        self.tabs.addTab(self.list_tab, "Employee List")
        self.create_employee_list()

    def apply_color_palette(self):
        """
        Applies a harmonious color palette to the application using QPalette.
        """
        palette = QPalette()

        # Primary Colors
        primary_color = QColor("#2E8B57")  # SeaGreen
        secondary_color = QColor("#3CB371")  # MediumSeaGreen
        accent_color = QColor("#20B2AA")  # LightSeaGreen

        # Background and Text Colors
        background_color = QColor("#F5F5F5")  # WhiteSmoke
        text_color = QColor("#2F4F4F")  # DarkSlateGray

        # Set Window Background
        palette.setColor(QPalette.ColorRole.Window, background_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)

        # Set Base (e.g., input fields background)
        palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))  # White
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#E0FFFF"))  # LightCyan

        # Set Text
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))  # White

        # Set Highlight
        palette.setColor(QPalette.ColorRole.Highlight, accent_color)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))  # White

        self.setPalette(palette)

    def set_global_font(self):
        """
        Sets a global font for the application.
        """
        font = QFont("Segoe UI", 10)
        self.setFont(font)

    def create_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction(QIcon.fromTheme("application-exit"), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction(QIcon.fromTheme("help-about"), "About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2E8B57; /* SeaGreen */
                spacing: 10px;
            }
            QToolButton {
                color: white;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #3CB371; /* MediumSeaGreen */
                border-radius: 5px;
            }
        """)
        self.addToolBar(toolbar)

        self.add_action = QAction(QIcon.fromTheme("list-add"), "Add Employee", self)
        self.add_action.setShortcut("Ctrl+N")
        toolbar.addAction(self.add_action)

        self.update_action = QAction(QIcon.fromTheme("document-save"), "Update Employee", self)
        self.update_action.setShortcut("Ctrl+S")
        toolbar.addAction(self.update_action)

        self.delete_action = QAction(QIcon.fromTheme("edit-delete"), "Delete Employee", self)
        self.delete_action.setShortcut("Del")
        toolbar.addAction(self.delete_action)

        self.list_action = QAction(QIcon.fromTheme("view-list"), "List Employees", self)
        self.list_action.setShortcut("Ctrl+L")
        toolbar.addAction(self.list_action)

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            "Employee Management System\nVersion 1.0\nDeveloped by Nguyen Le Hoang Khang"
        )

    def create_manage_section(self):
        layout = QVBoxLayout()
        self.manage_tab.setLayout(layout)

        # Employee Details Group
        group_box = QGroupBox("Employee Details")
        group_box.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #2E8B57;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
        """)
        layout.addWidget(group_box)

        grid = QGridLayout()
        group_box.setLayout(grid)

        # Labels and LineEdits
        labels = ["Employee ID:", "Name:", "Birthday (DD/MM/YYYY):", "Salary Rate:"]
        self.emp_id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.birthday_input = QLineEdit()
        self.salary_input = QLineEdit()

        # Set placeholder texts
        self.emp_id_input.setPlaceholderText("e.g., EMP001")
        self.name_input.setPlaceholderText("e.g., John Doe")
        self.birthday_input.setPlaceholderText("e.g., 15/08/1990")
        self.salary_input.setPlaceholderText("e.g., 3000.00")

        # Set tooltips
        self.emp_id_input.setToolTip("Enter unique Employee ID")
        self.name_input.setToolTip("Enter full name of the employee")
        self.birthday_input.setToolTip("Enter birthday in DD/MM/YYYY format")
        self.salary_input.setToolTip("Enter monthly salary rate (positive number)")

        labels_widgets = [QLabel(text) for text in labels]
        for label in labels_widgets:
            label.setStyleSheet("color: #2F4F4F;")  # DarkSlateGray
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        inputs = [self.emp_id_input, self.name_input, self.birthday_input, self.salary_input]

        for i in range(len(labels)):
            grid.addWidget(labels_widgets[i], i, 0)
            grid.addWidget(inputs[i], i, 1)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton(QIcon.fromTheme("list-add"), "Add Employee")
        self.update_button = QPushButton(QIcon.fromTheme("document-save"), "Update Employee")
        self.delete_button = QPushButton(QIcon.fromTheme("edit-delete"), "Delete Employee")
        self.list_button = QPushButton(QIcon.fromTheme("view-list"), "List Employees")

        # Set styles
        button_style = """
            QPushButton {
                background-color: #20B2AA; /* LightSeaGreen */
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3CB371; /* MediumSeaGreen */
            }
        """
        for btn in [self.add_button, self.update_button, self.delete_button, self.list_button]:
            btn.setStyleSheet(button_style)
            btn.setFixedWidth(180)

        # Add buttons to layout
        for btn in [self.add_button, self.update_button, self.delete_button, self.list_button]:
            button_layout.addWidget(btn)

        # Add stretch to push buttons to center
        button_layout.insertStretch(0, 1)
        button_layout.addStretch(1)

        layout.addLayout(button_layout)

    def create_employee_list(self):
        layout = QVBoxLayout()
        self.list_tab.setLayout(layout)

        # Search Bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID or Name")
        self.search_input.setToolTip("Enter Employee ID or Name to search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Birthday", "Salary Rate", "Annual Salary"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                gridline-color: #2E8B57; /* SeaGreen */
            }
            QTableWidget::item:selected {
                background-color: #20B2AA; /* LightSeaGreen */
                color: white;
            }
            QHeaderView::section {
                background-color: #2E8B57; /* SeaGreen */
                color: white;
                padding: 4px;
                font-size: 12px;
            }
        """)
        self.table.setSortingEnabled(True)  # Enable sorting

        layout.addWidget(self.table)

        # Connect search input to filtering function
        self.search_input.textChanged.connect(self.filter_employees)

    def get_employee_details(self) -> dict:
        return {
            'emp_id': self.emp_id_input.text().strip(),
            'name': self.name_input.text().strip(),
            'birthday': self.birthday_input.text().strip(),
            'salary_rate': self.salary_input.text().strip(),
        }

    def display_employees(self, employees):
        self.table.setRowCount(0)
        for emp in employees:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(emp.emp_id))
            self.table.setItem(row_position, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row_position, 2, QTableWidgetItem(emp.birthday))
            self.table.setItem(row_position, 3, QTableWidgetItem(f"{emp.salary_rate:.2f}"))
            self.table.setItem(row_position, 4, QTableWidgetItem(f"{emp.get_annual_salary():.2f}"))

    def get_selected_employee_index(self) -> int:
        selected_items = self.table.selectedItems()
        if selected_items:
            return self.table.currentRow()
        return -1

    def filter_employees(self):
        filter_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            item_id = self.table.item(row, 0).text().lower()
            item_name = self.table.item(row, 1).text().lower()
            if filter_text in item_id or filter_text in item_name:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    # Setter methods to bind controller commands
    def set_add_employee_command(self, command):
        self.add_button.clicked.connect(command)
        self.add_action.triggered.connect(command)

    def set_update_employee_command(self, command):
        self.update_button.clicked.connect(command)
        self.update_action.triggered.connect(command)

    def set_delete_employee_command(self, command):
        self.delete_button.clicked.connect(command)
        self.delete_action.triggered.connect(command)

    def set_list_employees_command(self, command):
        self.list_button.clicked.connect(command)
        self.list_action.triggered.connect(command)

    # Additional methods for input validation feedback
    def highlight_input(self, widget: QLineEdit, valid: bool):
        if valid:
            widget.setStyleSheet("border: 2px solid green;")
        else:
            widget.setStyleSheet("border: 2px solid red;")

    def clear_highlights(self):
        widgets = [self.emp_id_input, self.name_input, self.birthday_input, self.salary_input]
        for widget in widgets:
            widget.setStyleSheet("")

