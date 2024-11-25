import pandas as pd
from gestores import GestorXlsx
from Settings import Settings


class SNIESController:
    def __init__(self):
        self.dataframe_principal = pd.DataFrame()  # DataFrame para consolidar toda la información
        self.gestor_xlsx = GestorXlsx()
        self.etiquetas_columnas = []
        self.ruta_admitidos = Settings.ADMITIDOS_FILE_PATH
        self.ruta_graduados = Settings.GRADUADOS_FILE_PATH
        self.ruta_inscritos = Settings.INSCRITOS_FILE_PATH
        self.ruta_matriculados = Settings.MATRICULADOS_FILE_PATH
        self.ruta_matriculados_primer_curso = Settings.MATRICULADOS_PRIMER_CURSO_FILE_PATH

    def procesar_datos(self, anio1, anio2, palabra_clave):
        try:

            anio11 = int(anio1)
            anio22 = int(anio2)

            anios = [anio for anio in range(min(anio11, anio22), max(anio11, anio22) + 1)]
            primero = True
            gestor = GestorXlsx()

            for anio in anios:
                DIRECCIONES = [
                    Settings.ADMITIDOS_FILE_PATH,
                    Settings.GRADUADOS_FILE_PATH,
                    Settings.INSCRITOS_FILE_PATH,
                    Settings.MATRICULADOS_FILE_PATH,
                    Settings.MATRICULADOS_PRIMER_CURSO_FILE_PATH
                ]

                for direccion in DIRECCIONES:
                    ruta_archivo = f"{direccion}{anio}.xlsx"
                    dataframe_minimizado = gestor.leer_archivo(ruta_archivo, palabra_clave, not primero)

                    dataframe_minimizado["CÓDIGO SNIES DEL PROGRAMA"] = dataframe_minimizado["CÓDIGO SNIES DEL PROGRAMA"].astype(str)
                    dataframe_minimizado["SEMESTRE"] = dataframe_minimizado["SEMESTRE"].astype(str)

                    if primero:

                        dataframe_minimizado.rename(columns={"ADMITIDOS": f'{"ADMITIDOS"}_{anio}'}, inplace=True)
                        self.df = dataframe_minimizado
                        primero = False

                    else:
                        for col in dataframe_minimizado.columns:
                            if not (col == "CÓDIGO SNIES DEL PROGRAMA" or col == "SEMESTRE"):
                                dataframe_minimizado.rename(columns={col: f'{col}_{anio}'}, inplace=True)

                        self.df = pd.merge(
                            self.df, dataframe_minimizado,
                            on=["CÓDIGO SNIES DEL PROGRAMA", "SEMESTRE"],
                            how="left"
                        )

        except FileNotFoundError:
            raise FileNotFoundError("Archivo necesario no está cargado al SNIES")
        except Exception as e:
            raise Exception(f"Error al procesar los datos: {e}")

        return self.df




