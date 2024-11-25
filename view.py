from SNIESController import SNIESController
from Settings import Settings
from gestores import GestorXlsx, GestorCsv, GestorJson


class View:
    def __init__(self):
        self.controlador = SNIESController()

    @staticmethod
    def is_convertible_to_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def validar_entrada(self, entrada, es_anio=False):
        while True:
            if es_anio:
                if self.is_convertible_to_int(entrada):
                    return True
                else:
                    entrada = input("El valor ingresado fue inválido. Por favor, ingrese un año válido: ")
            else:
                entrada = input("Si ya hizo esto, escriba 'Y', de lo contrario 'N', y presione Enter: ").lower()
                if entrada in ['y', 'n']:
                    return entrada == 'y'
                else:
                    print("Entrada no válida. Por favor ingrese 'Y' o 'N'.")

    def organizar_anios(self, anio1, anio2):
        if int(anio2) < int(anio1):
            anio1, anio2 = anio2, anio1
        return anio1, anio2

    def mostrar_pantalla_bienvenido(self):
        print("Bienvenido al SNIES-Extractor!")
        print("=========================================")
        print("Recuerde que para el correcto funcionamiento del programa tuvo que haber parametrizado")
        print("la carpeta SNIES_EXTRACTOR en el disco duro C:, con sus respectivas carpetas inputs y outputs.")
        print("Además, todos los archivos CSV del SNIES deben estar correctamente ubicados.")

        user_answer = input("¿Ha parametrizado el programa correctamente? (Y/N): ").lower()
        if self.validar_entrada(user_answer, False):
            anio1 = input("Escriba el primer año de búsqueda: ")
            self.validar_entrada(anio1, True)
            anio2 = input("Escriba el segundo año de búsqueda: ")
            self.validar_entrada(anio2, True)

            # Solicitar palabra clave
            palabra_clave = input("Ingrese la palabra clave para filtrar los datos: ")
            if not palabra_clave.strip():
                print("Debe ingresar una palabra clave válida.")
                return False

            anio1, anio2 = self.organizar_anios(anio1, anio2)
            print("Procesando datos ...")

            # Asegurarse de que los parámetros adicionales estén definidos antes de pasarlos
            def_temp = self.controlador.procesar_datos(anio1, anio2, palabra_clave)

            # Preguntar por el formato de salida
            print("Seleccione el formato de archivo para exportar los datos:")
            print("1. XLSX")
            print("2. CSV")
            print("3. JSON")
            formato = input("Ingrese el número correspondiente al formato deseado: ").strip()

            if formato == "1":
                gestor = GestorXlsx()
                ruta_salida = Settings.OUTPUTS_PATH_XLSX
            elif formato == "2":
                gestor = GestorCsv()
                ruta_salida = Settings.OUTPUTS_PATH_CSV
            elif formato == "3":
                gestor = GestorJson()
                ruta_salida = Settings.OUTPUTS_PATH_JSON
            else:
                print("Formato no válido. Operación cancelada.")
                return False

            if gestor.crear_archivo(ruta_salida, def_temp):
                print(f"Datos exportados con éxito en el archivo: {ruta_salida}")
                return True
            else:
                print("Error al exportar los datos.")
                return False

        return False


    @staticmethod
    def validar_entrada_yn():
        while True:
            opcion = input("Por favor, ingrese 'Y' o 'N': ").lower()
            if opcion == 'y':
                return True
            elif opcion == 'n':
                return False
            else:
                print("Entrada inválida. Intente nuevamente.")



    def salir(self):
        print("Cerrando programa...")
        print("Recuerde revisar la carpeta de outputs para los archivos exportados.")
        print("Programa cerrado con éxito!")

