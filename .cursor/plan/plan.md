SDD de Planificación (CIRF + SOLID)

Proyecto: Sistema de directorio de empleados y contratos (Python + JSON + Pytest)

1. CONTEXTO (C)

Se desarrollará una aplicación en Python para gestionar empleados y sus contratos laborales usando almacenamiento en archivo empleados.json.

2. INTENCIÓN (I)

Construir un sistema modular que permita:

Crear, actualizar, eliminar y consultar empleados.
Asociar contratos a empleados.
Consultar contratos vencidos.
Guardar/cargar datos en JSON.
Incluir menú por terminal.
Implementar pruebas unitarias con pytest.

3. RESPUESTA ESPERADA (R)

Entrega final con:

gestor_empleados.py
gestor_contratos.py
main.py
empleados.json (autogenerable)
/tests con pytest
README.md
Zip final: actmod2_nombre_apellido.zip

4. FORMATO (F)
Python 3.x
Persistencia en JSON
Interfaz CLI por terminal
Pruebas con pytest
Estructura limpia y modular

5. REGLAS DE DESARROLLO (por título)
*Regla 1 — Arquitectura Obligatoria por Módulos*

Separar estrictamente:
Empleados → gestor_empleados.py
Contratos → gestor_contratos.py
Interfaz usuario → main.py

*Regla 2 — Principio SOLID (mínimo requerido)*

SRP: cada clase/módulo hace una sola cosa.
OCP: añadir funciones sin modificar lo existente.
DIP: lógica no debe depender directamente del archivo JSON (usar una clase repositorio).

*Regla 3 — Persistencia Centralizada*

Todo acceso a empleados.json debe pasar por una única clase/repositorio (ej: JsonRepository).
Prohibido leer/escribir JSON desde main.py.

*Regla 4 — Formato JSON Inmutable*

El JSON debe mantener esta estructura:

{ "empleados": [ { "id": ..., "nombre": ..., "cargo": ..., "contratos": [...] } ] }

No se permite cambiar nombres de claves.

*Regla 5 — IDs Autogenerados*

Los IDs (id empleado y id_contrato) deben generarse automáticamente incrementando el mayor existente.

*Regla 6 — Métodos Mínimos Obligatorios*

Implementar exactamente estos métodos (sin romper firma):
gestor_empleados.py

agregar_empleado(nombre, cargo) -> dict
eliminar_empleado(id) -> bool
buscar_empleado(id) -> dict

gestor_contratos.py

asociar_contrato(id_empleado, fecha_inicio, fecha_fin, salario) -> dict
listar_contratos_vencidos() -> list

*Regla 7 — Validación Básica Obligatoria*

Validar:

nombre y cargo no vacíos
salario > 0
fechas con formato YYYY-MM-DD
fecha_fin >= fecha_inicio

*Regla 8 — Contratos Siempre Dentro del Empleado*

Los contratos se guardan dentro de la lista "contratos" de cada empleado.

*Regla 9 — Gestión de Errores Controlada*

No lanzar excepciones sin capturarlas en main.py.
Los gestores deben devolver None, False o listas vacías cuando corresponda.

*Regla 10 — CLI Clara y Minimalista*

El menú debe incluir como mínimo:

Agregar empleado
Eliminar empleado
Buscar empleado
Asociar contrato
Listar contratos vencidos
Salir

*Regla 11 — Pruebas Unitarias Obligatorias (pytest)*

Crear pruebas para:

agregar empleado
eliminar empleado
buscar empleado
verificar que un empleado puede tener contrato

*Regla 12 — Pruebas Independientes del JSON Real*

Los tests no deben usar el JSON real del proyecto.
Usar un archivo temporal o fixture.

*Regla 13 — README Obligatorio*

El README debe incluir:

Objetivo
Instalación
Ejecución
Ejemplo de uso

*Regla 14 — Entrega Final*

El proyecto debe empaquetarse en zip con nombre exacto:
actmod2_nombre_apellido.zip
