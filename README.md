Integrantes: _Maria Lucía Castillo García, Juliana González Sánchez y Ana Daniela Paredes Tovar _


**1.1 Descripción General**

El Sistema Nacional de Información de la Educación Superior (SNIES) en Colombia es una plataforma fundamental para la recopilación y gestión de datos relacionados con las instituciones de educación superior y los programas académicos que ofrecen. Estos datos incluyen información clave sobre procesos como la inscripción, admisión, matrícula y graduación, constituyendo una base esencial para la toma de decisiones estratégicas en el sector educativo.

El análisis de estas tendencias permite identificar oportunidades de mejora en el diseño curricular de programas académicos, asegurando que sean pertinentes, atractivos y alineados con las necesidades de los estudiantes. Asimismo, el estudio de datos históricos y patrones emergentes resulta crucial para la planificación estratégica de las instituciones, facilitando decisiones informadas sobre la apertura de nuevos programas, la modificación de los existentes y la asignación eficiente de recursos.

Su objetivo principal es procesar grandes volúmenes de información proveniente de diferentes fuentes, como admitidos, graduados, inscritos, matriculados y matriculados en primer curso, consolidándolos en un único DataFrame que permite realizar análisis eficientes y personalizados.

El sistema permite a los usuarios filtrar los datos por palabras clave y rangos de años específicos. Además, incluye la capacidad de exportar los resultados en formatos versátiles como XLSX, CSV y JSON, facilitando su integración en otros sistemas o plataformas.

A través de una interfaz interactiva creada con Streamlit, los usuarios pueden cargar archivos desde su sistema local o navegador, parametrizar búsquedas, y visualizar los datos procesados. También ofrece herramientas para graficar y analizar tendencias basadas en las métricas seleccionadas, como admitidos o graduados, durante los años disponibles en los datos.

La estructura del proyecto se organiza en componentes especializados:

1. **Gestores**: Encargados de leer y exportar datos en diversos formatos.
2. **SNIESController**: Responsable de consolidar y procesar la información en función de las solicitudes del usuario.
3. **View**: Maneja la interacción con el usuario a través de la interfaz gráfica, validando entradas y guiando al usuario durante el proceso.
4. **Settings**: Define rutas y configuraciones clave para los archivos de entrada y salida.

En conjunto, "SNIES Extractor" es una herramienta robusta diseñada para facilitar el análisis y la toma de decisiones basada en datos educativos en Colombia.


***
**1.2 Descripción del Proyecto SNIES**

En el desarrollo del presente proyecto, se optó por abandonar el uso de C++ en favor de Python, dado que este último ofrece herramientas más adecuadas para el procesamiento y análisis de datos, así como una mayor facilidad para la creación de aplicaciones interactivas a través de bibliotecas como Streamlit. Esto hizo que clases como  _Consolidado_ y _ProgramaAcademico_ pasaran a ser obsoletas por lo que consolidar en Python por medio de dataframes resulta ser más sencillo y eficiente. 

Ahora bien, entre las clases que sí prevalecieron fueron: _Gestor_ que funciona como una clase base para manejar diferentes tipos de archivos. De ella derivan las clases hijas _GestorCsv_, _GestorXlx_ y _GestorJson_ , que se especializan en la lectura y escritura de datos en diferentes formatos. Esto lo hicimos por medio de dataframes. También mantuvimos el _SNIESController_ quien se encarga de controlar la interacción con el SNIES, facilitando la conexión y la gestión de datos necesarios para el análisis.

#### Imágenes de Gestor ![Gestor 1](imagenes/ss1Gestor.png) ![Gestor 2](imagenes/ss2Gestor.png) ![Gestor 3](imagenes/ss3Gestor.png) ![Gestor 4](imagenes/ss4Gestor.png) ![Gestor 5](imagenes/ss5Gestor.png) ![Gestor 6](imagenes/ss6Gestor.png) ![Gestor 7](imagenes/ss7Gestor.png) 

#### Imágenes de SNIES ![SNIES 1](imagenes/ss1SNIES.png) ![SNIES 2](imagenes/ss2SNIES.png) ![SNIES 3](imagenes/ss3SNIES.png) ![SNIES 4](imagenes/ss4SNIES.png)



La aplicación que desarrollamos se llama _streamlitSNIES_.  Esta es una aplicación interactiva desarrollada con Streamlit que permite analizar, filtrar y exportar datos relacionados con programas académicos del Sistema Nacional de Información de la Educación Superior (SNIES) en Colombia. La herramienta carga archivos en formatos como XLSX, CSV o JSON, y ofrece al usuario la posibilidad de filtrar información por años y palabras clave, consolidando los resultados en un único DataFrame para su análisis. Además, incluye funcionalidades para generar gráficos y visualizar datos seleccionados, ofreciendo una interfaz accesible y amigable que guía al usuario en cada paso del proceso. StreamlitSNIES es especialmente útil para instituciones educativas, investigadores o administradores que necesitan procesar grandes volúmenes de datos del SNIES de manera rápida y eficiente.

#### Imágenes de App ![App 1](imagenes/app1.png) ![App 2](imagenes/app2.png) ![App 3](imagenes/app3.png) ![App 4](imagenes/app4.png) ![App 5](imagenes/app5.png) ![App 6](imagenes/app6.png) ![App 7](imagenes/app7.png) ![App 8](imagenes/app8.png) ![App 9](imagenes/app9.png) ![App 10](imagenes/app10.png)




Por último, dejamos clases como el _View_ para la visualización del menú y la clase _Settings_ para el manejo de números mágicos. 

#### Imágenes de View ![View 1](imagenes/ss1View.png) ![View 2](imagenes/ss2View.png) ![View 3](imagenes/ss3View.png)



#### Imágenes de Settings ![Settings 1](imagenes/ss1Settings.png)


#### Imágenes de Main ![Main 1](imagenes/ss1Main.png)

****
**2.2 Funcionamiento del proyecto

![Función 1](imagenes/funcio1.png) ![Función 2](imagenes/funcio2.png) ![Función 3](imagenes/funcio3.png) ![Función 4](imagenes/funcio4.png) ![Función 5](imagenes/funcio5.png) ![Función 6](imagenes/funcio6.png) ![Función 7](imagenes/funcio7.png) ![Función 8](imagenes/funcio8.png) ![Función 9](imagenes/funcio9.png) ![Función 10](imagenes/funcio10.png) ![Función 11](imagenes/funcio11.png) ![Función 12](imagenes/funcio12.png)



****
**Diagrama UML:

```mermaid
classDiagram

    class SNIESController {

        +DataFrame dataframe_principal
        +GestorXlsx gestor_xlsx
        +list etiquetas_columnas
        +str ruta_admitidos
        +str ruta_graduados
        +str ruta_inscritos
        +str ruta_matriculados
        +str ruta_matriculados_primer_curso
        +procesar_datos(anio1, anio2, palabra_clave)

    }

  

    class View {

        +SNIESController controlador
        +is_convertible_to_int(value)
        +organizar_anios(anio1, anio2)
        +validar_entrada_anio(anio)
        +procesar_datos(anio1, anio2, palabra_clave, formato)

    }

  

    class Gestor {

        <<abstract>>
        +crear_archivo(ruta, dataframe) : bool

    }

  

    class GestorCsv {

        +crear_archivo(ruta, dataframe) : bool

    }

  

    class GestorJson {

        +crear_archivo(ruta, dataframe) : bool

    }

  

    class GestorXlsx {

        +leer_archivo(ruta, palabra_clave, columna_unica) : DataFrame
        +crear_archivo(ruta, dataframe) : bool

    }

  

    class Settings {

        +str ADMISIONES_FILE_PATH
        +str GRADUADOS_FILE_PATH
        +str INSCRITOS_FILE_PATH
        +str MATRICULADOS_FILE_PATH
        +str MATRICULADOS_PRIMER_CURSO_FILE_PATH
        +str OUTPUTS_PATH_XLSX
        +str OUTPUTS_PATH_CSV
        +str OUTPUTS_PATH_JSON

    }

  

    class streamlitSNIES {
        +extraer_anios_columnas(columnas)

    }

  

    main ..> View : usa

    View --> SNIESController : tiene
    SNIESController --> Gestor: tiene
    GestorXlsx --|> Gestor
    GestorJson --|> Gestor
    GestorCsv --|> Gestor
    View <.. streamlitSNIES : usa
    SNIESController ..> Settings: usa
