import openpyxl
import json
import csv
from openpyxl import Workbook
from programaAcademico import ProgramaAcademico



from typing import List, Dict



class Gestor:

    def crear_archivo(self, ruta: str, mapade_programas_academicos: Dict[int, 'ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        raise NotImplementedError



    def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        raise NotImplementedError



    def crear_archivo_extra(self, ruta: str, datos_a_imprimir: List[List[str]]) -> bool:

        raise NotImplementedError



class GestorCsv(Gestor):

    def crear_archivo(self, ruta: str, mapade_programas_academicos: Dict[int, 'ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        with open(ruta, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file)

            writer.writerow(etiquetas_columnas)  # Escribe las etiquetas de columna

            for programa in mapade_programas_academicos.values():

                writer.writerow(programa.obtener_datos_csv())  # Suponiendo que `obtener_datos_csv` devuelve los datos adecuados

        return True



    def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        with open(ruta, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file)

            writer.writerow(etiquetas_columnas)

            for programa in programas_buscados:

                writer.writerow(programa.obtener_datos_csv())  # Al igual que antes

        return True



    def crear_archivo_extra(self, ruta: str, datos_a_imprimir: List[List[str]]) -> bool:

        with open(ruta, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file)

            for fila in datos_a_imprimir:

                writer.writerow(fila)

        return True



class GestorJson(Gestor):

    def crear_archivo(self, ruta: str, mapade_programas_academicos: Dict[int, 'ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        datos = []

        for programa in mapade_programas_academicos.values():

            datos.append(programa.obtener_datos_json())  # Suponiendo que `obtener_datos_json` devuelve los datos como diccionario

        with open(ruta, 'w', encoding='utf-8') as file:

            json.dump(datos, file, indent=4)

        return True



    def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        datos = []

        for programa in programas_buscados:

            datos.append(programa.obtener_datos_json())  # Al igual que antes

        with open(ruta, 'w', encoding='utf-8') as file:

            json.dump(datos, file, indent=4)

        return True



    def crear_archivo_extra(self, ruta: str, datos_a_imprimir: List[List[str]]) -> bool:

        with open(ruta, 'w', encoding='utf-8') as file:

            json.dump(datos_a_imprimir, file, indent=4)

        return True



class GestorXlsx(Gestor):
        TITULOS_PRIMER_ARCHIVO = [
            "CÓDIGO DE LA INSTITUCIÓN", "IES_PADRE", "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)", "TIPO IES",
            "ID SECTOR IES", "SECTOR IES", "ID CARACTER", "CARACTER IES",
            "CÓDIGO DEL DEPARTAMENTO (IES)", "DEPARTAMENTO DE DOMICILIO DE LA IES",
            "CÓDIGO DEL MUNICIPIO IES", "MUNICIPIO DE DOMICILIO DE LA IES",
            "CÓDIGO SNIES DEL PROGRAMA", "PROGRAMA ACADÉMICO",
            "NÚCLEO BÁSICO DEL CONOCIMIENTO (NBC)", "ID NIVEL ACADÉMICO", "NIVEL ACADÉMICO",
            "ID NIVEL DE FORMACIÓN", "NIVEL DE FORMACIÓN", "ID METODOLOGÍA",
            "METODOLOGÍA", "ID ÁREA DE CONOCIMIENTO", "ÁREA DE CONOCIMIENTO",
            "ID NÚCLEO", "ID CINE CAMPO AMPLIO", "DESC CINE CAMPO AMPLIO",
            "ID CINE CAMPO ESPECIFICO", "DESC CINE CAMPO ESPECIFICO",
            "ID CINE CODIGO DETALLADO", "DESC CINE CODIGO DETALLADO",
            "CÓDIGO DEL DEPARTAMENTO (PROGRAMA)", "DEPARTAMENTO DE OFERTA DEL PROGRAMA",
            "CÓDIGO DEL MUNICIPIO (PROGRAMA)", "MUNICIPIO DE OFERTA DEL PROGRAMA"
        ]

        TITULOS_SEGUNDO_ARCHIVO = [
            "CÓDIGO SNIES DEL PROGRAMA", "ID SEXO", "SEXO", "AÑO", "SEMESTRE"
        ]

        @staticmethod
        def buscar_datos_codigos_snies(codigos_snies, rutas_archivos, datos_consolidar):
            """
            Busca datos específicos de TITULOS_SEGUNDO_ARCHIVO en varios archivos y retorna una lista consolidada.

            Args:
                codigos_snies (List[int]): Lista de códigos SNIES a buscar.
                rutas_archivos (List[str]): Rutas de los archivos XLSX donde buscar.
                titulos_segundo (List[str]): Títulos de las columnas de interés.

            Returns:
                List[List]: Lista de filas donde la primera columna es el código SNIES
                            y las demás columnas son los datos buscados.
            """
            datos_consolidados = []

            for ruta in rutas_archivos:
                try:
                    wb = openpyxl.load_workbook(ruta)
                    sheet = wb.active

                    # Identificar las posiciones de las columnas de interés
                    encabezados = None
                    for row in sheet.iter_rows(min_row=1, values_only=True):
                        if "CÓDIGO SNIES DEL PROGRAMA" in row:
                            encabezados = row
                            break

                    if not encabezados:
                        raise ValueError(f"No se encontraron encabezados en el archivo: {ruta}")

                    # Identificar las posiciones de las columnas de interés
                    pos_codigo_snies = encabezados.index("CÓDIGO SNIES DEL PROGRAMA")
                    posiciones_interes = [encabezados.index(titulo) for titulo in datos_consolidar if
                                          titulo in encabezados]

                    if not posiciones_interes:
                        raise ValueError(f"No se encontraron columnas de interés en el archivo: {ruta}")

                    # Leer las filas y buscar los códigos SNIES
                    for row in sheet.iter_rows(min_row=sheet.min_row + 1, values_only=True):
                        if row[pos_codigo_snies] in codigos_snies:
                            fila = [row[pos_codigo_snies]] + [row[pos] for pos in posiciones_interes]
                            datos_consolidados.append(fila)

                except Exception as e:
                    print(f"Error procesando el archivo {ruta}: {e}")

            return datos_consolidados

        @staticmethod
        def leer_codigos_snies(ruta):
            codigos_snies = set()  # Usar un set para asegurarse de que los valores sean únicos
            try:
                wb = openpyxl.load_workbook(ruta)
                sheet = wb.active

                # Buscar la fila donde comienza el encabezado
                fila_inicio_datos = None
                encabezado_fila = None
                for i, row in enumerate(sheet.iter_rows(min_row=1, values_only=True), start=1):
                    if "CÓDIGO DE LA INSTITUCIÓN" in row:
                        encabezado_fila = row
                        fila_inicio_datos = i + 1  # La fila de datos empieza justo después del encabezado
                        break

                if encabezado_fila is None:
                    raise ValueError("No se encontró la fila con el encabezado 'CÓDIGO DE LA INSTITUCIÓN'.")

                # Obtener los encabezados de la fila encontrada
                encabezados = list(encabezado_fila)

                # Buscar la posición de la columna "CÓDIGO SNIES DEL PROGRAMA"
                if "CÓDIGO SNIES DEL PROGRAMA" in encabezados:
                    columna_codigos_snies = encabezados.index("CÓDIGO SNIES DEL PROGRAMA")
                else:
                    raise ValueError("No se encontró la columna 'CÓDIGO SNIES DEL PROGRAMA' en el archivo.")

                # Leer los valores de la columna, asegurándose de que sean únicos
                for row in sheet.iter_rows(min_row=fila_inicio_datos, values_only=True):
                    if row[columna_codigos_snies] is not None:
                        codigos_snies.add(int(row[columna_codigos_snies]))  # Agregar el código al set

            except Exception as e:
                print(f"Error al leer el archivo: {e}")

            # Convertir el set de nuevo a lista si se necesita un vector
            return list(codigos_snies)

        @staticmethod
        def leer_archivo_primer(ruta, codigos_snies):
            """Lee un archivo XLSX y extrae filas con títulos específicos para el primer caso."""
            return GestorXlsx._leer_archivo(ruta, codigos_snies, GestorXlsx.TITULOS_PRIMER_ARCHIVO)

        @staticmethod
        def leer_archivo_segundo(ruta, codigos_snies):
            """Lee un archivo XLSX y extrae filas con títulos específicos para el segundo caso."""
            return GestorXlsx._leer_archivo(ruta, codigos_snies, GestorXlsx.TITULOS_SEGUNDO_ARCHIVO)

        @staticmethod
        def _leer_archivo(ruta, codigos_snies, titulos_interes):
            """Lógica común para leer archivos XLSX."""
            # Imprimir los códigos SNIES y los títulos de interés
            print("Códigos SNIES:", codigos_snies)
            print("Títulos de interés:", titulos_interes)

            matriz_resultado = []
            try:
                wb = openpyxl.load_workbook(ruta)
                sheet = wb.active
                # Buscar las posiciones de las columnas de interés
                encabezados = None
                for row in sheet.iter_rows(min_row=1, values_only=True):
                    # Buscar la fila que contiene el título "CÓDIGO DE LA INSTITUCIÓN"
                    if "CÓDIGO DE LA INSTITUCIÓN" in row:
                        encabezados = row
                        break

                if not encabezados:
                    raise ValueError("No se encontró la fila con el título 'CÓDIGO DE LA INSTITUCIÓN'.")

                posiciones_interes = [i for i, titulo in enumerate(encabezados) if titulo in titulos_interes]

                if not posiciones_interes:
                    raise ValueError("No se encontraron los títulos en el archivo.")

                # Agregar encabezados seleccionados a la matriz
                matriz_resultado.append([encabezados[i] for i in posiciones_interes])

                # Leer las filas
                for row in sheet.iter_rows(min_row=sheet.min_row + 1,
                                           values_only=True):  # Empezar desde la siguiente fila
                    if len(row) > 12 and row[12] != "Sin programa especifico":
                        codigo_snies = row[12]
                        if codigo_snies in codigos_snies:
                            fila = [row[i] for i in posiciones_interes]
                            matriz_resultado.append(fila)

            except Exception as e:
                print(f"Error al procesar el archivo {ruta}: {e}")

            return matriz_resultado


        def crear_archivo(self, ruta: str, mapade_programas_academicos: Dict[int, 'ProgramaAcademico'],
                          etiquetas_columnas: List[str]) -> bool:
            wb = Workbook()
            ws = wb.active
            ws.append(etiquetas_columnas)

            for programa in mapade_programas_academicos.values():
                ws.append(
                    programa.obtener_datos_xlsx())  # Suponiendo que `obtener_datos_xlsx` devuelve los datos adecuados

            wb.save(ruta)
            return True

        def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'],
                                   etiquetas_columnas: List[str]) -> bool:
            wb = Workbook()
            ws = wb.active
            ws.append(etiquetas_columnas)

            for programa in programas_buscados:
                ws.append(programa.obtener_datos_xlsx())  # Al igual que antes

            wb.save(ruta)
            return True

        def crear_archivo_extra(self, ruta: str, datos_a_imprimir: List[List[str]]) -> bool:
            wb = Workbook()
            ws = wb.active
            for fila in datos_a_imprimir:
                ws.append(fila)

            wb.save(ruta)
            return True

