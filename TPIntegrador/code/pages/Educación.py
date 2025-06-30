import streamlit as st
from src.util.constantes import INDIVIDUOS_FUSIONADO
from src.util.constantes import HOGARES_FUSIONADO
from src.util.data_processing import (resumen_nivel_educativo_anual, resumen_lectura_escritura, nivel_educacional_por_rango)
from src.util.plots import (grafico_nivel_educativo_anual, grafico_lectura_escritura)

#1.6.1
def cantidad_personas_por_nivel_educativo():
    """
    Muestra la cantidad de personas por nivel educativo para un año seleccionado por el usuario.

    Carga el resumen anual de nivel educativo, permite seleccionar el año, y presenta los resultados
    en una tabla y un gráfico de barras.
    """
    st.title("Cantidad de Personas por Nivel Educativo")
    st.markdown("Información para un año seleccionado por el usuario.")

    resumen = resumen_nivel_educativo_anual(INDIVIDUOS_FUSIONADO)
    if resumen is None or resumen.empty:
        st.info("No hay datos disponibles para mostrar.")
        return

    anios_disponibles = sorted(resumen['Año'].unique(), reverse=True)
    if not anios_disponibles:
        st.warning("No se encontraron años válidos en el dataset para analizar.")
        return

    anio_seleccionado = st.selectbox("Seleccione el año", anios_disponibles)
    resumen_filtrado = resumen[resumen['Año'] == anio_seleccionado]

    st.subheader(f"Cantidad de Personas por Nivel Educativo - Año {anio_seleccionado}")
    st.dataframe(resumen_filtrado.sort_values(by='Cantidad de Personas', ascending=False), hide_index=True)
    st.subheader("Distribución Gráfica")
    fig = grafico_nivel_educativo_anual(resumen_filtrado, anio_seleccionado)
    st.pyplot(fig)

#1.6.4
def porcentaje_mayores_6_anos():
    """
    Muestra el porcentaje de personas mayores de 6 años capaces e incapaces de leer y escribir por año.

    Calcula y presenta el porcentaje y cantidad de personas mayores de 6 años que pueden o no pueden leer y escribir,
    agrupado por año, en una tabla y un gráfico.
    """
    st.subheader("Información sobre la cantidad de personas mayores a 6 años capaces e incapaces de leer y escribir.")
    resumen = resumen_lectura_escritura(INDIVIDUOS_FUSIONADO)
    if resumen is None or resumen.empty:
        st.info("No hay datos disponibles para mostrar.")
        return

    st.dataframe(
        resumen[["Año", "Porcentaje Capaces", "Porcentaje Incapaces", "Capaces", "Incapaces"]],
        hide_index=True
    )
    st.subheader("Distribución Gráfica")
    fig = grafico_lectura_escritura(resumen)
    st.pyplot(fig)

#1.6.2
def nivel_educacional():
    """
    Muestra el nivel educacional más común por rango etario.

    Calcula y presenta el nivel educativo predominante en cada rango de edad, mostrando los resultados en una tabla.
    """
    st.subheader("Nivel educacional más común por rango etario")
    resultado_df = nivel_educacional_por_rango(INDIVIDUOS_FUSIONADO)
    st.dataframe(resultado_df)

#1.6.3
def descargar_ranking_csv():
    """
    Genera y permite descargar un ranking de aglomerados según el porcentaje de hogares con educación universitaria.

    Calcula el ranking usando los datos de hogares e individuos, muestra la tabla y habilita la descarga en formato CSV.
    """
    from src.util.modulos_seccion_b import ranking_aglomerados_hogares
    from src.util.data_processing import (cargar_hogares, cargar_individuos)
    import pandas as pd
    indiv = pd.read_csv(INDIVIDUOS_FUSIONADO, sep=";", dtype=str)
    hogar = pd.read_csv(HOGARES_FUSIONADO, sep=";", dtype=str)
    diccionario_1 = indiv.to_dict(orient='records')
    diccionario_2 = hogar.to_dict(orient='records')
    ranking = ranking_aglomerados_hogares(diccionario_2, diccionario_1)

    dataframe_ranking = pd.DataFrame(list(ranking.items()), columns=["AGLOMERADO", "PORCENTAJE"])

    path_csv = "ranking_aglomerados.csv"
    dataframe_ranking.to_csv(path_csv, index=False)

    st.title("Ranking de aglomerados por educacion universitaria")
    st.dataframe(dataframe_ranking, hide_index=True)

    st.download_button(
        label="Descargar CSV",
        data=dataframe_ranking.to_csv(index=False),
        file_name="ranking_aglomerados.csv",
        mime="text/csv"
    )   

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    cantidad_personas_por_nivel_educativo()
    st.markdown('---')
    nivel_educacional()
    st.markdown('---')
    descargar_ranking_csv()
    st.markdown('---')
    porcentaje_mayores_6_anos()