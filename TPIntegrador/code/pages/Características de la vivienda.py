import pandas as pd
import streamlit as st
from src.util.constantes import HOGARES_FUSIONADO
from src.util.data_processing import (cargar_hogares, filtrar_por_anio, resumen_material_predominante_pisos, resumen_viviendas_en_villa_emergencia, condicion_habitabilidad_por_aglomerado, viviendas_con_banio)
from src.util.plots import (grafico_pie_viviendas_por_tipo, grafico_barra_material_pisos, grafico_barra_villas)
from src.util.modulos_seccion_b import codigos_aglom
import matplotlib.pyplot as plt

#1.4.1
def mostrar_caracteristicas_vivienda():
    """
    Muestra la cantidad total de viviendas ponderadas para el año seleccionado.

    Carga los datos de hogares, los filtra por año según la selección del usuario y muestra el total de viviendas ponderadas.
    """
    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    datos_filtrados = filtrar_por_anio(datos_hogar, st.session_state.get('tab_year_filter', "Todos"))
    st.write("### Cantidad total de viviendas")
    total_viviendas = datos_filtrados["PONDERA"].sum()
    st.metric(label="Cantidad de viviendas ponderadas:", value=f"{int(total_viviendas):,}")

#1.4.2
def proporcion_viviendas_segun_tipo():
    """
    Muestra la proporción de viviendas según su tipo para el año seleccionado.

    Agrupa los datos de hogares filtrados por tipo de vivienda y suma los ponderadores.
    Presenta los resultados en un gráfico de torta y una tabla..
    """
    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    datos_filtrados = filtrar_por_anio(datos_hogar, st.session_state.get('tab_year_filter', "Todos"))
    if "TIPO_HOGAR" not in datos_filtrados.columns or "PONDERA" not in datos_filtrados.columns:
        st.error("Faltan columnas necesarias: 'TIPO_HOGAR' o 'PONDERA'")
        return
    resumen = (
        datos_filtrados
        .groupby("TIPO_HOGAR", as_index=False)["PONDERA"]
        .sum()
        .rename(columns={"PONDERA": "Total ponderado de viviendas", "TIPO_HOGAR": "Tipo de vivienda"})
    )
    st.subheader(" Proporción de viviendas según su tipo")
    st.pyplot(grafico_pie_viviendas_por_tipo(resumen))
    st.dataframe(resumen, hide_index=True)

#1.4.3
def material_predominante_pisos():
    """
    Muestra el material predominante en los pisos de las viviendas por aglomerado.

    Agrupa los datos de hogares filtrados para obtener el material más frecuente en los pisos por aglomerado,
    y presenta los resultados en un gráfico de barras y una tabla con nombres de aglomerados.
    """
    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    datos_filtrados = filtrar_por_anio(datos_hogar, st.session_state.get('tab_year_filter', "Todos"))
    df_mat = resumen_material_predominante_pisos(datos_filtrados)
    st.write("### Material predominante en pisos por aglomerado")
    st.write("Se muestra el material más frecuente en los pisos de las viviendas por aglomerado.")
    fig = grafico_barra_material_pisos(df_mat, codigos_aglom)
    st.pyplot(fig)
    df_tabla = df_mat.copy()
    df_tabla["Aglomerado"] = df_tabla["AGLOMERADO"].astype(str).map(codigos_aglom)
    df_tabla = df_tabla.drop(columns=["AGLOMERADO"])
    columnas = ["Aglomerado"] + [col for col in df_tabla.columns if col != "Aglomerado"]
    df_tabla = df_tabla[columnas]
    st.dataframe(df_tabla, hide_index=True)

#1.4.6
def viviendas_en_villa_emergencia():
    """
    Muestra el porcentaje de viviendas ubicadas en villas de emergencia por aglomerado.

    Agrupa los datos de hogares filtrados para calcular el porcentaje de viviendas en villas de emergencia por aglomerado,
    y presenta los resultados en un gráfico de barras y una tabla con nombres de aglomerados.
    """
    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    datos_filtrados = filtrar_por_anio(datos_hogar, st.session_state.get('tab_year_filter', "Todos"))
    df_villas = resumen_viviendas_en_villa_emergencia(datos_filtrados)
    st.write("### Porcentaje de viviendas en villa de emergencia por aglomerado")
    st.write("Porcentaje de viviendas ubicadas en villas de emergencia, agrupadas por aglomerado.")
    if df_villas is None or df_villas.empty:
        st.info("No hay datos disponibles para mostrar.")
        return
    fig = grafico_barra_villas(df_villas, codigos_aglom)
    st.pyplot(fig)
    df_tabla = df_villas.copy()
    df_tabla["Aglomerado"] = df_tabla["AGLOMERADO"].astype(str).map(codigos_aglom)
    df_tabla = df_tabla.drop(columns=["AGLOMERADO"])
    columnas = ["Aglomerado"] + [col for col in df_tabla.columns if col != "Aglomerado"]
    df_tabla = df_tabla[columnas]
    st.dataframe(df_tabla, hide_index=True)

#1.4.7
def mostrar_condicion_habitabilidad_por_aglomerado():
    """
    Muestra la cantidad y porcentaje de viviendas según su condición de habitabilidad en cada aglomerado.

    Agrupa los datos de hogares filtrados por aglomerado y condición de habitabilidad,
    calcula los totales y porcentajes, y presenta los resultados en una tabla descargable.

    """
    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    anio_filtro = st.session_state.get('tab_year_filter', "Todos")
    datos_filtrados = filtrar_por_anio(datos_hogar, anio_filtro)
    tabla = condicion_habitabilidad_por_aglomerado(datos_filtrados)  
    st.write("### Condición de habitabilidad por aglomerado")
    st.write("Cantidad y porcentaje de viviendas según su condición de habitabilidad en cada aglomerado (ponderadas).")
    tabla["Aglomerado"] = tabla["AGLOMERADO"].astype(str).map(codigos_aglom)
    tabla = tabla.drop(columns=["AGLOMERADO"])
    columnas = ["Aglomerado"] + [col for col in tabla.columns if col != "Aglomerado"]
    tabla = tabla[columnas]
    st.dataframe(tabla, use_container_width=True, hide_index=True)
    csv = tabla.to_csv(index=False, sep=";").encode("utf-8")
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name="porcentaje_viviendas_por_aglomerado.csv",
        mime="text/csv"
    )

#1.4.4
def viviendas_con_baño():
    """
    Muestra la proporción de viviendas que cuentan con baño por aglomerado.

    Agrupa los datos de hogares filtrados para calcular la proporción de viviendas con baño por aglomerado,
    y presenta los resultados en una tabla con nombres de aglomerados.
    """
    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    datos_filtrados = filtrar_por_anio(datos_hogar, st.session_state.get('tab_year_filter', "Todos"))
    proporcion = viviendas_con_banio(datos_filtrados)
    proporcion["AGLOMERADO"] = proporcion["AGLOMERADO"].astype(str).replace(codigos_aglom)
    st.write("### Proporción de viviendas con baño por aglomerado")
    st.write("Proporción de viviendas que cuentan con baño, agrupadas por aglomerado.")
    st.dataframe(proporcion, hide_index=True)

#1.4.5
def evolucion_tenencia():
    """
    Muestra la evolución de la tenencia de la vivienda por año para un aglomerado seleccionado.

    Permite al usuario seleccionar un aglomerado y tipos de tenencia, agrupa los datos filtrados por año y tipo de tenencia,
    y presenta la evolución en un gráfico de líneas.
    """
    tipos_tenencia = {
        1: "Propietario de la vivienda y terreno",
        2: "Propietario de la vivienda solamente",
        3: "Inquilino/arrendatario de la vivienda",
        4: "Ocupante por pago de impuestos/expensas",
        5: "Ocupante en relación de dependencia",
        6: "Ocupante gratuito (con permiso)",
        7: "Ocupante de hecho (sin permiso)",
        8: "Está en sucesión",
        9: "Otros"
    }

    datos_hogar = cargar_hogares(HOGARES_FUSIONADO)
    datos_filtrados = filtrar_por_anio(datos_hogar,st.session_state.get('tab_year_filter',"Todos"))
    codigo_para_nombre = {int(k):v for k, v in codigos_aglom.items()}
    nombre_por_codigo = {v:k for k , v in codigo_para_nombre.items()}
    nombre_aglomerado= st.selectbox("Seleccione un aglomerado",sorted(codigo_para_nombre.values()))
    codigo_aglome = int(nombre_por_codigo[nombre_aglomerado])

    df_aglom = datos_filtrados[datos_filtrados["AGLOMERADO"]== codigo_aglome]
    df_aglom = df_aglom[df_aglom['II7'].notna()]
    df_aglom['II7'] = df_aglom['II7'].astype(int)
    df_aglom=df_aglom[df_aglom['II7']!= 0]
    valores_tenencia = sorted(df_aglom['II7'].unique())
    nombres_tenencia = [tipos_tenencia[v]for v in valores_tenencia]
    seleccionados = st.multiselect("Selecciona tipo(s) de tenencia ",nombres_tenencia,default=nombres_tenencia)

    valores_seleccionados = [k for k,v in tipos_tenencia.items()if v in seleccionados]

    df_aglom = df_aglom[df_aglom["II7"].isin(valores_seleccionados)]

    df_agrupado = df_aglom.groupby(["ANO4", "II7"])["PONDERA"].sum().reset_index(name="cantidad")
    df_agrupado["Tenencia"] = df_agrupado["II7"].map(tipos_tenencia)

    df_pivot = df_agrupado.pivot(index="ANO4", columns="Tenencia", values="cantidad").fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    try:
        df_pivot.plot(ax=ax, marker='o')
        ax.set_title("Evolución de la tenencia de la vivienda por año")
        ax.set_xlabel("Año")
        ax.set_ylabel("Cantidad de hogares")
        ax.legend(title="Tipo de tenencia", bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True)
        
        st.pyplot(fig)
    except:
        st.warning("No se ha seleccionado ninguna opción.")

# Main
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    # Lee el archivo de hogares una vez para obtener los años disponibles para el filtro
    try:
        # Usamos usecols para cargar solo la columna 'ANO4' para mayor eficiencia
        df_temp_years = pd.read_csv(HOGARES_FUSIONADO, sep=";", encoding="utf-8", usecols=['ANO4'])
        df_temp_years['ANO4'] = pd.to_numeric(df_temp_years['ANO4'], errors='coerce').fillna(0).astype(int)
        años_disponibles = sorted(df_temp_years['ANO4'].unique())
        opciones_años = ["Todos"] + [str(año) for año in años_disponibles if año > 0]
    except FileNotFoundError:
        st.error(f"Error: No se pudo leer el archivo de hogares en la ruta: {HOGARES_FUSIONADO} para el filtro de año. Asegúrate de que el archivo exista y la ruta sea correcta.")
        opciones_años = ["Todos"] # Si hay error, solo se permite la opción "Todos"
    except KeyError:
        st.error("Error: La columna 'ANO4' no se encuentra en el archivo de hogares. El filtro de año no funcionará correctamente.")
        opciones_años = ["Todos"]

    # Inicializar st.session_state para el año seleccionado de esta pestaña si no existe
    if 'tab_year_filter' not in st.session_state:
        st.session_state.tab_year_filter = "Todos"

    # Mostrar el selectbox del filtro de año al inicio de esta pestaña
    st.header("Filtro para toda la página:")
    st.markdown("Seleccione un año o todos para explorar las características habitacionales de la población argentina en ese período. ")
    
    st.session_state.tab_year_filter = st.selectbox(
        "Seleccione un año o todos:",
        opciones_años,
        index=opciones_años.index(st.session_state.tab_year_filter),
        key="main_tab_year_selector" # Clave única para este widget
    )
    
    st.markdown("---") # Separador visual después del filtro
    mostrar_caracteristicas_vivienda()
    st.markdown("---")
    proporcion_viviendas_segun_tipo()
    st.markdown("---")
    material_predominante_pisos()
    st.markdown("---")
    viviendas_con_baño()
    st.markdown("---")
    evolucion_tenencia()
    st.markdown("---")
    viviendas_en_villa_emergencia()
    st.markdown("---")
    mostrar_condicion_habitabilidad_por_aglomerado()