import streamlit as st
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

    def organizar_anios(self, anio1, anio2):
        if int(anio2) < int(anio1):
            anio1, anio2 = anio2, anio1
        return anio1, anio2

    def validar_entrada_anio(self, anio):
        if View.is_convertible_to_int(anio):
            return True, int(anio)
        else:
            return False, None


    def procesar_datos(self, anio1, anio2, palabra_clave, formato):
        controlador = SNIESController()
        anio1, anio2 = View().organizar_anios(anio1, anio2)
        def_temp = controlador.procesar_datos(anio1, anio2, palabra_clave)

        if formato == "XLSX":
            gestor = GestorXlsx()
            ruta_salida = Settings.OUTPUTS_PATH_XLSX
        elif formato == "CSV":
            gestor = GestorCsv()
            ruta_salida = Settings.OUTPUTS_PATH_CSV
        elif formato == "JSON":
            gestor = GestorJson()
            ruta_salida = Settings.OUTPUTS_PATH_JSON
        else:
            st.error("Formato no válido.")
            return False

        if gestor.crear_archivo(ruta_salida, def_temp):
            st.success(f"Datos exportados con éxito en el archivo: {ruta_salida}")
            return True
        else:
            st.error("Error al exportar los datos.")
            return False


