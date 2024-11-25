import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import re
from view import View


st.title("¡Bienvenido al **_SNIES Extractor_**! 🎈")
st.write("_Siga las instrucciones a continuación para realizar el análisis y exportación de datos._")

st.subheader("Parametrización Inicial")
st.write("Asegúrese de que la carpeta SNIES_EXTRACTOR esté correctamente configurada con los archivos necesarios.")

if st.button("Confirmar parametrización"):
    st.success("Parametrización confirmada. Puedes continuar con el análisis.")

st.subheader("Selección de parámetros")
anio1 = st.text_input("Escriba el primer año de búsqueda:", value="2020")
anio2 = st.text_input("Escriba el segundo año de búsqueda:", value="2021")

view = View()

valid_anio1, anio1_int = view.validar_entrada_anio(anio1)
valid_anio2, anio2_int = view.validar_entrada_anio(anio2)

if not (valid_anio1 and valid_anio2):
    st.error("Ambos años deben ser valores enteros válidos.")
else:
    palabra_clave = st.text_input("Ingrese una palabra clave para filtrar los datos:", value="")

    if not palabra_clave.strip():
        st.error("Debe ingresar una palabra clave válida.")
    else:
        formato = st.selectbox("Seleccione el formato de archivo para exportar los datos:", ["XLSX", "CSV", "JSON"])

        if st.button("Procesar y Exportar"):
            view.procesar_datos(anio1_int, anio2_int, palabra_clave, formato)

st.subheader("Cierre del programa")
if st.button("Salir"):
    st.success("Recuerde revisar la carpeta de outputs para los archivos exportados. ¡Programa cerrado con éxito!")


st.write("_Siga las instrucciones a continuación para generar los análisis deseados_")

# Opción de selección: Cargar archivo desde el sistema local o desde el navegador
opcion_archivo = st.radio("¿Cómo deseas cargar el archivo?", ('Desde el sistema local', 'Desde el navegador'))


def extraer_anios_columnas(columnas):
    """
    Extrae los años de las columnas que siguen el patrón <nombre>_<año>.
    """
    anios = []
    for col in columnas:
        match = re.search(r"_(\d{4})$", col)
        if match:
            anios.append(int(match.group(1)))
    return sorted(set(anios))


# Cargar archivos desde el sistema local
if opcion_archivo == 'Desde el sistema local':
    directorio_archivos = "C:/Users/Usuario/Documents/YAAA"
    archivos = [f for f in os.listdir(directorio_archivos) if f.endswith(('.csv', '.xlsx'))]
    archivo_seleccionado = st.selectbox("Selecciona un archivo", archivos)

    if archivo_seleccionado:
        ruta_archivo = os.path.join(directorio_archivos, archivo_seleccionado)

        try:
            if archivo_seleccionado.endswith(".csv"):
                df = pd.read_csv(ruta_archivo, delimiter=";").dropna()
            elif archivo_seleccionado.endswith(".xlsx"):
                df = pd.read_excel(ruta_archivo)
            else:
                st.error("Formato de archivo no soportado.")
                df = None

            if df is not None:
                df.columns = df.columns.str.strip()
                st.success("Archivo cargado exitosamente.")
                st.write("Vista previa del DataFrame:")
                st.dataframe(df)

                anios_disponibles = extraer_anios_columnas(df.columns)

                if not anios_disponibles:
                    st.warning("No se encontraron columnas con el formato esperado (<nombre>_<año>).")
                else:
                    st.write("Años disponibles en los datos:", anios_disponibles)

                    years_selected = st.multiselect("Selecciona los años para analizar", anios_disponibles)
                    metric_options = ["ADMITIDOS", "GRADUADOS", "INSCRITOS", "MATRICULADOS", "PRIMER CURSO"]
                    metric_selected = st.selectbox("Selecciona el tipo de dato a graficar", metric_options)
                    chart_type = st.radio("Selecciona el tipo de gráfico", ["Barras", "Líneas de tendencia"])

                    if not years_selected:
                        st.error("Selecciona al menos un año para continuar.")
                    else:
                        filtered_columns = [
                            col for col in df.columns if
                            any(col.startswith(f"{metric_selected}_{year}") for year in years_selected)
                        ]

                        if not filtered_columns:
                            st.error("No se encontraron datos para la combinación seleccionada.")
                        else:
                            filtered_df = df[filtered_columns]
                            st.write(f"Datos para {metric_selected} en los años seleccionados:")
                            st.dataframe(filtered_df)

                            try:
                                graph_data = filtered_df.sum().reset_index()
                                graph_data.columns = ['Column', 'Value']
                                graph_data['Year'] = graph_data['Column'].str.extract(r'_(\d{4})$')[0].astype(int)

                                fig, ax = plt.subplots(figsize=(12, 6))

                                if chart_type == "Barras":
                                    grouped_data = graph_data.groupby("Year")["Value"].sum()
                                    ax.bar(grouped_data.index, grouped_data.values, color='skyblue')
                                    ax.set_title(f"Comparativa de {metric_selected} entre los años seleccionados")
                                    ax.set_xlabel("Año")
                                    ax.set_ylabel(metric_selected)
                                elif chart_type == "Líneas de tendencia":
                                    graph_data = graph_data.sort_values("Year")
                                    ax.plot(
                                        graph_data["Year"],
                                        graph_data["Value"],
                                        marker='o',
                                        linestyle='-',
                                        color='b',
                                        label=f"Tendencia de {metric_selected}"
                                    )
                                    ax.set_title(f"Tendencia de {metric_selected} entre los años seleccionados")
                                    ax.set_xlabel("Año")
                                    ax.set_ylabel(metric_selected)
                                    ax.legend(title="Datos")

                                plt.xticks(rotation=45, ha='right')
                                st.pyplot(fig)
                            except Exception as e:
                                st.error(f"Error al generar el gráfico: {e}")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
else:
    uploaded_file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_extension == "csv":
                df = pd.read_csv(uploaded_file, delimiter=";").dropna()
            elif file_extension == "xlsx":
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Formato de archivo no soportado.")
                df = None

            if df is not None:
                df.columns = df.columns.str.strip()
                st.success("Archivo subido exitosamente.")
                st.write("Vista previa del DataFrame:")
                st.dataframe(df)

                anios_disponibles = extraer_anios_columnas(df.columns)

                if not anios_disponibles:
                    st.warning("No se encontraron columnas con el formato esperado (<nombre>_<año>).")
                else:
                    st.write("Años disponibles en los datos:", anios_disponibles)

                    years_selected = st.multiselect("Selecciona los años para analizar", anios_disponibles)
                    metric_options = ["ADMITIDOS", "GRADUADOS", "INSCRITOS", "MATRICULADOS", "PRIMER CURSO"]
                    metric_selected = st.selectbox("Selecciona el tipo de dato a graficar", metric_options)
                    chart_type = st.radio("Selecciona el tipo de gráfico", ["Barras", "Líneas de tendencia"])

                    if not years_selected:
                        st.error("Selecciona al menos un año para continuar.")
                    else:
                        filtered_columns = [
                            col for col in df.columns if
                            any(col.startswith(f"{metric_selected}_{year}") for year in years_selected)
                        ]

                        if not filtered_columns:
                            st.error("No se encontraron datos para la combinación seleccionada.")
                        else:
                            filtered_df = df[filtered_columns]
                            st.write(f"Datos para {metric_selected} en los años seleccionados:")
                            st.dataframe(filtered_df)

                            try:
                                graph_data = filtered_df.sum().reset_index()
                                graph_data.columns = ['Column', 'Value']
                                graph_data['Year'] = graph_data['Column'].str.extract(r'_(\d{4})$')[0].astype(int)

                                fig, ax = plt.subplots(figsize=(12, 6))

                                if chart_type == "Barras":
                                    grouped_data = graph_data.groupby("Year")["Value"].sum()
                                    ax.bar(grouped_data.index, grouped_data.values, color='skyblue')
                                    ax.set_title(f"Comparativa de {metric_selected} entre los años seleccionados")
                                    ax.set_xlabel("Año")
                                    ax.set_ylabel(metric_selected)
                                elif chart_type == "Líneas de tendencia":
                                    graph_data = graph_data.sort_values("Year")
                                    ax.plot(
                                        graph_data["Year"],
                                        graph_data["Value"],
                                        marker='o',
                                        linestyle='-',
                                        color='b',
                                        label=f"Tendencia de {metric_selected}"
                                    )
                                    ax.set_title(f"Tendencia de {metric_selected} entre los años seleccionados")
                                    ax.set_xlabel("Año")
                                    ax.set_ylabel(metric_selected)
                                    ax.legend(title="Datos")

                                plt.xticks(rotation=45, ha='right')
                                st.pyplot(fig)
                            except Exception as e:
                                st.error(f"Error al generar el gráfico: {e}")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

