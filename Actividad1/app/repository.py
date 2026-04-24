"""
Repositorio de persistencia en JSON.

Este es el único punto de acceso al fichero JSON de empleados, forzando el
esquema inmutable requerido por el proyecto.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from app.models import BaseDatos


def _base_datos_vacia() -> BaseDatos:
    """
    Devuelve una estructura válida de base de datos vacía.

    Input: ninguno
    Output: BaseDatos
    """

    return {"empleados": []}


def _forzar_base_datos(payload: Any) -> BaseDatos:
    """
    Convierte un payload arbitrario en una estructura BaseDatos segura.

    Input: payload (Any)
    Output: BaseDatos
    """

    if not isinstance(payload, dict):
        return _base_datos_vacia()

    empleados = payload.get("empleados")
    if not isinstance(empleados, list):
        return _base_datos_vacia()

    return {"empleados": empleados}  # mantener clave superior inmutable


@dataclass(frozen=True)
class JsonRepository:
    """
    Repositorio que carga/guarda la base de datos en un fichero JSON.

    Input: jsonPath (Path | str)
    Output: instancia de JsonRepository
    """

    jsonPath: Path

    def __init__(self, jsonPath: Optional[Path | str] = None) -> None:
        object.__setattr__(
            self,
            "jsonPath",
            Path(jsonPath) if jsonPath is not None else Path("app/data/empleados.json"),
        )

    def loadDatabase(self) -> BaseDatos:
        """
        Carga la base de datos desde disco. Si falta/está vacío/está corrupto, devuelve una base vacía.

        Input: ninguno
        Output: BaseDatos
        """

        try:
            if not self.jsonPath.exists():
                return _base_datos_vacia()

            raw = self.jsonPath.read_text(encoding="utf-8").strip()
            if raw == "":
                return _base_datos_vacia()

            payload = json.loads(raw)
            return _forzar_base_datos(payload)
        except Exception:
            return _base_datos_vacia()

    def saveDatabase(self, db: BaseDatos) -> bool:
        """
        Guarda la base de datos en disco, forzando el esquema JSON inmutable.

        Input: db (BaseDatos)
        Output: bool (True si se guardó, False en caso contrario)
        """

        try:
            safeDb = _forzar_base_datos(db)
            self.jsonPath.parent.mkdir(parents=True, exist_ok=True)
            self.jsonPath.write_text(
                json.dumps(safeDb, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return True
        except Exception:
            return False

