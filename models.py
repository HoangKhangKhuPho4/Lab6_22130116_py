# File: models.py

from dataclasses import dataclass, field
from typing import List
import json
import os


@dataclass
class Employee:
    emp_id: str
    name: str
    birthday: str
    salary_rate: float

    def get_annual_salary(self) -> float:
        return self.salary_rate * 12


@dataclass
class Department:
    name: str
    employees: List[Employee] = field(default_factory=list)
    data_file: str = "employees.json"

    def __post_init__(self):
        self.load_employees()

    def add_employee(self, employee: Employee):
        if any(emp.emp_id == employee.emp_id for emp in self.employees):
            raise ValueError("Employee ID already exists.")
        self.employees.append(employee)
        self.save_employees()

    def remove_employee(self, emp_id: str):
        original_count = len(self.employees)
        self.employees = [emp for emp in self.employees if emp.emp_id != emp_id]
        if len(self.employees) == original_count:
            raise ValueError("Employee ID not found.")
        self.save_employees()

    def update_employee(self, updated_employee: Employee):
        for index, emp in enumerate(self.employees):
            if emp.emp_id == updated_employee.emp_id:
                self.employees[index] = updated_employee
                self.save_employees()
                return
        raise ValueError("Employee ID not found.")

    def list_employees(self) -> List[Employee]:
        return self.employees

    def save_employees(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump([emp.__dict__ for emp in self.employees], f, indent=4)
        except Exception as e:
            raise IOError(f"Failed to save employees: {e}")

    def load_employees(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, 'r') as f:
                employees_data = json.load(f)
                self.employees = [Employee(**emp) for emp in employees_data]
        except Exception as e:
            raise IOError(f"Failed to load employees: {e}")

    def __str__(self):
        return f"Department Name: {self.name}, Total Employees: {len(self.employees)}"
