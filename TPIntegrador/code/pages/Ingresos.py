from src.util.constantes import HOGARES_FUSIONADO, INGRESOS_PATH
from src.util.data_processing import (cargar_hogares, cargar_ingresos)
import pandas as pd
import streamlit as st

def hogares_bajo_linea_pobreza_indigencia():
    """
    Muestra la cantidad y porcentaje de hogares de 4 integrantes bajo la línea de pobreza e indigencia para un año y trimestre seleccionados.

    Filtra los hogares de 4 integrantes según el año y trimestre elegidos, calcula el promedio trimestral de la línea de pobreza e indigencia
    a partir de la canasta básica, y determina cuántos hogares están por debajo de esos umbrales. Presenta los resultados en métricas y una tabla resumen.
    """
    df_hogares = cargar_hogares(HOGARES_FUSIONADO)
    df_canasta = cargar_ingresos(INGRESOS_PATH)
    
    st.header("Hogares bajo la línea de pobreza e indigencia (4 integrantes)")
    años = sorted(df_hogares["ANO4"].unique())
    trimestres = sorted(df_hogares["TRIMESTRE"].unique())
    col1, col2 = st.columns(2)
    with col1:
        año = st.selectbox("Seleccione el año", años)
    with col2:
        trimestre = st.selectbox("Seleccione el trimestre", trimestres)

    # Filtrar hogares de 4 integrantes para el año y trimestre seleccionados
    hogares_filtrados = df_hogares[(df_hogares["ANO4"] == año) & (df_hogares["TRIMESTRE"] == trimestre) & (df_hogares["IX_TOT"] == 4)].copy()

    if hogares_filtrados.empty:
        st.warning("No hay datos de hogares de 4 integrantes para ese año y trimestre.")
        return

    # Obtener los 3 meses del trimestre
    meses_por_trimestre = {1: [1,2,3], 2: [4,5,6], 3: [7,8,9], 4: [10,11,12]}
    meses = meses_por_trimestre.get(trimestre, [])

    # Filtrar canasta básica para el año y meses del trimestre
    df_canasta["anio"] = pd.to_datetime(df_canasta["indice_tiempo"]).dt.year
    df_canasta["mes"] = pd.to_datetime(df_canasta["indice_tiempo"]).dt.month
    canasta_trim = df_canasta[(df_canasta["anio"] == año) & (df_canasta["mes"].isin(meses))]

    if canasta_trim.empty:
        st.warning("No hay datos de canasta básica para ese año y trimestre.")
        return

    # Calcular promedio trimestral de línea de pobreza e indigencia
    promedio_pobreza = canasta_trim["linea_pobreza"].mean()
    promedio_indigencia = canasta_trim["linea_indigencia"].mean()

    # Calcular hogares bajo línea de pobreza e indigencia (ponderados)
    hogares_filtrados["PONDERA"] = pd.to_numeric(hogares_filtrados["PONDERA"], errors="coerce").fillna(0)
    total_hogares = hogares_filtrados["PONDERA"].sum()
    bajo_pobreza = hogares_filtrados[hogares_filtrados["ITF"] < promedio_pobreza]
    bajo_indigencia = hogares_filtrados[hogares_filtrados["ITF"] < promedio_indigencia]
    total_bajo_pobreza = bajo_pobreza["PONDERA"].sum()
    total_bajo_indigencia = bajo_indigencia["PONDERA"].sum()

    st.subheader(f"Año {año} - Trimestre {trimestre}")
    st.write(f"Promedio línea de pobreza (trimestre): ${promedio_pobreza:,.2f}")
    st.write(f"Promedio línea de indigencia (trimestre): ${promedio_indigencia:,.2f}")
    st.metric("Total hogares (4 integrantes)", f"{int(total_hogares):,}")
    st.metric("Hogares bajo línea de pobreza", f"{int(total_bajo_pobreza):,} ({(total_bajo_pobreza/total_hogares*100):.2f}%)")
    st.metric("Hogares bajo línea de indigencia", f"{int(total_bajo_indigencia):,} ({(total_bajo_indigencia/total_hogares*100):.2f}%)")

    # Mostrar tabla resumen
    resumen = pd.DataFrame({
        "Categoría": ["Bajo línea de pobreza", "Bajo línea de indigencia"],
        "Cantidad ponderada": [int(total_bajo_pobreza), int(total_bajo_indigencia)],
        "Porcentaje": [total_bajo_pobreza/total_hogares*100, total_bajo_indigencia/total_hogares*100]
        })
    st.dataframe(resumen, hide_index=True)

# Main
if __name__ == '__main__':
    st.set_page_config(layout="wide")    
    hogares_bajo_linea_pobreza_indigencia()