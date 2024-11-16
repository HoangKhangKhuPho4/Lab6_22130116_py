# File: controllers.py

from models import Department, Employee
from views import EmployeeView
from PyQt6.QtWidgets import QMessageBox
import datetime
import logging


class EmployeeController:
    def __init__(self, department: Department, view: EmployeeView):
        self.department = department
        self.view = view
        self.bind_buttons()
        self.view.display_employees(self.department.list_employees())

    def bind_buttons(self):
        self.view.set_add_employee_command(self.add_employee)
        self.view.set_update_employee_command(self.update_employee)
        self.view.set_delete_employee_command(self.delete_employee)
        self.view.set_list_employees_command(self.list_employees)

    def add_employee(self):
        details = self.view.get_employee_details()
        emp_id = details['emp_id']
        name = details['name']
        birthday = details['birthday']
        salary_rate_str = details['salary_rate']

        # Clear previous highlights
        self.view.clear_highlights()

        # Validate inputs
        valid = True
        if not emp_id:
            self.view.highlight_input(self.view.emp_id_input, False)
            valid = False
        if not name:
            self.view.highlight_input(self.view.name_input, False)
            valid = False
        if not self.validate_birthday(birthday):
            self.view.highlight_input(self.view.birthday_input, False)
            valid = False
        if not self.validate_salary(salary_rate_str):
            self.view.highlight_input(self.view.salary_input, False)
            valid = False

        if not valid:
            self.show_error("Please correct the highlighted fields.")
            return

        try:
            salary_rate = float(salary_rate_str)
        except ValueError:
            self.show_error("Salary Rate must be a valid number.")
            return

        # Add employee
        try:
            new_employee = Employee(emp_id, name, birthday, salary_rate)
            self.department.add_employee(new_employee)
            self.view.display_employees(self.department.list_employees())
            QMessageBox.information(self.view, "Success", "Employee added successfully.")
            self.clear_inputs()
            logging.info(f"Added employee: {new_employee.emp_id} - {new_employee.name}")
        except ValueError as ve:
            self.show_error(str(ve))
            logging.error(f"Error adding employee: {str(ve)}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")
            logging.error(f"Unexpected error adding employee: {str(e)}")

    def update_employee(self):
        selected_index = self.view.get_selected_employee_index()
        if selected_index == -1:
            self.show_error("No employee selected.")
            return

        current_emp = self.department.employees[selected_index]
        details = self.view.get_employee_details()
        emp_id = details['emp_id']
        name = details['name']
        birthday = details['birthday']
        salary_rate_str = details['salary_rate']

        # Clear previous highlights
        self.view.clear_highlights()

        # Validate inputs
        valid = True
        if not emp_id:
            self.view.highlight_input(self.view.emp_id_input, False)
            valid = False
        if not name:
            self.view.highlight_input(self.view.name_input, False)
            valid = False
        if not self.validate_birthday(birthday):
            self.view.highlight_input(self.view.birthday_input, False)
            valid = False
        if not self.validate_salary(salary_rate_str):
            self.view.highlight_input(self.view.salary_input, False)
            valid = False

        if not valid:
            self.show_error("Please correct the highlighted fields.")
            return

        try:
            salary_rate = float(salary_rate_str)
        except ValueError:
            self.show_error("Salary Rate must be a valid number.")
            return

        if emp_id != current_emp.emp_id and any(emp.emp_id == emp_id for emp in self.department.employees):
            self.show_error("Employee ID already exists.")
            self.view.highlight_input(self.view.emp_id_input, False)
            return

        # Update employee
        try:
            updated_employee = Employee(emp_id, name, birthday, salary_rate)
            self.department.update_employee(updated_employee)
            self.view.display_employees(self.department.list_employees())
            QMessageBox.information(self.view, "Success", "Employee updated successfully.")
            self.clear_inputs()
            logging.info(f"Updated employee: {updated_employee.emp_id} - {updated_employee.name}")
        except ValueError as ve:
            self.show_error(str(ve))
            logging.error(f"Error updating employee: {str(ve)}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")
            logging.error(f"Unexpected error updating employee: {str(e)}")

    def delete_employee(self):
        selected_index = self.view.get_selected_employee_index()
        if selected_index == -1:
            self.show_error("No employee selected.")
            return

        emp = self.department.employees[selected_index]
        confirm = QMessageBox.question(
            self.view,
            "Confirm Delete",
            f"Are you sure you want to delete employee '{emp.name}' (ID: {emp.emp_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.department.remove_employee(emp.emp_id)
                self.view.display_employees(self.department.list_employees())
                QMessageBox.information(self.view, "Success", "Employee deleted successfully.")
                self.clear_inputs()
                logging.info(f"Deleted employee: {emp.emp_id} - {emp.name}")
            except ValueError as ve:
                self.show_error(str(ve))
                logging.error(f"Error deleting employee: {str(ve)}")
            except Exception as e:
                self.show_error(f"An unexpected error occurred: {str(e)}")
                logging.error(f"Unexpected error deleting employee: {str(e)}")

    def list_employees(self):
        try:
            employees = self.department.list_employees()
            self.view.display_employees(employees)
            logging.info("Listed all employees.")
        except Exception as e:
            self.show_error(f"An error occurred while listing employees: {str(e)}")
            logging.error(f"Error listing employees: {str(e)}")

    def clear_inputs(self):
        self.view.emp_id_input.clear()
        self.view.name_input.clear()
        self.view.birthday_input.clear()
        self.view.salary_input.clear()
        self.view.clear_highlights()

    def validate_birthday(self, birthday: str) -> bool:
        try:
            datetime.datetime.strptime(birthday, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validate_salary(self, salary: str) -> bool:
        try:
            salary_float = float(salary)
            return salary_float >= 0
        except ValueError:
            return False

    def show_error(self, message: str):
        QMessageBox.critical(self.view, "Error", message)
