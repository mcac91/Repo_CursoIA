"""
Pruebas unitarias para gestor_contratos.py
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from app.gestor_empleados import agregar_empleado, buscar_empleado
from app.gestor_contratos import asociar_contrato, listar_contratos_vencidos


def test_asociar_contrato_valido(monkeypatch, tmp_path):
    """
    Prueba asociar contrato válido.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)
    monkeypatch.setattr("app.gestor_contratos._ruta_json_por_defecto", lambda: json_path)

    # Agregar empleado
    emp = agregar_empleado("Juan", "Dev")
    assert emp

    # Asociar contrato
    contrato = asociar_contrato(emp["id"], "2026-01-01", "2026-12-31", 30000)
    assert isinstance(contrato, dict)
    assert contrato["id_contrato"] == 1
    assert contrato["fecha_inicio"] == "2026-01-01"
    assert contrato["salario"] == 30000

    # Verificar que se agregó al empleado
    emp_actualizado = buscar_empleado(emp["id"])
    assert len(emp_actualizado["contratos"]) == 1
    assert emp_actualizado["contratos"][0]["id_contrato"] == 1


def test_asociar_contrato_invalido(monkeypatch, tmp_path):
    """
    Prueba asociar contrato con datos inválidos.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)
    monkeypatch.setattr("app.gestor_contratos._ruta_json_por_defecto", lambda: json_path)

    emp = agregar_empleado("Juan", "Dev")

    # Salario 0
    contrato = asociar_contrato(emp["id"], "2026-01-01", "2026-12-31", 0)
    assert contrato == {}

    # Fecha inválida
    contrato = asociar_contrato(emp["id"], "2026-13-01", "2026-12-31", 30000)
    assert contrato == {}

    # Fecha fin antes de inicio
    contrato = asociar_contrato(emp["id"], "2026-12-31", "2026-01-01", 30000)
    assert contrato == {}

    # Empleado inexistente
    contrato = asociar_contrato(999, "2026-01-01", "2026-12-31", 30000)
    assert contrato == {}


def test_listar_contratos_vencidos(monkeypatch, tmp_path):
    """
    Prueba listar contratos vencidos.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)
    monkeypatch.setattr("app.gestor_contratos._ruta_json_por_defecto", lambda: json_path)

    emp = agregar_empleado("Juan", "Dev")

    # Contrato vencido (fecha anterior a hoy, 2026)
    asociar_contrato(emp["id"], "2023-01-01", "2023-12-31", 25000)

    # Contrato no vencido
    asociar_contrato(emp["id"], "2026-01-01", "2026-12-31", 30000)

    vencidos = listar_contratos_vencidos()
    assert len(vencidos) == 1
    assert vencidos[0]["id_empleado"] == emp["id"]
    assert vencidos[0]["contrato"]["salario"] == 25000


def test_empleado_puede_tener_contrato(monkeypatch, tmp_path):
    """
    Prueba que un empleado puede tener contrato (integración).
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)
    monkeypatch.setattr("app.gestor_contratos._ruta_json_por_defecto", lambda: json_path)

    # Agregar empleado
    emp = agregar_empleado("María", "Analista")
    assert emp["contratos"] == []

    # Asociar contrato
    contrato = asociar_contrato(emp["id"], "2025-01-01", "2025-12-31", 35000)
    assert contrato

    # Verificar
    emp_actualizado = buscar_empleado(emp["id"])
    assert len(emp_actualizado["contratos"]) == 1
    assert emp_actualizado["contratos"][0]["salario"] == 35000


def test_listar_contratos_vencidos_con_fecha_invalida(monkeypatch, tmp_path):
    """
    Prueba listar contratos vencidos con fecha inválida en contrato.
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)
    monkeypatch.setattr("app.gestor_contratos._ruta_json_por_defecto", lambda: json_path)

    emp = agregar_empleado("Juan", "Dev")

    # Agregar contrato con fecha inválida manualmente para test
    from app.repository import JsonRepository
    repo = JsonRepository(json_path)
    db = repo.loadDatabase()
    db["empleados"][0]["contratos"].append({
        "id_contrato": 1,
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "invalid-date",
        "salario": 30000
    })
    repo.saveDatabase(db)

    # Listar no debe fallar
    vencidos = listar_contratos_vencidos()
    assert isinstance(vencidos, list)  # No crash


def test_asociar_contrato_excepcion_general(monkeypatch, tmp_path):
    """
    Prueba asociar contrato con excepción general (saveDatabase falla).
    """
    json_path = tmp_path / "empleados.json"
    monkeypatch.setattr("app.gestor_empleados._ruta_json_por_defecto", lambda: json_path)
    monkeypatch.setattr("app.gestor_contratos._ruta_json_por_defecto", lambda: json_path)

    emp = agregar_empleado("Juan", "Dev")

    # Mock saveDatabase to return False
    with patch("app.gestor_contratos.JsonRepository.saveDatabase", return_value=False):
        contrato = asociar_contrato(emp["id"], "2026-01-01", "2026-12-31", 30000)
        assert contrato == {}