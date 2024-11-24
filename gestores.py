import openpyxl
import json
import csv
from openpyxl import Workbook
import pandas as pd
from typing import List, Dict



class Gestor:

    def crear_archivo(self, ruta: str, dataframe: pd.DataFrame) -> bool:

        raise NotImplementedError



    def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        raise NotImplementedError



class GestorCsv(Gestor):

    def crear_archivo(self, ruta: str, dataframe: pd.DataFrame) -> bool:
        """
        Crea un archivo CSV basado en un DataFrame.

        :param ruta: Ruta donde se guardará el archivo CSV.
        :param dataframe: DataFrame que contiene los datos a guardar.
        :return: True si se crea el archivo correctamente.
        """
        try:
            dataframe.to_csv(ruta, index=False, encoding='utf-8')  # Guarda el DataFrame directamente como CSV
            return True
        except Exception as e:
            print(f"Error al crear el archivo CSV: {e}")
            return False


    def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        with open(ruta, 'w', newline='', encoding='utf-8') as file:

            writer = csv.writer(file)

            writer.writerow(etiquetas_columnas)

            for programa in programas_buscados:

                writer.writerow(programa.obtener_datos_csv())  # Al igual que antes

        return True




class GestorJson(Gestor):

    def crear_archivo(self, ruta: str, dataframe: pd.DataFrame) -> bool:
        """
        Crea un archivo JSON basado en un DataFrame.

        :param ruta: Ruta donde se guardará el archivo JSON.
        :param dataframe: DataFrame que contiene los datos a guardar.
        :return: True si se crea el archivo correctamente.
        """
        try:
            dataframe.to_json(ruta, orient='records', indent=4, force_ascii=False)  # Guarda el DataFrame como JSON
            return True
        except Exception as e:
            print(f"Error al crear el archivo JSON: {e}")
            return False



    def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'], etiquetas_columnas: List[str]) -> bool:

        datos = []

        for programa in programas_buscados:

            datos.append(programa.obtener_datos_json())  # Al igual que antes

        with open(ruta, 'w', encoding='utf-8') as file:

            json.dump(datos, file, indent=4)

        return True



class GestorXlsx(Gestor):

        def leer_archivo_snies(self, ruta_archivo, unico_dato=False):
            """
            Lee un archivo Excel y selecciona columnas predeterminadas.
            También opcionalmente filtra por códigos SNIES y/o usa solo un conjunto reducido de columnas.

            Args:
                ruta_archivo (str): Ruta del archivo Excel.
                codigos_snies (list): Lista de códigos SNIES para filtrar (opcional).
                unico_dato (bool): Indica si se debe usar solo un conjunto reducido de columnas.

            Returns:
                pd.DataFrame: DataFrame procesado.
            """
            try:
                # Leer todo el archivo Excel
                df = pd.read_excel(ruta_archivo, header=None)

                # Encontrar la fila que contiene "CÓDIGO DE LA INSTITUCIÓN"
                fila_inicio = \
                df[df.apply(lambda x: x.str.contains("CÓDIGO DE LA INSTITUCIÓN", na=False).any(), axis=1)].index[0]

                # Leer el archivo nuevamente con el encabezado correcto
                df = pd.read_excel(ruta_archivo, skiprows=fila_inicio)

                if not unico_dato:
                    # Seleccionar las columnas predeterminadas
                    ultima_columna = df.columns[-1]
                    columnas_predeterminadas = ["CÓDIGO DE LA INSTITUCIÓN", "CÓDIGO SNIES DEL PROGRAMA", "SEMESTRE", "SEXO", "ID SEXO", "AÑO", ultima_columna]
                    df_filtrado = df[columnas_predeterminadas]
                else:
                    ultima_columna_nombre = df.columns[-1]
                    df_filtrado = df[[ultima_columna_nombre]]

                # Consolidar datos agrupándolos y sumando
                df_consolidado = df_filtrado.groupby(df_filtrado.columns.tolist()).sum(numeric_only=True).reset_index()

                return df_consolidado


            except Exception as e:
                print(f"Error al procesar el archivo: {e}")
                return pd.DataFrame()




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

        def crear_archivo(self, ruta: str, dataframe: pd.DataFrame) -> bool:
            """
            Crea un archivo Excel basado en un DataFrame.

            :param ruta: Ruta donde se guardará el archivo Excel.
            :param dataframe: DataFrame que contiene los datos a guardar.
            :return: True si se crea el archivo correctamente.
            """
            try:
                dataframe.to_excel(ruta, index=False, engine='openpyxl')  # Guarda el DataFrame como Excel
                return True
            except Exception as e:
                print(f"Error al crear el archivo Excel: {e}")
                return False

        def crear_archivo_buscados(self, ruta: str, programas_buscados: List['ProgramaAcademico'],
                                   etiquetas_columnas: List[str]) -> bool:
            wb = Workbook()
            ws = wb.active
            ws.append(etiquetas_columnas)

            for programa in programas_buscados:
                ws.append(programa.obtener_datos_xlsx())  # Al igual que antes

            wb.save(ruta)
            return True

