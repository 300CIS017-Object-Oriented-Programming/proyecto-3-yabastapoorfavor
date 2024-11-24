import streamlit as st
import pandas as pd
import os

st.title("¡Bienvenido al **_SNIES Extractor_**!:balloon:")

st.write("_Siga las instrucciones a continuación para generar los archivos deseados_")

# Opción de selección: Cargar archivo desde el sistema local o desde el navegador
opcion_archivo = st.radio("¿Cómo deseas cargar el archivo?", ('Desde el sistema local', 'Desde el navegador'))

# Cargar archivos desde el sistema local
if opcion_archivo == 'Desde el sistema local':
    # Ruta del directorio local donde se encuentran los archivos
    directorio_archivos = "C:/Users/mond_/OneDrive/Escritorio/SNIESCPP/proyecto-2-snies-extractor-4-beibis-1/outputs"  # Cambia esta ruta al directorio donde guardas los archivos

    # Obtener la lista de archivos CSV y Excel en el directorio
    archivos = [f for f in os.listdir(directorio_archivos) if f.endswith(('.csv', '.xlsx'))]

    # Crear un selector de archivos
    archivo_seleccionado = st.selectbox("Selecciona un archivo", archivos)

    if archivo_seleccionado:
        # Obtener la ruta completa del archivo
        ruta_archivo = os.path.join(directorio_archivos, archivo_seleccionado)

        try:
            # Determinar el tipo de archivo
            if archivo_seleccionado.endswith(".csv"):
                # Leer archivo CSV con delimitador ";"
                df = pd.read_csv(ruta_archivo, delimiter=";").dropna()  # Eliminar filas vacías
            elif archivo_seleccionado.endswith(".xlsx"):
                # Leer archivo Excel
                df = pd.read_excel(ruta_archivo)
            else:
                st.error("Formato de archivo no soportado. Sube un archivo CSV o Excel.")
                df = None

            if df is not None:
                # Eliminar comas y formatear los números como texto sin comas
                df = df.applymap(lambda x: f"{x:.0f}" if isinstance(x, (int, float)) else x)

                st.success("Archivo cargado exitosamente.")
                st.write("Vista previa del DataFrame:")

                # Filtro por palabra clave
                keyword = st.text_input("Filtrar por palabra clave (por ejemplo, nombre del programa académico):")

                if keyword:
                    # Filtrar el DataFrame por la palabra clave en todas las columnas
                    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    st.write(f"Resultados filtrados por '{keyword}':")
                    st.dataframe(filtered_df)
                else:
                    # Si no se ha introducido una palabra clave, mostrar el DataFrame completo
                    st.dataframe(df)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
else:
    # Subir archivo desde el navegador
    uploaded_file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Determinar el tipo de archivo subido
        file_extension = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_extension == "csv":
                # Leer archivo CSV con delimitador ";"
                df = pd.read_csv(uploaded_file, delimiter=";").dropna()  # Eliminar filas vacías
            elif file_extension == "xlsx":
                # Leer archivo Excel
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Formato de archivo no soportado. Sube un archivo CSV o Excel.")
                df = None

            if df is not None:
                # Eliminar comas y formatear los números como texto sin comas
                df = df.applymap(lambda x: f"{x:.0f}" if isinstance(x, (int, float)) else x)

                st.success("Archivo subido exitosamente.")
                st.write("Vista previa del DataFrame:")

                # Filtro por palabra clave
                keyword = st.text_input("Filtrar por palabra clave (por ejemplo, nombre del programa académico):")

                if keyword:
                    # Filtrar el DataFrame por la palabra clave en todas las columnas
                    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    st.write(f"Resultados filtrados por '{keyword}':")
                    st.dataframe(filtered_df)
                else:
                    # Si no se ha introducido una palabra clave, mostrar el DataFrame completo
                    st.dataframe(df)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")