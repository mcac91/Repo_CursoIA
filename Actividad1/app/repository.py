"""
JSON persistence repository.

This is the single point of access to the employees JSON file, enforcing the
immutable JSON schema required by the project.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from app.models import Database


def _emptyDatabase() -> Database:
    """
    Return a valid empty database structure.

    Input: none
    Output: Database
    """

    return {"empleados": []}


def _coerceDatabase(payload: Any) -> Database:
    """
    Coerce an arbitrary JSON payload into a safe Database structure.

    Input: payload (Any)
    Output: Database
    """

    if not isinstance(payload, dict):
        return _emptyDatabase()

    empleados = payload.get("empleados")
    if not isinstance(empleados, list):
        return _emptyDatabase()

    return {"empleados": empleados}  # keep immutable top-level key


@dataclass(frozen=True)
class JsonRepository:
    """
    Repository that loads/saves the database from/to a JSON file.

    Input: jsonPath (Path | str)
    Output: JsonRepository instance
    """

    jsonPath: Path

    def __init__(self, jsonPath: Optional[Path | str] = None) -> None:
        object.__setattr__(
            self,
            "jsonPath",
            Path(jsonPath) if jsonPath is not None else Path("app/data/empleados.json"),
        )

    def loadDatabase(self) -> Database:
        """
        Load the database from disk. If missing/empty/corrupted, return an empty database.

        Input: none
        Output: Database
        """

        try:
            if not self.jsonPath.exists():
                return _emptyDatabase()

            raw = self.jsonPath.read_text(encoding="utf-8").strip()
            if raw == "":
                return _emptyDatabase()

            payload = json.loads(raw)
            return _coerceDatabase(payload)
        except Exception:
            return _emptyDatabase()

    def saveDatabase(self, db: Database) -> bool:
        """
        Save the database to disk, enforcing the immutable JSON schema.

        Input: db (Database)
        Output: bool (True on success, False otherwise)
        """

        try:
            safeDb = _coerceDatabase(db)
            self.jsonPath.parent.mkdir(parents=True, exist_ok=True)
            self.jsonPath.write_text(
                json.dumps(safeDb, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return True
        except Exception:
            return False

