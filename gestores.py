import openpyxl
import json
import csv
from openpyxl import Workbook
import pandas as pd
from typing import List, Dict
import streamlit as st


class Gestor:

    def crear_archivo(self, ruta: str, dataframe: pd.DataFrame) -> bool:
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





class GestorXlsx(Gestor):

    @staticmethod
    def leer_archivo(ruta, palabra_clave, columna_unica):
        try:
            df = pd.read_excel(ruta, header=None)

            # Limpiar filas completamente vacías
            df.dropna(how='all', inplace=True)

            # Buscar la fila del encabezado correcto
            fila_encabezado = None
            for idx, fila in df.iterrows():
                if "PROGRAMA ACADÉMICO" in fila.values:  # Buscar la columna clave
                    fila_encabezado = idx
                    break

            if fila_encabezado is None:
                raise KeyError("No se encontró la columna 'PROGRAMA ACADÉMICO' en el archivo.")

            # Releer el archivo usando la fila del encabezado detectado
            df = pd.read_excel(ruta, header=fila_encabezado)

            # Estandarizar nombres de columnas
            df.columns = df.columns.str.strip().str.upper()

            # Validar si la columna clave está presente
            if "PROGRAMA ACADÉMICO" not in df.columns:
                raise KeyError("La columna 'PROGRAMA ACADÉMICO' no existe en el archivo después de procesarlo.")

            # Filtrar por palabra clave
            df_palabra_clave = df[df["PROGRAMA ACADÉMICO"].str.contains(palabra_clave, case=False, na=False)]

            # Definir columnas a consolidar según `unico_dato`
            columnas_a_buscar = [
                "CÓDIGO SNIES DEL PROGRAMA", "SEMESTRE"
            ] if columna_unica else [
                "CÓDIGO SNIES DEL PROGRAMA",
                "METODOLOGÍA",
                "PROGRAMA ACADÉMICO",
                "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)",
                "PRINCIPAL O SECCIONAL",
                "DEPARTAMENTO DE OFERTA DEL PROGRAMA",
                "MUNICIPIO DE OFERTA DEL PROGRAMA",
                "NIVEL DE FORMACIÓN",
                "SEMESTRE"
            ]

            # Selección y consolidación de datos
            ultima_columna = df.columns[-1]
            ultima_columna_df = df_palabra_clave[ultima_columna]
            buscado = df_palabra_clave[columnas_a_buscar]


            buscado = pd.concat([buscado, ultima_columna_df], axis=1)
            resultado = buscado.groupby(columnas_a_buscar).sum(numeric_only=True).reset_index()

            return resultado

        except KeyError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            return None


    def crear_archivo(self, ruta: str, dataframe: pd.DataFrame) -> bool:
        """
        Crea un archivo XLSX basado en un DataFrame.

        :param ruta: Ruta donde se guardará el archivo XLSX.
        :param dataframe: DataFrame que contiene los datos a guardar.
        :return: True si se crea el archivo correctamente.
        """
        try:
            dataframe.to_excel(ruta, index=False, engine='openpyxl')  # Guarda el DataFrame como XLSX
            return True
        except Exception as e:
            print(f"Error al crear el archivo XLSX: {e}")
            return False


