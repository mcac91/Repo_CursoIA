"""
Employee management module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from app.models import Database, Employee
from app.repository import JsonRepository


def _getDefaultJsonPath() -> Path:
    """
    Build the default JSON path for this activity folder.

    Input: none
    Output: Path
    """

    return Path(__file__).resolve().parent / "data" / "empleados.json"


def _getNextEmployeeId(db: Database) -> int:
    """
    Compute the next employee id by incrementing the current max.

    Input: db (Database)
    Output: int
    """

    maxId = 0
    for employee in db.get("empleados", []):
        if isinstance(employee, dict):
            candidate = employee.get("id")
            if isinstance(candidate, int) and candidate > maxId:
                maxId = candidate
    return maxId + 1


def _findEmployeeById(db: Database, employeeId: int) -> Optional[Employee]:
    """
    Find an employee by id.

    Input: db (Database), employeeId (int)
    Output: Employee | None
    """

    for employee in db.get("empleados", []):
        if isinstance(employee, dict) and employee.get("id") == employeeId:
            return employee  # type: ignore[return-value]
    return None


def agregar_empleado(nombre, cargo) -> dict:
    """
    Add a new employee to the database.

    Input: nombre (str), cargo (str)
    Output: dict (created employee) or empty dict on failure
    """

    try:
        if not isinstance(nombre, str) or not isinstance(cargo, str):
            return {}

        name = nombre.strip()
        role = cargo.strip()
        if name == "" or role == "":
            return {}

        repo = JsonRepository(_getDefaultJsonPath())
        db = repo.loadDatabase()

        newEmployee: Employee = {
            "id": _getNextEmployeeId(db),
            "nombre": name,
            "cargo": role,
            "contratos": [],
        }
        db["empleados"].append(newEmployee)

        if not repo.saveDatabase(db):
            return {}

        return newEmployee
    except Exception:
        return {}


def eliminar_empleado(id) -> bool:
    """
    Delete an employee by id.

    Input: id (int)
    Output: bool (True on success, False otherwise)
    """

    try:
        employeeId = int(id)

        repo = JsonRepository(_getDefaultJsonPath())
        db = repo.loadDatabase()

        employees = db.get("empleados", [])
        for idx, employee in enumerate(employees):
            if isinstance(employee, dict) and employee.get("id") == employeeId:
                del employees[idx]
                return repo.saveDatabase(db)

        return False
    except Exception:
        return False


def buscar_empleado(id) -> dict:
    """
    Find an employee by id.

    Input: id (int)
    Output: dict (employee) or empty dict if not found / invalid
    """

    try:
        employeeId = int(id)

        repo = JsonRepository(_getDefaultJsonPath())
        db = repo.loadDatabase()

        employee = _findEmployeeById(db, employeeId)
        return employee if employee is not None else {}
    except Exception:
        return {}

