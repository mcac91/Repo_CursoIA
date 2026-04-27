"""
Módulo de gestión de empleados.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from app.models import BaseDatos, Empleado
from app.repository import JsonRepository


def _ruta_json_por_defecto() -> Path:
    """
    Construye la ruta por defecto del JSON para esta actividad.

    Input: ninguno
    Output: Path
    """

    return Path(__file__).resolve().parent / "data" / "empleados.json"


def _siguiente_id_empleado(db: BaseDatos) -> int:
    """
    Calcula el siguiente id de empleado incrementando el máximo actual.

    Input: db (BaseDatos)
    Output: int
    """

    max_id = 0
    for employee in db.get("empleados", []):
        if isinstance(employee, dict):
            candidate = employee.get("id")
            if isinstance(candidate, int) and candidate > max_id:
                max_id = candidate
    return max_id + 1


def _buscar_empleado_por_id(db: BaseDatos, employee_id: int) -> Optional[Empleado]:
    """
    Busca un empleado por id.

    Input: db (BaseDatos), employee_id (int)
    Output: Empleado | None
    """

    for employee in db.get("empleados", []):
        if isinstance(employee, dict) and employee.get("id") == employee_id:
            return employee  # type: ignore[return-value]
    return None


def agregar_empleado(nombre, cargo) -> dict:
    """
    Añade un nuevo empleado a la base de datos.

    Input: nombre (str), cargo (str)
    Output: dict (empleado creado) o dict vacío en caso de fallo
    """

    try:
        if not isinstance(nombre, str) or not isinstance(cargo, str):
            return {}

        nombre_limpio = nombre.strip()
        cargo_limpio = cargo.strip()
        if nombre_limpio == "" or cargo_limpio == "":
            return {}

        repo = JsonRepository(_ruta_json_por_defecto())
        db = repo.loadDatabase()

        nuevo_empleado: Empleado = {
            "id": _siguiente_id_empleado(db),
            "nombre": nombre_limpio,
            "cargo": cargo_limpio,
            "contratos": [],
        }
        db["empleados"].append(nuevo_empleado)

        if not repo.saveDatabase(db):
            return {}

        return nuevo_empleado
    except Exception:
        return {}


def eliminar_empleado(id) -> bool:
    """
    Elimina un empleado por id.

    Input: id (int)
    Output: bool (True si se eliminó, False en caso contrario)
    """

    try:
        employee_id = int(id)

        repo = JsonRepository(_ruta_json_por_defecto())
        db = repo.loadDatabase()

        employees = db.get("empleados", [])
        for idx, employee in enumerate(employees):
            if isinstance(employee, dict) and employee.get("id") == employee_id:
                del employees[idx]
                return repo.saveDatabase(db)

        return False
    except Exception:
        return False


def buscar_empleado(id) -> dict:
    """
    Busca un empleado por id.

    Input: id (int)
    Output: dict (empleado) o dict vacío si no existe / no es válido
    """

    try:
        employee_id = int(id)

        repo = JsonRepository(_ruta_json_por_defecto())
        db = repo.loadDatabase()

        employee = _buscar_empleado_por_id(db, employee_id)
        return employee if employee is not None else {}
    except Exception:
        return {}

