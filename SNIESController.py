from typing import Dict, List
from gestores import GestorCsv, GestorJson, GestorXlsx
from programaAcademico import ProgramaAcademico
from Settings import Settings


class SNIESController:
    def __init__(self):
        self.programas_academicos: Dict[int, ProgramaAcademico] = {}
        self.gestor_xlsx = GestorXlsx()
        self.etiquetas_columnas: List[str] = []
        self.ruta_admitidos = Settings.ADMITIDOS_FILE_PATH
        self.ruta_graduados = Settings.GRADUADOS_FILE_PATH
        self.ruta_inscritos = Settings.INSCRITOS_FILE_PATH
        self.ruta_matriculados = Settings.MATRICULADOS_FILE_PATH
        self.ruta_matriculados_primer_curso = Settings.MATRICULADOS_PRIMER_CURSO_FILE_PATH
        self.ruta_output = Settings.OUTPUTS_PATH

    def procesar_datos_csv(self, ano1: str, ano2: str):
        # Leer códigos SNIES desde el archivo de programas
        codigos_snies = self.gestor_xlsx.leer_codigos_snies(self.ruta_admitidos + "2020.xlsx")

        # Leer datos del archivo admitidos
        programas_academicos_vector = self.gestor_xlsx.leer_archivo_primer(self.ruta_admitidos + ano1 + ".xlsx",
                                                                           codigos_snies)

        self.etiquetas_columnas = programas_academicos_vector[0]
        columnas_map = {col: idx for idx, col in enumerate(self.etiquetas_columnas)}

        # Procesar cada programa y consolidar datos
        for i in range(1, len(programas_academicos_vector), Settings.DATOS_ACADEM_DEMOGRAF):
            codigo_snies = int(programas_academicos_vector[i][columnas_map["CÓDIGO SNIES DEL PROGRAMA"]])

            # Crear o actualizar el programa académico

            if codigo_snies not in self.programas_academicos:
                programa_academico = ProgramaAcademico(
                    codigo_de_la_institucion=int(
                        programas_academicos_vector[i][columnas_map["CÓDIGO DE LA INSTITUCIÓN"]]),
                    programa_academico=programas_academicos_vector[i][columnas_map["PROGRAMA ACADÉMICO"]],
                    id_nivel_formacion=int(programas_academicos_vector[i][columnas_map["ID NIVEL DE FORMACIÓN"]]),
                    nivel_formacion=programas_academicos_vector[i][columnas_map["NIVEL DE FORMACIÓN"]],
                    metodologia=programas_academicos_vector[i][columnas_map["METODOLOGÍA"]]
                    # FALTA ANADIR EL RESTO DE DATOS
                )
                self.programas_academicos[codigo_snies] = programa_academico
            else:
                programa_academico = self.programas_academicos[codigo_snies]

            # Buscar y añadir los datos relacionados con "ID SEXO", "ADMITIDOS", etc.
            datos_consolidar = ["INSCRITOS", "ADMITIDOS", "MATRICULADOS",
                               "PRIMER CURSO", "GRADUADOS"]
            rutas_archivos = [
                self.ruta_admitidos + ano1 + ".xlsx", self.ruta_admitidos + ano2 + ".xlsx",
                self.ruta_inscritos + ano1 + ".xlsx", self.ruta_inscritos + ano2 + ".xlsx",
                self.ruta_graduados + ano1 + ".xlsx", self.ruta_graduados + ano2 + ".xlsx",
                self.ruta_matriculados + ano1 + ".xlsx", self.ruta_matriculados + ano2 + ".xlsx",
                self.ruta_matriculados_primer_curso + ano1 + ".xlsx",
                self.ruta_matriculados_primer_curso + ano2 + ".xlsx"
            ]

            # Llamar a la función buscar_datos_codigos_snies para obtener los datos
            datos_consolidados = self.gestor_xlsx.buscar_datos_codigos_snies(codigos_snies, rutas_archivos,
                                                                             datos_consolidar)
            print(datos_consolidados)
            # Agregar los datos consolidados al programa académico
            for fila in datos_consolidados:
                programa_academico.agregar_consolidado(
                    id_sexo=int(fila[1]),
                    sexo=fila[2],
                    ano=fila[3],
                    semestre=fila[4],
                    inscritos=int(fila[5]),
                    admitidos=int(fila[6]),
                    matriculados=int(fila[7]),
                    matriculados_primer_semestre=int(fila[8]),
                    graduados=int(fila[9])
                )

        # Generar archivo de salida
        opcion = int(input("Desea generar un archivo CSV (1), TXT (2) o JSON (3): "))
        if opcion == 1:
            gestor_aux = GestorCsv()
        elif opcion == 2:
            gestor_aux = GestorXlsx()
        else:
            gestor_aux = GestorJson()
        gestor_aux.crear_archivo(self.ruta_output, self.programas_academicos, self.etiquetas_columnas)


    def buscar_programas(self, flag, palabra_clave, id_comparacion):
        lista_programas = []

        try:
            # Filtrar programas por palabra clave y nivel de formación
            for programa in self.programas_academicos.values():
                nombre = programa.programa_academico
                id_nivel = programa.id_nivel_formacion

                if palabra_clave in nombre and id_nivel == id_comparacion:
                    lista_programas.append(programa)
                    print(f"{programa.codigo_snies};{programa.programa_academico};"
                          f"{programa.codigo_de_la_institucion};{programa.institucion_ies};"
                          f"{programa.metodologia}")

            # Generar archivo si flag es True
            if flag:
                opcion = int(input("Desea generar un archivo CSV (1), XLSX (2) o JSON (3): "))
                if opcion not in [1, 2, 3]:
                    raise ValueError("Opción no válida. Debe ser 1, 2 o 3.")

                if opcion == 1:
                    gestor = GestorCsv()
                elif opcion == 2:
                    gestor = GestorXlsx()
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

            id_metodologia = programa.id_metodologia
            if id_metodologia in [1, 3]:
                for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                    consolidado = programa.data.iloc[i]  # Asumiendo que consolidado es un registro en 'data'
                    suma_primer_ano += consolidado["matriculados"]

                for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                    consolidado = programa.data.iloc[i + 4]
                    suma_segundo_ano += consolidado["matriculados"]

            for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                consolidado = programa.data.iloc[i]
                neos_primer_ano += consolidado["matriculadosPrimerSemestre"]

            for i in range(Settings.DATOS_ACADEM_DEMOGRAF):
                consolidado = programa.data.iloc[i + 4]
                neos_segundo_ano += consolidado["matriculadosPrimerSemestre"]

            diferencia_neos = (
                    (neos_segundo_ano - neos_primer_ano) * 100 / neos_primer_ano) if neos_primer_ano != 0 else 0
            matriz_etiquetas2.append([
                str(programa.codigo_snies),
                programa.programa_academico,
                programa.institucion_ies,
                str(diferencia_neos)
            ])

            neos_sin_estudiantes = all(
                programa.data.iloc(i)["matriculadosPrimerSemestre"] == 0 for i in range(3)
            ) or all(
                programa.data.iloc(i + 1)["matriculadosPrimerSemestre"] == 0 for i in range(3)
            )
            if neos_sin_estudiantes:
                matriz_etiquetas3.append(
                    [str(programa.codigo_snies), programa.programa_academico])

        matriz_etiquetas1.append([str(suma_primer_ano), str(suma_segundo_ano)])
        matriz_final.extend(matriz_etiquetas1 + matriz_etiquetas2 + matriz_etiquetas3)

        for fila in matriz_final:
            print(";".join(fila))

        if flag:
            opcion = int(input("Desea generar un archivo CSV (1), XSLX (2) o JSON (3): "))
            if opcion == 1:
                gestor = GestorCsv()
            elif opcion == 2:
                gestor = GestorXlsx()
            else:
                gestor = GestorJson()

            gestor.crear_archivo_extra(self.ruta_output, matriz_final)
