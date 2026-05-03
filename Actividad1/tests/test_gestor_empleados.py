"""
Pruebas unitarias para gestor_empleados.py
"""

import pytest
from pathlib import Path

from app.gestor_empleados import agregar_empleado, eliminar_empleado, buscar_empleado


def test_agregar_empleado_valido(monkeypatch, tmp_path):
    """
    Prueba agregar empleado válido.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    resultado = agregar_empleado("Juan Pérez", "Desarrollador")
    assert isinstance(resultado, dict)
    assert resultado["id"] == 1
    assert resultado["nombre"] == "Juan Pérez"
    assert resultado["cargo"] == "Desarrollador"
    assert resultado["contratos"] == []


def test_agregar_empleado_invalido(monkeypatch, tmp_path):
    """
    Prueba agregar empleado con datos inválidos.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    # Nombre vacío
    resultado = agregar_empleado("", "Desarrollador")
    assert resultado == {}

    # Cargo vacío
    resultado = agregar_empleado("Juan", "")
    assert resultado == {}


def test_eliminar_empleado_existente(monkeypatch, tmp_path):
    """
    Prueba eliminar empleado existente.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    # Agregar primero
    agregar_empleado("Juan", "Dev")
    # Eliminar
    resultado = eliminar_empleado(1)
    assert resultado is True

    # Verificar que no existe
    emp = buscar_empleado(1)
    assert emp == {}


def test_eliminar_empleado_inexistente(monkeypatch, tmp_path):
    """
    Prueba eliminar empleado inexistente.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    resultado = eliminar_empleado(999)
    assert resultado is False


def test_buscar_empleado_existente(monkeypatch, tmp_path):
    """
    Prueba buscar empleado existente.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    agregar_empleado("Ana", "Gerente")
    resultado = buscar_empleado(1)
    assert isinstance(resultado, dict)
    assert resultado["nombre"] == "Ana"


def test_buscar_empleado_inexistente(monkeypatch, tmp_path):
    """
    Prueba buscar empleado inexistente.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    resultado = buscar_empleado(999)
    assert resultado == {}


def test_eliminar_empleado_id_no_numerico(monkeypatch, tmp_path):
    """
    Prueba eliminar empleado con ID no numérico.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    resultado = eliminar_empleado("abc")
    assert resultado is False


def test_buscar_empleado_id_no_numerico(monkeypatch, tmp_path):
    """
    Prueba buscar empleado con ID no numérico.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)

    resultado = buscar_empleado("abc")
    assert resultado == {}