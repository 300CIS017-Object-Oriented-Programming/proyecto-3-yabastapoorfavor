import csv
from typing import Dict, List, Optional

class SNIESController:
    def __init__(self):
        self.programas_academicos: Dict[int, ProgramaAcademico] = {}
        self.gestor_csv = GestorCsv()
        self.etiquetas_columnas: List[str] = []
        self.ruta_programas_csv = Settings.PROGRAMAS_FILTRAR_FILE_PATH
        self.ruta_admitidos = Settings.ADMITIDOS_FILE_PATH
        self.ruta_graduados = Settings.GRADUADOS_FILE_PATH
        self.ruta_inscritos = Settings.INSCRITOS_FILE_PATH
        self.ruta_matriculados = Settings.MATRICULADOS_FILE_PATH
        self.ruta_matriculados_primer_semestre = Settings.MATRICULADOS_PRIMER_SEMESTRE_FILE_PATH
        self.ruta_output = Settings.OUTPUTS_PATH

    def __del__(self):
        for programa in self.programas_academicos.values():
            del programa

    def procesar_datos_csv(self, ano1: str, ano2: str):
        codigos_snies = self.gestor_csv.leer_programas_csv(self.ruta_programas_csv)
        programas_academicos_vector = self.gestor_csv.leer_archivo_primera(self.ruta_admitidos, ano1, codigos_snies)
        self.etiquetas_columnas = programas_academicos_vector[0]
        columnas_map = {col: idx for idx, col in enumerate(self.etiquetas_columnas)}

        for i in range(1, len(programas_academicos_vector), Settings.DATOS_ACADEM_DEMOGRAF):
            programa_academico = ProgramaAcademico()
            # Fill in the attributes from the columns in the CSV
            programa_academico.set_codigo_de_la_institucion(
                int(programas_academicos_vector[i][columnas_map["CÓDIGO DE LA INSTITUCIÓN"]]))
            # (continue setting other fields similarly...)

            consolidado = [Consolidado() for _ in range(Settings.DATOS_ACADEM_DEMOGRAF)]
            for m in range(Settings.DATOS_ACADEM_DEMOGRAF):
                consolidado[m].set_id_sexo(int(programas_academicos_vector[i + m][columnas_map["ID SEXO"]]))
                # (continue setting other fields similarly...)
                programa_academico.set_consolidado(consolidado[m], m)

            self.programas_academicos[programa_academico.get_codigo_snies_del_programa()] = programa_academico

        # Repeat this structure for the remaining data sources (ruta_admitidos, ruta_graduados, etc.)
        # Fill additional fields based on Settings constants

        # Output generation
        opcion = int(input("Desea generar un archivo CSV (1), TXT (2) o JSON (3): "))
        if opcion == 1:
            gestor_aux = GestorCsv()
        elif opcion == 2:
            gestor_aux = GestorTxt()
        else:
            gestor_aux = GestorJson()
        gestor_aux.crear_archivo(self.ruta_output, self.programas_academicos, self.etiquetas_columnas)

    def buscar_programas(self, flag, palabra_clave, id_comparacion):
        lista_programas = []

        try:
            # Filtrar programas por palabra clave y nivel de formación
            for programa in self.programas_academicos.values():
                nombre = programa.get_programa_academico()
                id_nivel = programa.get_id_nivel_de_formacion()

                if palabra_clave in nombre and id_nivel == id_comparacion:
                    lista_programas.append(programa)
                    print(f"{programa.get_codigo_snies_del_programa()};{programa.get_programa_academico()};"
                          f"{programa.get_codigo_de_la_institucion()};{programa.get_institucion_de_educacion_superior_ies()};"
                          f"{programa.get_metodologia()}")

            # Generar archivo si flag es True
            if flag:
                opcion = int(input("Desea generar un archivo CSV (1), TXT (2) o JSON (3): "))
                if opcion not in [1, 2, 3]:
                    raise ValueError("Opción no válida. Debe ser 1, 2 o 3.")

                if opcion == 1:
                    gestor = GestorCsv()
                elif opcion == 2:
                    gestor = GestorTxt()
                else:
                    gestor = GestorJson()

                gestor.crear_archivo_buscados(self.ruta_output, lista_programas, self.etiquetas_columnas)

        except ValueError as e:
            print(f"Error: {e}")
        except MemoryError as e:
            print(f"Error de memoria: {e}")
        except Exception as e:
            print(f"Se produjo un error: {e}")
        except:
            print("Se produjo un error desconocido.")

    def calcular_datos_extra(self, flag):
        matriz_final = []
        matriz_etiquetas1 = [
            ["Suma Estudiantes Matriculados de Programas Seleccionados (Presencial o Virtual) Primer año",
             "Suma Estudiantes Matriculados de Programas Seleccionados (Presencial o Virtual)"]]
        matriz_etiquetas2 = [
            ["Codigo Snies", "Nombre del Programa", "Nombre del Institucion", "Diferencial porcentual anual de NEOS"]]
        matriz_etiquetas3 = [["Codigo Snies", "Nombre del Programa sin NEOS en los ultimos 3 semestres"]]

        suma_primer_ano = 0
        suma_segundo_ano = 0

        for programa in self.programas_academicos.values():
            neos_primer_ano = 0
            neos_segundo_ano = 0

            id_metodologia = programa.get_id_metodologia()
            if id_metodologia in [1, 3]:
                for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                    consolidado = programa.get_consolidado(i)
                    suma_primer_ano += consolidado.get_matriculados()

                for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                    consolidado = programa.get_consolidado(i + 4)
                    suma_segundo_ano += consolidado.get_matriculados()

            for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                consolidado = programa.get_consolidado(i)
                neos_primer_ano += consolidado.get_matriculados_primer_semestre()

            for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                consolidado = programa.get_consolidado(i + 4)
                neos_segundo_ano += consolidado.get_matriculados_primer_semestre()

            diferencia_neos = (
                        (neos_segundo_ano - neos_primer_ano) * 100 / neos_primer_ano) if neos_primer_ano != 0 else 0
            matriz_etiquetas2.append([
                str(programa.get_codigo_snies_del_programa()),
                programa.get_programa_academico(),
                programa.get_institucion_de_educacion_superior_ies(),
                str(diferencia_neos)
            ])

            neos_sin_estudiantes = all(
                programa.get_consolidado(i).get_matriculados_primer_semestre() == 0 for i in range(3)
            ) or all(
                programa.get_consolidado(i + 1).get_matriculados_primer_semestre() == 0 for i in range(3)
            )
            if neos_sin_estudiantes:
                matriz_etiquetas3.append(
                    [str(programa.get_codigo_snies_del_programa()), programa.get_programa_academico()])

        matriz_etiquetas1.append([str(suma_primer_ano), str(suma_segundo_ano)])
        matriz_final.extend(matriz_etiquetas1 + matriz_etiquetas2 + matriz_etiquetas3)

        for fila in matriz_final:
            print(";".join(fila))

        if flag:
            opcion = int(input("Desea generar un archivo CSV (1), TXT (2) o JSON (3): "))
            if opcion == 1:
                gestor = GestorCsv()
            elif opcion == 2:
                gestor = GestorTxt()
            else:
                gestor = GestorJson()

            gestor.crear_archivo_extra(self.ruta_output, matriz_final)