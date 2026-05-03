"""
Convenciones del modelo de datos para la aplicación.

Este módulo define las estructuras internas de datos usadas en la app,
manteniendo inmutables las claves del JSON requeridas por la especificación.
"""

from __future__ import annotations

from typing import List, TypedDict, Union


Salario = Union[int, float]


class Contrato(TypedDict):
    id_contrato: int
    fecha_inicio: str
    fecha_fin: str
    salario: Salario


class Empleado(TypedDict):
    id: int
    nombre: str
    cargo: str
    contratos: List[Contrato]


class BaseDatos(TypedDict):
    empleados: List[Empleado]


# Backwards-compatible aliases (will be removed later if desired)
Contract = Contrato
Employee = Empleado
Database = BaseDatos

