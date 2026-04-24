"""
Punto de entrada CLI para la aplicación de directorio de empleados y contratos.
"""

from app.gestor_empleados import agregar_empleado, eliminar_empleado, buscar_empleado
from app.gestor_contratos import asociar_contrato, listar_contratos_vencidos


def mostrar_menu() -> None:
    """
    Muestra el menú de opciones.
    """
    print("\n--- Sistema de Directorio de Empleados y Contratos ---")
    print("1. Agregar empleado")
    print("2. Eliminar empleado")
    print("3. Buscar empleado")
    print("4. Asociar contrato")
    print("5. Listar contratos vencidos")
    print("6. Salir")
    print("Seleccione una opción (1-6): ", end="")


def main() -> None:
    """
    Función principal del CLI.
    """
    while True:
        mostrar_menu()
        try:
            opcion = input().strip()
            if opcion == "1":
                nombre = input("Ingrese el nombre del empleado: ").strip()
                cargo = input("Ingrese el cargo del empleado: ").strip()
                resultado = agregar_empleado(nombre, cargo)
                if resultado:
                    print(f"Empleado agregado: ID {resultado['id']}, Nombre: {resultado['nombre']}, Cargo: {resultado['cargo']}")
                else:
                    print("Error: No se pudo agregar el empleado. Verifique que nombre y cargo no estén vacíos.")
            elif opcion == "2":
                id_str = input("Ingrese el ID del empleado a eliminar: ").strip()
                try:
                    id_emp = int(id_str)
                    if eliminar_empleado(id_emp):
                        print("Empleado eliminado exitosamente.")
                    else:
                        print("Error: Empleado no encontrado o no se pudo eliminar.")
                except ValueError:
                    print("Error: ID debe ser un número entero.")
            elif opcion == "3":
                id_str = input("Ingrese el ID del empleado a buscar: ").strip()
                try:
                    id_emp = int(id_str)
                    empleado = buscar_empleado(id_emp)
                    if empleado:
                        print(f"Empleado encontrado: {empleado}")
                    else:
                        print("Empleado no encontrado.")
                except ValueError:
                    print("Error: ID debe ser un número entero.")
            elif opcion == "4":
                id_str = input("Ingrese el ID del empleado: ").strip()
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()
                salario_str = input("Ingrese el salario: ").strip()
                try:
                    id_emp = int(id_str)
                    salario = float(salario_str)
                    resultado = asociar_contrato(id_emp, fecha_inicio, fecha_fin, salario)
                    if resultado:
                        print(f"Contrato asociado: ID {resultado['id_contrato']}, Salario: {resultado['salario']}")
                    else:
                        print("Error: No se pudo asociar el contrato. Verifique los datos (empleado existe, fechas válidas, salario > 0).")
                except ValueError:
                    print("Error: ID debe ser entero, salario numérico.")
            elif opcion == "5":
                contratos = listar_contratos_vencidos()
                if contratos:
                    print("Contratos vencidos:")
                    for item in contratos:
                        emp_id = item["id_empleado"]
                        contrato = item["contrato"]
                        print(f"  Empleado ID {emp_id}: Contrato ID {contrato['id_contrato']}, Fin: {contrato['fecha_fin']}, Salario: {contrato['salario']}")
                else:
                    print("No hay contratos vencidos.")
            elif opcion == "6":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()

