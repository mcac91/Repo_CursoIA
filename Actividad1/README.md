# Actividad Modular 2 — Sistema de Directorio de Empleados y Contratos (Python + JSON + Pytest)

## Objetivo

Desarrollar una aplicación CLI modular para gestionar empleados y sus contratos laborales, con persistencia en un archivo JSON. La aplicación permite agregar, eliminar y buscar empleados, así como asociar contratos y listar contratos vencidos.

## Instalación

1. Asegúrese de tener Python 3.8 o superior instalado.
2. Instale las dependencias (si hay alguna adicional, pero en este proyecto solo se usa la biblioteca estándar de Python).
3. Clone o descargue el proyecto en un directorio local.

## Ejecución

Para ejecutar la aplicación:

```bash
cd Actividad1
python -m app.main
```

Esto iniciará el menú CLI interactivo.

## Ejemplo de Uso

1. **Agregar un empleado:**
   - Seleccione opción 1.
   - Ingrese nombre: "Juan Pérez"
   - Ingrese cargo: "Desarrollador"
   - Resultado: Empleado agregado con ID autogenerado.

2. **Asociar un contrato:**
   - Seleccione opción 4.
   - Ingrese ID del empleado: 1
   - Ingrese fecha de inicio: 2024-01-01
   - Ingrese fecha de fin: 2024-12-31
   - Ingrese salario: 30000
   - Resultado: Contrato asociado.

3. **Buscar un empleado:**
   - Seleccione opción 3.
   - Ingrese ID: 1
   - Resultado: Muestra los detalles del empleado, incluyendo contratos.

4. **Listar contratos vencidos:**
   - Seleccione opción 5.
   - Resultado: Lista contratos cuya fecha de fin es anterior a la fecha actual.

5. **Eliminar un empleado:**
   - Seleccione opción 2.
   - Ingrese ID: 1
   - Resultado: Empleado eliminado.

Para salir, seleccione opción 6.

## Estructura del Proyecto

- `app/`: Código fuente principal.
  - `main.py`: Punto de entrada CLI.
  - `gestor_empleados.py`: Lógica de gestión de empleados.
  - `gestor_contratos.py`: Lógica de gestión de contratos.
  - `repository.py`: Repositorio para persistencia JSON.
  - `models.py`: Definiciones de tipos de datos.
- `tests/`: Pruebas unitarias con pytest.
- `steps.md`: Memoria del proyecto y pasos de implementación.
- `empleados.json`: Archivo de datos autogenerable (no incluido inicialmente).

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
cd Actividad1
python -m pytest tests/
```

Todas las pruebas pasan y usan archivos temporales para no afectar el JSON real.

## Entrega

El proyecto se empaqueta en un archivo ZIP con nombre `actmod2_nombre_apellido.zip`, incluyendo toda la estructura y archivos necesarios.

