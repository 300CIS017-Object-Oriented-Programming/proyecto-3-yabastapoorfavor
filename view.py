
class View:
    def __init__(self):
        ruta1 = "inputs/programas.csv"
        ruta2 = "inputs/admitidos"
        ruta3 = "inputs/graduados"
        ruta4 = "inputs/inscritos"
        ruta5 = "inputs/matriculados"
        ruta6 = "inputs/matriculadosPrimerSemestre"
        ruta7 = "outputs/"
        self.controlador = SNIESController(ruta1, ruta2, ruta3, ruta4, ruta5, ruta6, ruta7)

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
        print("Además, todos los archivo CSV del SNIES deben estar correctamente ubicados.")

        user_answer = input("¿Ha parametrizado el programa correctamente? (Y/N): ").lower()
        if self.validar_entrada(user_answer, False):
            anio1 = input("Escriba el primer año de búsqueda: ")
            self.validar_entrada(anio1, True)
            anio2 = input("Escriba el segundo año de búsqueda: ")
            self.validar_entrada(anio2, True)
            anio1, anio2 = self.organizar_anios(anio1, anio2)
            print("Procesando datos ...")
            self.controlador.procesar_datos_csv(anio1, anio2)
            print("Datos procesados con éxito!")
            return True
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

    def mostrar_datos_extra(self):
        print("A continuación vamos a mostrar datos relevantes de los programas académicos seleccionados.")
        print("¿Desea convertir los datos a un archivo CSV, TXT o JSON? (Y/N): ")
        opcion_yn = self.validar_entrada_yn()
        self.controlador.calcular_datos_extra(opcion_yn)

    def buscar_por_palabra_clave_y_formacion(self):
        opcion_yn = 'y'
        while opcion_yn == 'y':
            opcion_yn = input("¿Desea hacer una búsqueda por palabra clave del nombre del programa? (Y/N): ").lower()
            if opcion_yn == 'y':
                convertir_csv = input("¿Deseas convertir los datos del programa académico a un CSV? (Y/N): ").lower() == 'y'
                palabra_clave = input("Escriba la palabra clave para buscar los programas por nombre: ")
                print("Seleccione un nivel de formación para filtrar:")
                print("1->Especialización Universitaria\n2->Maestría\n3->Doctorado\n4->Formación Técnica Profesional\n"
                      "5->Tecnológico\n6->Universitario\n7->Especialización Técnico Profesional\n8->Especialización Tecnológica\n"
                      "10->Especialización Médico Quirúrgica")
                id_formacion_academica = int(input("Seleccione una opción: "))
                while id_formacion_academica not in range(1, 11) or id_formacion_academica == 9:
                    print("Seleccione una opción entre 1-10 excluyendo el 9.")
                    id_formacion_academica = int(input("Seleccione una opción: "))
                self.controlador.buscar_programas(convertir_csv, palabra_clave, id_formacion_academica)

    def salir(self):
        print("Cerrando programa...")
        print("Recuerde revisar la carpeta de outputs para los archivos .csv exportados.")
        print("Programa cerrado con éxito!")


def main():
    menu = View()
    if menu.mostrar_pantalla_bienvenido():
        menu.mostrar_datos_extra()
        menu.buscar_por_palabra_clave_y_formacion()
    menu.salir()


if __name__ == "__main__":
    main()