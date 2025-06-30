import streamlit as st
from src.util.constantes import INDIVIDUOS_FUSIONADO, COORDENADAS_JSON
from src.util.data_processing import (resumen_desocupados_por_estudio, calcular_tasa_desempleo, cargar_individuos,calcular_evolucion_tasas_aglomerado)
from src.util.plots import (grafico_barras_desocupados_estudio, grafico_evolucion_tasa_desempleo)
from src.util.modulos_seccion_b import codigos_aglom
import json
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

#1.5.1
def estudios_de_personas_desocupadas():
    """
    Muestra la cantidad de personas desocupadas agrupadas por el nivel de estudios alcanzado,
    permitiendo al usuario seleccionar año y trimestre. Presenta los datos en una tabla y un gráfico de barras.

    Utiliza los datos fusionados de individuos para calcular el resumen de personas desocupadas según su nivel educativo,
    filtra por año y trimestre seleccionados por el usuario, y visualiza los resultados.
    """
    st.title("Actividad y Empleo")
    st.markdown("Cantidad de personas desocupadas según sus estudios alcanzados por año y trimestre.")
    resumen = resumen_desocupados_por_estudio(INDIVIDUOS_FUSIONADO)
    if resumen is None or resumen.empty:
        st.info("No hay personas desocupadas en el dataset para analizar.")
        return
    # Selección de año y trimestre por el usuario
    anios = sorted(resumen["ANO4"].unique(), reverse=True)
    trimestres = sorted(resumen["TRIMESTRE"].unique())
    col1, col2 = st.columns(2)
    with col1:
        anio_seleccionado = st.selectbox("Seleccione el año", anios)
    with col2:
        trimestre_seleccionado = st.selectbox("Seleccione el trimestre", trimestres)
    resumen_filtrado = resumen[(resumen["ANO4"] == anio_seleccionado) & (resumen["TRIMESTRE"] == trimestre_seleccionado)].copy()

    if resumen_filtrado.empty:
        st.info(f"No hay datos de personas desocupadas para el Año {anio_seleccionado}, Trimestre {trimestre_seleccionado}.")
        return
    st.subheader(f"Cantidad de personas desocupadas según estudios alcanzados - Año {anio_seleccionado}, Trimestre {trimestre_seleccionado}")
    st.write("Se muestra la cantidad de personas desocupadas agrupadas por el nivel de estudios alcanzado.")
    st.dataframe(resumen_filtrado[["Estudios alcanzados", "Cantidad de Personas"]].sort_values(by="Cantidad de Personas", ascending=False), hide_index=True)
    st.subheader("Distribución Gráfica")
    fig = grafico_barras_desocupados_estudio(resumen_filtrado)
    st.pyplot(fig)

#1.5.2
def tasa_desempleo():
    """
    Visualiza la evolución de la tasa de desempleo por período y aglomerado.

    Calcula la tasa de desempleo utilizando los datos de individuos fusionados y permite al usuario
    seleccionar el aglomerado de interés. Muestra la evolución de la tasa en un gráfico de líneas.
    """
    st.subheader("Evolución de la tasa de desempleo (%)")
    st.write("Visualización de la evolución de la tasa de desempleo por período y aglomerado.")

    comparacion, opciones_aglom, aglo_seleccionado = calcular_tasa_desempleo(INDIVIDUOS_FUSIONADO, codigos_aglom)
    if comparacion is None or comparacion.empty:
        st.info("No hay datos para calcular la tasa de desempleo.")
        return

    fig = grafico_evolucion_tasa_desempleo(comparacion, aglo_seleccionado, codigos_aglom)
    st.pyplot(fig)

#1.5.3
def evolucion_empleo():
    """
    Muestra la evolución de la tasa de empleo a lo largo de los años, permitiendo seleccionar un aglomerado.

    Permite al usuario seleccionar un aglomerado específico o ver el total país. Calcula la tasa de empleo
    como el porcentaje de ocupados sobre la suma de ocupados y desocupados, y la muestra en una tabla y un gráfico de líneas.
    """
    st.title("Evolucion de la tasa de empleo")
    datos_individuo= INDIVIDUOS_FUSIONADO
    individuos = cargar_individuos(datos_individuo).copy()
    individuos['AGLOMERADO'] = individuos['AGLOMERADO'].astype(int)

    opciones = ['Todo el país'] + list(codigos_aglom.values())
    seleccion = st.selectbox("Seleccioná un aglomerado", opciones)

    if seleccion != 'Todo el país':
        codigo_aglo = [int(k) for k, v in codigos_aglom.items() if v == seleccion]
        if codigo_aglo:
            codigo_seleccionado = codigo_aglo[0]
            individuos = individuos[individuos['AGLOMERADO'] == codigo_seleccionado]
        else:
            st.error("Aglomerado no encontrado")
            return

    ocupados = individuos[individuos['ESTADO'] == 1].groupby('ANO4')['PONDERA'].sum()
    desocupados = individuos[individuos['ESTADO'] == 2].groupby('ANO4')['PONDERA'].sum()

    tasa_empleo = (ocupados / (ocupados + desocupados)) * 100
    tasa_empleo = tasa_empleo.sort_index()

    st.dataframe(tasa_empleo.reset_index(name='Tasa de empleo (%)'), hide_index=True)
    fig, ax = plt.subplots()
    ax.plot(tasa_empleo.index, tasa_empleo.values, marker='o', color='green')
    ax.set_title('Evolución de la tasa de empleo')
    ax.set_xlabel('Año')
    ax.set_ylabel('Tasa de empleo (%)')
    ax.grid(True)
    st.pyplot(fig)


#1.5.5
def evolucion_en_mapa():
    """
    Muestra en un mapa la evolución de la tasa de empleo o desempleo por aglomerado,
    comparando el período más antiguo y el más reciente.

    Carga las tasas de empleo y desempleo por aglomerado, las une con las coordenadas geográficas,
    y visualiza en un mapa los cambios de tasa entre dos períodos, usando colores para indicar aumento o disminución.
    """
    st.subheader("Evolución de tasas por aglomerado")
    st.write("Comparación de la tasa de empleo o desempleo entre el período más antiguo y el más reciente.")

    comparacion, periodos, error = calcular_evolucion_tasas_aglomerado(INDIVIDUOS_FUSIONADO)
    if error:
        st.error(error)
        return

    min_ano, min_trim, max_ano, max_trim = periodos
    st.markdown(f"**Comparando período:** {int(min_ano)}T{int(min_trim)} ➜ {int(max_ano)}T{int(max_trim)}")

    # Cargar coordenadas
    try:
        with open(COORDENADAS_JSON, encoding="utf-8") as f:
            datos_json = json.load(f)
    except FileNotFoundError:
        st.error("No se encontró el archivo de coordenadas de aglomerados.")
        return

    lista_coords = []
    for cod, info in datos_json.items():
        lista_coords.append({
            "AGLOMERADO": int(cod),
            "NOMBRE_AGLOMERADO": info["nombre"],
            "LAT": info["coordenadas"][0],
            "LON": info["coordenadas"][1]
        })
    df_coords = pd.DataFrame(lista_coords)

    # Unir tasas con coordenadas
    df_mapa = pd.merge(comparacion, df_coords, on="AGLOMERADO", how="inner")

    # Selección de tasa a visualizar
    tipo_tasa = st.radio("¿Qué tasa desea visualizar?", ["Tasa de empleo", "Tasa de desempleo"])

    st.markdown("""**¿Cómo se calculan las tasas?**  
    - **Tasa de empleo** = (personas ocupadas / PEA) × 100  
    - **Tasa de desempleo** = (personas desocupadas / PEA) × 100  
    Donde **PEA** = Ocupados + Desocupados.""")

    if tipo_tasa == "Tasa de empleo":
        st.markdown("🟢 **Verde**: la tasa de empleo aumentó &nbsp;&nbsp;&nbsp; 🔴 **Rojo**: la tasa de empleo disminuyó")
    else:
        st.markdown("🔴 **Rojo**: la tasa de desempleo aumentó &nbsp;&nbsp;&nbsp; 🟢 **Verde**: la tasa de desempleo disminuyó")

    # Asignar colores
    df_mapa["COLOR"] = df_mapa.apply(lambda row:
        [0, 200, 0] if (row["Cambio_Empleo"] > 0 and tipo_tasa == "Tasa de empleo") or
                       (row["Cambio_Desempleo"] < 0 and tipo_tasa == "Tasa de desempleo") else
        [200, 0, 0] if (row["Cambio_Empleo"] < 0 and tipo_tasa == "Tasa de empleo") or
                       (row["Cambio_Desempleo"] > 0 and tipo_tasa == "Tasa de desempleo") else
        [180, 180, 180], axis=1)

    # Mostrar mapa
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=-38, longitude=-64, zoom=3.3, pitch=0),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_mapa,
                get_position=["LON", "LAT"],
                get_fill_color="COLOR",
                get_radius=50000,
                pickable=True
            )
        ],
        tooltip={
            "text": "Aglomerado: {NOMBRE_AGLOMERADO}\nEmpleo: {Tasa_Empleo_rec}%\nDesempleo: {Tasa_Desempleo_rec}%"
        }
    ))

#1.5.4
def empleo_por_aglomerado():
    """
    Muestra el total y el porcentaje de personas empleadas por tipo de empleo (estatal, privado, otro)
    para cada aglomerado.

    Lee los datos de individuos, clasifica el tipo de empleo según el código, agrupa y suma los ponderadores,
    calcula los porcentajes por tipo de empleo y muestra los resultados en una tabla.
    """
    st.subheader("Empleo por aglomerado: total y porcentaje por tipo de empleo")

    try:
        df = pd.read_csv(INDIVIDUOS_FUSIONADO, sep=";", encoding="utf-8")
    except FileNotFoundError:
        st.error("No se encontró el archivo de individuos.")
        return

    # Clasificación de tipo de empleo según PP04A (1: estatal, 2: privado, 3: otro tipo)
    df["TIPO_EMPLEO"] = df["PP04A"].map({
        1: "Empleo estatal",
        2: "Empleo privado",
        3: "Otro tipo"
    })

    # Agrupar y sumar ponderador
    tabla = (
        df
        .groupby(["AGLOMERADO", "TIPO_EMPLEO"])["PONDERA"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Calcular totales y porcentajes
    tabla["Total personas"] = tabla[["Empleo estatal", "Empleo privado", "Otro tipo"]].sum(axis=1)
    tabla["% estatal"] = (tabla["Empleo estatal"] / tabla["Total personas"] * 100).round(2)
    tabla["% privado"] = (tabla["Empleo privado"] / tabla["Total personas"] * 100).round(2)
    tabla["% otro tipo"] = (tabla["Otro tipo"] / tabla["Total personas"] * 100).round(2)

    tabla["AGLOMERADO"] = tabla["AGLOMERADO"].astype(str).replace(codigos_aglom)
    st.dataframe(
        tabla[["AGLOMERADO", "Total personas", "% estatal", "% privado", "% otro tipo"]],
        hide_index=True)

# Main
if __name__ == '__main__':
    st.set_page_config(layout="wide")
    estudios_de_personas_desocupadas()
    st.markdown('---')
    tasa_desempleo()
    st.markdown('---')
    evolucion_empleo()
    st.markdown('---')
    empleo_por_aglomerado()
    st.markdown('---')
    evolucion_en_mapa()