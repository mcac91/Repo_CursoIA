"""
Pruebas unitarias para repository.py
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from app.repository import JsonRepository, _forzar_base_datos


def test_load_database_archivo_inexistente(tmp_path):
    """
    Prueba cargar base de datos cuando el archivo no existe.
    """
    repo = JsonRepository(tmp_path / "inexistente.json")
    db = repo.loadDatabase()
    assert db == {"empleados": []}


def test_load_database_archivo_vacio(tmp_path):
    """
    Prueba cargar base de datos con archivo vacío.
    """
    json_path = tmp_path / "vacio.json"
    json_path.write_text("")
    repo = JsonRepository(json_path)
    db = repo.loadDatabase()
    assert db == {"empleados": []}


def test_load_database_json_invalido(tmp_path):
    """
    Prueba cargar base de datos con JSON inválido.
    """
    json_path = tmp_path / "invalido.json"
    json_path.write_text("no json")
    repo = JsonRepository(json_path)
    db = repo.loadDatabase()
    assert db == {"empleados": []}


def test_save_database_exito(tmp_path):
    """
    Prueba guardar base de datos exitosamente.
    """
    json_path = tmp_path / "test.json"
    repo = JsonRepository(json_path)
    db = {"empleados": [{"id": 1, "nombre": "Test"}]}
    result = repo.saveDatabase(db)
    assert result is True
    assert json_path.exists()
    loaded = json.loads(json_path.read_text())
    assert loaded == db


def test_forzar_base_datos_no_dict():
    """
    Prueba _forzar_base_datos con payload no dict.
    """
    result = _forzar_base_datos("string")
    assert result == {"empleados": []}


def test_forzar_base_datos_sin_empleados():
    """
    Prueba _forzar_base_datos con dict sin empleados.
    """
    result = _forzar_base_datos({"otros": []})
    assert result == {"empleados": []}