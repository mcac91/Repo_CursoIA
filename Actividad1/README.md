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

## Mejoras identificadas (no implementadas)

Tras la validación completa del proyecto se han identificado varias mejoras y optimizaciones que podrían aumentar la calidad y funcionalidad del sistema. Sin embargo, estas mejoras no se han implementado con el objetivo de evitar un mayor consumo de tokens de IA.

Las mejoras detectadas son las siguientes:

- **Mejora 1: Visualización de datos en CLI más legible**  
  Mejorar el formato de salida en terminal para presentar la información de forma más clara y estructurada, facilitando la lectura y comprensión por parte del usuario.

- **Mejora 2: Validación inmediata de campos introducidos**  
  Implementar una validación en tiempo real que permita detectar y notificar errores en los campos en el momento en que se introducen, evitando esperar hasta la finalización del proceso y proporcionando mensajes de error más específicos.

- **Mejora 3: Actualización de empleados y contratos mediante ID**  
  Añadir la funcionalidad de actualización de registros de empleados y contratos utilizando su identificador (ID), permitiendo modificar datos existentes de forma más directa y eficiente.

Estas mejoras quedan registradas como posibles ampliaciones para futuras versiones del proyecto.

