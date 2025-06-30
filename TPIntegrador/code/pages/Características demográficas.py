import streamlit as st
from src.util.constantes import INDIVIDUOS_FUSIONADO
from src.util.data_processing import (resumen_media_mediana_edad, edad_promedio_por_aglomerado, datos_dependencia_demografica, datos_poblacion_edad_genero)
from src.util.plots import (grafico_edad_promedio_aglomerado, grafico_dependencia_demografica, grafico_poblacion_edad_genero)
from src.util.modulos_seccion_b import codigos_aglom

# 1.3.4
def mostrar_media_y_mediana_edad():
    """
    Muestra la media, mediana y cantidad de datos de la edad por año y trimestre.

    Calcula y presenta estadísticas descriptivas de la edad (media, mediana, cantidad de datos) agrupadas por año y trimestre,
    utilizando los datos fusionados de individuos.
    """
    st.title("Características demográficas")
    st.markdown("Media, mediana y cantidad de datos de la edad por año y trimestre.")
    resumen = resumen_media_mediana_edad(INDIVIDUOS_FUSIONADO)
    if resumen is None or resumen.empty:
        st.info("No hay datos disponibles para mostrar.")
        return
    st.dataframe(resumen, use_container_width=True, hide_index=True)
    st.markdown("---")

# 1.3.2
def promedio_edad_por_aglomerado():
    """
    Muestra la edad promedio ponderada de personas por aglomerado para el último trimestre y año disponibles.

    Calcula la edad promedio ponderada por aglomerado, reemplaza el código por el nombre del aglomerado,
    y presenta los resultados en una tabla y un gráfico de barras.
    """
    st.title("Edad Promedio de Personas por Aglomerado")
    st.markdown("Información para el último trimestre y año disponibles.")
    resumen_edad, max_anio, max_trimestre = edad_promedio_por_aglomerado(INDIVIDUOS_FUSIONADO)
    if resumen_edad is None or resumen_edad.empty:
        st.info("No hay datos válidos para calcular la edad promedio.")
        return

    resumen_edad['Aglomerado'] = resumen_edad['AGLOMERADO'].astype(str).map(codigos_aglom)
    resumen_edad = resumen_edad.drop(columns=['AGLOMERADO'])
    resumen_edad = resumen_edad[['Aglomerado', 'Edad Promedio Ponderada']]

    st.write("### Edad Promedio por Aglomerado (Ponderada)")
    st.dataframe(resumen_edad.sort_values(by='Edad Promedio Ponderada', ascending=False), hide_index=True)
    st.write("### Distribución de Edad Promedio por Aglomerado")
    fig = grafico_edad_promedio_aglomerado(resumen_edad, max_anio, max_trimestre, codigos_aglom)
    st.pyplot(fig)
# 1.3.3
def dependencia_demografica():
    """
    Muestra el índice de dependencia demográfica por aglomerado y período.

    Calcula la relación entre la población pasiva (niños y adultos mayores) y la población activa,
    agrupada por aglomerado y período, y la presenta en un gráfico de barras.
    """
    st.title("Índice de Dependencia Demográfica")
    st.markdown("Relación entre la población pasiva (niños y adultos mayores) y la población activa por aglomerado y período.")
    comparacion, _, _ = datos_dependencia_demografica(INDIVIDUOS_FUSIONADO, codigos_aglom)
    if comparacion is None or comparacion.empty:
        st.info("No hay datos para calcular el índice de dependencia demográfica.")
        return
    fig = grafico_dependencia_demografica(comparacion)
    st.write("Mayor el porcentaje, mayor la proporción de jubilados/niños respecto a la población activa.")
    st.pyplot(fig)
# 1.3.1
def poblacion_edad_genero():
    """
    Muestra la distribución de la población por edad y sexo para el año y trimestre seleccionados.

    Agrupa los datos de individuos por rangos de edad y sexo, y presenta la distribución en un gráfico de barras apiladas.
    """
    st.title("Distribución de la población por edad y sexo")
    st.markdown("Distribución de la población agrupada por rangos de edad y sexo para el año y trimestre seleccionados.")
    df_agrupado, año, trimestre = datos_poblacion_edad_genero(INDIVIDUOS_FUSIONADO)
    if df_agrupado is None or df_agrupado.empty:
        st.warning("No hay datos disponibles para el año y trimestre seleccionado.")
        return
    fig = grafico_poblacion_edad_genero(df_agrupado, año, trimestre)
    st.pyplot(fig)
    st.markdown("---")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    poblacion_edad_genero()
    st.markdown("---")
    promedio_edad_por_aglomerado()
    st.markdown("---")
    dependencia_demografica()
    st.markdown("---")
    mostrar_media_y_mediana_edad()