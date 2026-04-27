# Memoria del proyecto: pasos de implementación

Proyecto: **Sistema de directorio de empleados y contratos** (Python + JSON + Pytest)

Este documento define **los pasos a ejecutar** para implementar la aplicación de forma incremental.  
Cada bloque termina con un **punto de control** para que el desarrollador confirme si se continúa al siguiente paso.

---

## 0) Reglas y criterios (baseline)

- **Arquitectura por módulos (obligatoria)**:
  - `gestor_empleados.py`: lógica de empleados.
  - `gestor_contratos.py`: lógica de contratos.
  - `main.py`: interfaz CLI (sin acceso directo al JSON).
- **Persistencia centralizada**:
  - Todo acceso a `empleados.json` pasa por una única clase/repositorio (p. ej. `JsonRepository`).
- **Formato JSON inmutable**:
  - Estructura exacta:
    - `{ "empleados": [ { "id": ..., "nombre": ..., "cargo": ..., "contratos": [...] } ] }`
  - No se cambian los nombres de claves.
- **IDs autogenerados**:
  - `id` empleado y `id_contrato` se generan incrementando el mayor existente.
- **Firmas mínimas obligatorias (no romper firma)**:
  - En `gestor_empleados.py`:
    - `agregar_empleado(nombre, cargo) -> dict`
    - `eliminar_empleado(id) -> bool`
    - `buscar_empleado(id) -> dict`
  - En `gestor_contratos.py`:
    - `asociar_contrato(id_empleado, fecha_inicio, fecha_fin, salario) -> dict`
    - `listar_contratos_vencidos() -> list`
- **Validación básica obligatoria**:
  - `nombre` y `cargo` no vacíos.
  - `salario > 0`
  - `fechas` con formato `YYYY-MM-DD`
  - `fecha_fin >= fecha_inicio`
- **Contratos dentro del empleado**:
  - Los contratos viven en `empleado["contratos"]`.
- **Gestión de errores controlada**:
  - En gestores, devolver `None`, `False` o listas vacías cuando corresponda (evitar excepciones sin controlar).
  - En `main.py`, capturar y manejar errores sin “reventar” la ejecución.
- **Reglas Python del proyecto (`.cursor/rules/cursor.mdc`)**:
  - **Funciones en `lowerCamelCase`**.
  - **Código en inglés** (nombres, mensajes, variables).
  - **Todas las funciones documentadas en inglés**, incluyendo inputs/outputs si aplica.

**Punto de control (confirmación requerida):** validar que estas reglas son el “contrato” de implementación antes de escribir código.

---

## 1) Estructura inicial del proyecto ✅ (COMPLETADO)

Crear/validar la estructura mínima:

- `gestor_empleados.py`
- `gestor_contratos.py`
- `main.py`
- `empleados.json` (autogenerable; puede crearse vacío en runtime si no existe)
- `tests/` (pytest)
- `README.md`

Definir también (si aplica al repositorio) `.gitignore` para excluir artefactos típicos (`__pycache__/`, `.pytest_cache/`, etc.).

**Punto de control (confirmación requerida):** estructura creada y ejecutable el esqueleto (aunque aún no haga nada). **Estado: completado.**

---

## 2) Definir el modelo de datos y convenciones internas

Establecer las convenciones internas (en inglés) para los diccionarios:

- **Empleado**:
  - `id: int`
  - `nombre: str`
  - `cargo: str`
  - `contratos: list[Contrato]`
- **Contrato** (dentro de `contratos`):
  - `id_contrato: int`
  - `fecha_inicio: str` (`YYYY-MM-DD`)
  - `fecha_fin: str` (`YYYY-MM-DD`)
  - `salario: float | int` (positivo)

Nota: aunque las claves JSON están fijadas por el enunciado en español (`nombre`, `cargo`, `contratos`), el **código** (variables, funciones, mensajes) debe estar en inglés.

**Punto de control (confirmación requerida):** confirmar que estas claves y tipos son los usados en toda la app.

---

## 3) Implementar repositorio de persistencia (`JsonRepository`)

Crear una clase repositorio responsable de:

- **Cargar** datos desde `empleados.json`:
  - Si no existe, iniciar con `{ "empleados": [] }`.
  - Si existe pero está vacío/corrupto, devolver un estado seguro (p. ej. estructura vacía) de forma controlada.
- **Guardar** datos manteniendo el formato inmutable.

Requisitos clave:

- Nadie fuera del repositorio lee/escribe el JSON.
- Las operaciones devuelven resultados controlados (sin excepciones no manejadas propagándose a `main.py`).

**Punto de control (confirmación requerida):** persistencia funcionando (leer/guardar) y formato JSON inmutable garantizado.

---

## 4) Implementar `gestor_empleados.py` (métodos obligatorios)

Implementar exactamente estas funciones (en `lowerCamelCase`) y documentarlas en inglés:

- `agregar_empleado(nombre, cargo) -> dict`
  - Validar `nombre` y `cargo` no vacíos.
  - Autogenerar `id`.
  - Crear empleado con `contratos: []`.
  - Persistir cambios vía repositorio.
  - En caso de fallo/validación: devolver `None` (o dict vacío) según criterio consistente.

- `eliminar_empleado(id) -> bool`
  - Si existe, eliminar, persistir, devolver `True`.
  - Si no existe o falla, devolver `False`.

- `buscar_empleado(id) -> dict`
  - Si existe, devolver dict del empleado.
  - Si no existe, devolver `None` (o dict vacío) de forma consistente.

**Punto de control (confirmación requerida):** operaciones de empleado completas, con validación y persistencia centralizada.

---

## 5) Implementar `gestor_contratos.py` (métodos obligatorios)

Implementar exactamente estas funciones (en `lowerCamelCase`) y documentarlas en inglés:

- `asociar_contrato(id_empleado, fecha_inicio, fecha_fin, salario) -> dict`
  - Validar:
    - formato fechas `YYYY-MM-DD`
    - `fecha_fin >= fecha_inicio`
    - `salario > 0`
  - Verificar que el empleado existe.
  - Autogenerar `id_contrato` incremental (a partir del máximo existente en todos los contratos del empleado, o global; definir criterio y mantenerlo).
  - Insertar contrato en `empleado["contratos"]`.
  - Persistir cambios vía repositorio.
  - En caso de fallo/validación: devolver `None` (o dict vacío) de forma consistente.

- `listar_contratos_vencidos() -> list`
  - Evaluar contratos cuya `fecha_fin` sea anterior a la fecha actual.
  - Devolver lista (vacía si no hay).

**Punto de control (confirmación requerida):** contratos asociados correctamente y listado de vencidos fiable.

---

## 6) Implementar `main.py` (CLI mínima obligatoria)

Construir un menú CLI claro y minimalista con, como mínimo:

- Agregar empleado
- Eliminar empleado
- Buscar empleado
- Asociar contrato
- Listar contratos vencidos
- Salir

Requisitos:

- `main.py` **no** accede directamente al JSON.
- Manejo de errores controlado (entradas inválidas, ids no numéricos, fechas mal formadas, etc.).
- Mensajes y textos del CLI en inglés (por regla del proyecto).

**Punto de control (confirmación requerida):** flujo CLI completo y estable sin crashes.

---

## 7) Pruebas unitarias (`pytest`)

Crear `tests/` con pruebas para:

- Agregar empleado
- Eliminar empleado
- Buscar empleado
- Verificar que un empleado puede tener contrato

Regla crítica:

- Las pruebas **no** deben usar el `empleados.json` real del proyecto:
  - Usar archivo temporal/fixture (p. ej. `tmp_path`) e inyectarlo al repositorio.

**Punto de control (confirmación requerida):** `pytest` pasa en limpio (todas las pruebas en verde).

---

## 8) README y entrega

Crear `README.md` incluyendo:

- Objetivo
- Instalación
- Ejecución
- Ejemplo de uso

Preparar entrega final:

- Estructura final acorde a lo requerido.
- `empleados.json` autogenerable (no imprescindible incluirlo con datos).
- ZIP con nombre exacto: `actmod2_nombre_apellido.zip`

**Punto de control (confirmación requerida):** documentación completa y empaquetado conforme al formato.

---

## Checklist final de cumplimiento

- [ ] Firmas mínimas implementadas sin cambios.
- [ ] Persistencia centralizada (solo repositorio toca JSON).
- [ ] JSON con estructura y claves inmutables.
- [ ] IDs autogenerados incrementalmente.
- [ ] Validaciones: no vacíos, salario \(> 0\), fechas `YYYY-MM-DD`, orden de fechas.
- [ ] Contratos dentro de `empleado["contratos"]`.
- [ ] Errores controlados (gestores devuelven valores “seguros”; CLI no revienta).
- [ ] Código en inglés; funciones `lowerCamelCase`; docstrings en inglés con inputs/outputs.
- [ ] Tests aislados del JSON real (tmp/fixture).
- [ ] README completo y ZIP final con nombre exacto.

