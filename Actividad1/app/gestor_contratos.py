"""
Módulo de gestión de contratos.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from app.models import BaseDatos, Contrato, Empleado
from app.repository import JsonRepository


def _ruta_json_por_defecto() -> Path:
    """
    Construye la ruta por defecto del JSON para esta actividad.

    Input: ninguno
    Output: Path
    """

    return Path(__file__).resolve().parent / "data" / "empleados.json"


def _buscar_empleado_por_id(db: BaseDatos, id_empleado: int) -> Optional[Empleado]:
    """
    Busca un empleado por id.

    Input: db (BaseDatos), id_empleado (int)
    Output: Empleado | None
    """

    for empleado in db.get("empleados", []):
        if isinstance(empleado, dict) and empleado.get("id") == id_empleado:
            return empleado  # type: ignore[return-value]
    return None


def _siguiente_id_contrato(db: BaseDatos) -> int:
    """
    Calcula el siguiente id de contrato incrementando el máximo actual en toda la base de datos.

    Input: db (BaseDatos)
    Output: int
    """

    max_id = 0
    for empleado in db.get("empleados", []):
        if isinstance(empleado, dict):
            for contrato in empleado.get("contratos", []):
                if isinstance(contrato, dict):
                    candidato = contrato.get("id_contrato")
                    if isinstance(candidato, int) and candidato > max_id:
                        max_id = candidato
    return max_id + 1


def _validar_fecha(fecha_str: str) -> bool:
    """
    Valida que la fecha tenga formato YYYY-MM-DD.

    Input: fecha_str (str)
    Output: bool
    """

    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def asociar_contrato(id_empleado, fecha_inicio, fecha_fin, salario) -> dict:
    """
    Asocia un contrato a un empleado existente.

    Input: id_empleado (int), fecha_inicio (str), fecha_fin (str), salario (float | int)
    Output: dict (contrato creado) o dict vacío en caso de fallo
    """

    try:
        # Validar tipos básicos
        if not isinstance(id_empleado, int) or not isinstance(fecha_inicio, str) or not isinstance(fecha_fin, str) or not isinstance(salario, (int, float)):
            return {}

        # Validar formato fechas
        if not _validar_fecha(fecha_inicio) or not _validar_fecha(fecha_fin):
            return {}

        # Validar orden de fechas
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        if fecha_fin_dt < fecha_inicio_dt:
            return {}

        # Validar salario
        if salario <= 0:
            return {}

        # Cargar base de datos
        repo = JsonRepository(_ruta_json_por_defecto())
        db = repo.loadDatabase()

        # Verificar que el empleado existe
        empleado = _buscar_empleado_por_id(db, id_empleado)
        if empleado is None:
            return {}

        # Generar id_contrato
        id_contrato = _siguiente_id_contrato(db)

        # Crear contrato
        nuevo_contrato: Contrato = {
            "id_contrato": id_contrato,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "salario": salario,
        }

        # Agregar a contratos del empleado
        empleado["contratos"].append(nuevo_contrato)

        # Persistir
        if not repo.saveDatabase(db):
            return {}

        return nuevo_contrato
    except Exception:
        return {}


def listar_contratos_vencidos() -> list:
    """
    Lista todos los contratos vencidos (fecha_fin anterior a la fecha actual).

    Input: ninguno
    Output: list (lista de dicts con id_empleado y contrato)
    """

    try:
        repo = JsonRepository(_ruta_json_por_defecto())
        db = repo.loadDatabase()

        hoy = date.today()
        contratos_vencidos = []

        for empleado in db.get("empleados", []):
            if isinstance(empleado, dict):
                id_empleado = empleado.get("id")
                for contrato in empleado.get("contratos", []):
                    if isinstance(contrato, dict):
                        fecha_fin_str = contrato.get("fecha_fin")
                        if isinstance(fecha_fin_str, str):
                            try:
                                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
                                if fecha_fin < hoy:
                                    contratos_vencidos.append({
                                        "id_empleado": id_empleado,
                                        "contrato": contrato
                                    })
                            except ValueError:
                                continue  # Ignorar contratos con fechas inválidas

        return contratos_vencidos
    except Exception:
        return []

