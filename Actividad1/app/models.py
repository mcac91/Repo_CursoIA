"""
Data model conventions for the application.

This module defines the internal data shapes used across the app while keeping
the JSON keys immutable (Spanish keys required by the spec).
"""

from __future__ import annotations

from typing import List, TypedDict, Union


Salary = Union[int, float]


class Contract(TypedDict):
    id_contrato: int
    fecha_inicio: str
    fecha_fin: str
    salario: Salary


class Employee(TypedDict):
    id: int
    nombre: str
    cargo: str
    contratos: List[Contract]


class Database(TypedDict):
    empleados: List[Employee]

