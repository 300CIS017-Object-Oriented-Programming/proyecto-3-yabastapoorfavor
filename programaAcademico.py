import pandas as pd  # type: ignore
from typing import List, Dict



class ProgramaAcademico:
    def __init__(self, codigo_de_la_institucion=None, ies_padre=None, institucion_ies=None, principal_o_seccional=None,
                 id_sector_ies=None, sector_ies=None, id_caracter=None, caracter_ies=None,
                 codigo_departamento_ies=None, departamento_domicilio_ies=None, codigo_municipio_ies=None,
                 municipio_domicilio_ies=None, codigo_snies=None, programa_academico=None, id_nivel_academico=None,
                 nivel_academico=None, id_nivel_formacion=None, nivel_formacion=None, id_metodologia=None,
                 metodologia=None, id_area=None, area_conocimiento=None, id_nucleo=None, nucleo_conocimiento=None,
                 id_cine_campo_amplio=None, desc_cine_campo_amplio=None, id_cine_campo_especifico=None,
                 desc_cine_campo_especifico=None, id_cine_codigo_detallado=None, desc_cine_codigo_detallado=None,
                 codigo_departamento_programa=None, departamento_oferta=None, codigo_municipio_programa=None,
                 municipio_oferta=None):
        self.codigo_de_la_institucion = codigo_de_la_institucion
        self.ies_padre = ies_padre
        self.institucion_ies = institucion_ies
        self.principal_o_seccional = principal_o_seccional
        self.id_sector_ies = id_sector_ies
        self.sector_ies = sector_ies
        self.id_caracter = id_caracter
        self.caracter_ies = caracter_ies
        self.codigo_departamento_ies = codigo_departamento_ies
        self.departamento_domicilio_ies = departamento_domicilio_ies
        self.codigo_municipio_ies = codigo_municipio_ies
        self.municipio_domicilio_ies = municipio_domicilio_ies
        self.codigo_snies = codigo_snies
        self.programa_academico = programa_academico
        self.id_nivel_academico = id_nivel_academico
        self.nivel_academico = nivel_academico
        self.id_nivel_formacion = id_nivel_formacion
        self.nivel_formacion = nivel_formacion
        self.id_metodologia = id_metodologia
        self.metodologia = metodologia
        self.id_area = id_area
        self.area_conocimiento = area_conocimiento
        self.id_nucleo = id_nucleo
        self.nucleo_conocimiento = nucleo_conocimiento
        self.id_cine_campo_amplio = id_cine_campo_amplio
        self.desc_cine_campo_amplio = desc_cine_campo_amplio
        self.id_cine_campo_especifico = id_cine_campo_especifico
        self.desc_cine_campo_especifico = desc_cine_campo_especifico
        self.id_cine_codigo_detallado = id_cine_codigo_detallado
        self.desc_cine_codigo_detallado = desc_cine_codigo_detallado
        self.codigo_departamento_programa = codigo_departamento_programa
        self.departamento_oferta = departamento_oferta
        self.codigo_municipio_programa = codigo_municipio_programa
        self.municipio_oferta = municipio_oferta

        # DataFrame para almacenar los datos de consolidado
        self.data = pd.DataFrame(columns=[
            "idSexo", "sexo", "ano", "semestre", "inscritos", "admitidos",
            "matriculados", "matriculadosPrimerSemestre", "graduados"
        ])

    def agregar_consolidado(self, id_sexo, sexo, ano, semestre, inscritos, admitidos,
                            matriculados, matriculados_primer_semestre, graduados):
        nuevo_consolidado = {
            "idSexo": id_sexo, "sexo": sexo, "ano": ano, "semestre": semestre,
            "inscritos": inscritos, "admitidos": admitidos,
            "matriculados": matriculados, "matriculadosPrimerSemestre": matriculados_primer_semestre,
            "graduados": graduados
        }
        self.data = self.data.append(nuevo_consolidado, ignore_index=True)

    def obtener_datos_csv(self) -> List:
        """
        Devuelve los datos del programa en un formato de lista para CSV.
        """
        return [
            self.codigo_snies,
            self.programa_academico,
            self.nivel_formacion,
            self.metodologia
        ]

    def obtener_datos_xlsx(self) -> Dict[str, any]:
        """
        Devuelve los datos del programa en un formato de diccionario para XLSX.
        """
        return {
            "Código SNIES": self.codigo_snies,
            "Programa Académico": self.programa_academico,
            "Nivel de Formación": self.nivel_formacion,
            "Metodología": self.metodologia
        }

    def obtener_datos_json(self) -> Dict[str, any]:
        """
        Devuelve los datos del programa en un formato de diccionario para JSON.
        """
        return {
            "codigo_snies": self.codigo_snies,
            "programa_academico": self.programa_academico,
            "nivel_formacion": self.nivel_formacion,
            "metodologia": self.metodologia
        }