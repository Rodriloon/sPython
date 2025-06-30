import pandas as pd
import streamlit as st

def cargar_hogares(path):
    return pd.read_csv(path, sep=";", encoding="utf-8")

def cargar_individuos(path):
    return pd.read_csv(path, sep=";", encoding="utf-8")

def cargar_ingresos(path):
    return pd.read_csv(path, sep=",", encoding="utf-8")

def filtrar_por_anio(df, anio):
    """
    Filtra un DataFrame por año. Si el año es "Todos", devuelve una copia del DataFrame original.

    Args:
        df: DataFrame a filtrar.
        anio: Año a filtrar (int o "Todos").

    Returns:
        DataFrame filtrado por el año especificado.
    """
    if anio == "Todos":
        return df.copy()
    try:
        anio_int = int(anio)
        return df[df["ANO4"] == anio_int].copy()
    except Exception:
        return df.copy()

#1.4.3
def resumen_material_predominante_pisos(df):
    """
    Calcula el material predominante en los pisos de las viviendas por aglomerado.

    Args:
        df: DataFrame de hogares.

    Returns:
        DataFrame con el material predominante en pisos por aglomerado y la cantidad ponderada.
    """
    iv3_map = {
        '1': 'Mosaico/baldosa/madera/cerámica/alfombra',
        '2': 'Cemento/ladrillo fijo',
        '3': 'Ladrillo suelto/tierra',
        '4': 'Otros (especificar)',
        '9': 'No especificado / No responde',
        '': 'Sin dato'
    }
    df['IV3_str'] = df['IV3'].astype(str).map(iv3_map).fillna('Desconocido')
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str)
    conteo = df.groupby(['AGLOMERADO', 'IV3_str'])['PONDERA'].sum().reset_index()
    idx = conteo.groupby('AGLOMERADO')['PONDERA'].idxmax()
    return conteo.loc[idx][['AGLOMERADO', 'IV3_str', 'PONDERA']]

#1.4.6
def resumen_viviendas_en_villa_emergencia(df):
    """
    Calcula el porcentaje de viviendas ubicadas en villas de emergencia por aglomerado.

    Args:
        df: DataFrame de hogares.

    Returns:
        DataFrame con la cantidad y porcentaje de viviendas en villas por aglomerado.
    """
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str)
    df['IV12_3'] = pd.to_numeric(df['IV12_3'], errors='coerce')
    total = df.groupby('AGLOMERADO')['PONDERA'].sum().reset_index(name='Total')
    villas = df[df['IV12_3'] == 1].groupby('AGLOMERADO')['PONDERA'].sum().reset_index(name='Villas')
    resumen = pd.merge(villas, total, on='AGLOMERADO', how='left').fillna(0)
    resumen['Porcentaje'] = (resumen['Villas'] / resumen['Total'] * 100).round(2)
    return resumen[['AGLOMERADO', 'Villas', 'Porcentaje']]

#1.4.7
def condicion_habitabilidad_por_aglomerado(df):
    """
    Calcula la cantidad y porcentaje de viviendas según su condición de habitabilidad en cada aglomerado.

    Args:
        df: DataFrame de hogares.

    Returns:
        DataFrame con la cantidad ponderada y porcentaje por condición de habitabilidad y aglomerado.
    """
    tabla = (
        df.groupby(['AGLOMERADO', 'CONDICION_DE_HABITABILIDAD'])['PONDERA']
        .sum()
        .reset_index(name='Cantidad Ponderada')
    )
    total_por_aglo = tabla.groupby('AGLOMERADO')['Cantidad Ponderada'].transform('sum')
    tabla['Porcentaje'] = (tabla['Cantidad Ponderada'] / total_por_aglo * 100).round(2)
    return tabla

#1.4.4
def viviendas_con_banio(df):
    """
    Calcula la proporción de viviendas que cuentan con baño por aglomerado.

    Args:
        df: DataFrame de hogares.

    Returns:
        DataFrame con la proporción de viviendas con baño por aglomerado.
    """
    total_ponderados = df.groupby("AGLOMERADO")["PONDERA"].sum().reset_index(name="Total")
    con_banio = df[df["IV8"] == 1].groupby("AGLOMERADO")["PONDERA"].sum().reset_index(name="Viviendas con baño")
    proporcion = total_ponderados.merge(con_banio, on="AGLOMERADO", how="left").fillna(0)
    proporcion["Proporcion"] = (proporcion["Viviendas con baño"] / proporcion["Total"]).round(4)
    return proporcion

#1.5.1
def resumen_desocupados_por_estudio(path):
    """
    Calcula la cantidad de personas desocupadas agrupadas por nivel de estudios, año y trimestre.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        DataFrame con la cantidad de personas desocupadas por nivel educativo, año y trimestre.
        Devuelve None si no hay datos o faltan columnas necesarias.
    """
    try:
        datos_individuos = cargar_individuos(path)
    except FileNotFoundError:
        return None

    datos_individuos['ANO4'] = pd.to_numeric(datos_individuos['ANO4'], errors='coerce').fillna(0).astype(int)
    datos_individuos['TRIMESTRE'] = pd.to_numeric(datos_individuos['TRIMESTRE'], errors='coerce').fillna(0).astype(int)
    datos_individuos['PONDERA'] = pd.to_numeric(datos_individuos['PONDERA'], errors='coerce').fillna(0)
    if not {"ANO4", "TRIMESTRE", "CONDICION_LABORAL", "NIVEL_ED_str", "PONDERA"}.issubset(datos_individuos.columns):
        return None

    datos_desocupados = datos_individuos[datos_individuos["CONDICION_LABORAL"] == 'Desocupado'].copy()
    if datos_desocupados.empty:
        return None

    datos_desocupados['Estudios alcanzados'] = datos_desocupados['NIVEL_ED_str']
    resumen = (
        datos_desocupados
        .groupby(["ANO4", "TRIMESTRE", "Estudios alcanzados"])
        ['PONDERA'].sum()
        .reset_index(name="Cantidad de Personas")
    )
    return resumen

#1.5.2
def calcular_tasa_desempleo(path, codigos_aglom):
    """
    Calcula la evolución de la tasa de desempleo por período y aglomerado.

    Args:
        path: Ruta al archivo CSV de individuos.
        codigos_aglom: Diccionario que mapea el código de aglomerado a su nombre.

    Returns:
        comparacion: DataFrame con la tasa de desempleo por período.
        opciones_aglom: Lista de códigos de aglomerado disponibles.
        aglo_seleccionado: Código del aglomerado seleccionado.
    """
    try:
        df = pd.read_csv(path, delimiter=";", encoding="utf-8")
    except:
        return None, [], None

    df["ESTADO"] = pd.to_numeric(df["ESTADO"], errors="coerce")
    df["PONDERA"] = pd.to_numeric(df["PONDERA"], errors="coerce")
    df["ANO4"] = pd.to_numeric(df["ANO4"], errors="coerce")
    df["TRIMESTRE"] = pd.to_numeric(df["TRIMESTRE"], errors="coerce")

    opciones_aglom = ["Todos"] + sorted([str(a) for a in df["AGLOMERADO"].dropna().unique()])
    
    if "tasa_aglo_selector" in st.session_state:
        aglo_seleccionado = st.session_state["tasa_aglo_selector"]
    else:
        aglo_seleccionado = "Todos"
    
    opciones_visibles = [("Todos", "Todos")] + [(codigos_aglom.get(cod, f"Aglomerado {cod}"), cod) for cod in opciones_aglom if cod != "Todos"]
    seleccion = st.selectbox("Seleccione un aglomerado:", opciones_visibles, format_func=lambda x: x[0])  # nombre del aglom
    aglo_seleccionado = seleccion[1]

    if aglo_seleccionado != "Todos":
        df = df[df["AGLOMERADO"] == int(aglo_seleccionado)]

    activos = df[df["ESTADO"].isin([1, 2])]
    ocupados = (
        activos[activos["ESTADO"] == 1].copy()
        .groupby(["ANO4", "TRIMESTRE"])["PONDERA"]
        .sum()
        .reset_index(name="ocupados_ponderados")
    )
    desocupados = (
        activos[activos["ESTADO"] == 2].copy()
        .groupby(["ANO4", "TRIMESTRE"])["PONDERA"]
        .sum()
        .reset_index(name="desocupados_ponderados")
    )
    comparacion = ocupados.merge(desocupados, on=["ANO4", "TRIMESTRE"], how="outer").fillna(0)
    comparacion["Tasa_desempleo"] = (comparacion["desocupados_ponderados"] / (comparacion["ocupados_ponderados"] + comparacion["desocupados_ponderados"])) * 100
    comparacion = comparacion.sort_values(by=["ANO4", "TRIMESTRE"])
    comparacion["Periodo"] = comparacion["ANO4"].astype(int).astype(str) + " T" + comparacion["TRIMESTRE"].astype(int).astype(str)
    return comparacion, opciones_aglom, aglo_seleccionado

# 1.3.4
def resumen_media_mediana_edad(path):
    """
    Calcula la media, mediana y cantidad de datos de la edad por año y trimestre.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        DataFrame con la edad media, mediana y cantidad de personas por año y trimestre.
    """
    try:
        datos = cargar_individuos(path)
    except FileNotFoundError:
        return None
    
    columnas = {"ANO4", "TRIMESTRE", "CH06", "PONDERA"}
    if not columnas.issubset(datos.columns):
        return None

    datos["CH06"] = pd.to_numeric(datos["CH06"], errors="coerce")
    datos["PONDERA"] = pd.to_numeric(datos["PONDERA"], errors="coerce")
    # Eliminar filas con datos nulos
    datos = datos.dropna(subset=["CH06", "PONDERA"])

    resultados = []

    # agrupa por año y trimestre
    for (anio, trimestre), grupo in datos.groupby(["ANO4", "TRIMESTRE"]):
        edades = grupo["CH06"]
        pondera = grupo["PONDERA"]

        # media ponderada
        media = (edades * pondera).sum() / pondera.sum()

        # mediana ponderada
        df_ordenado = grupo.sort_values(by="CH06").copy().reset_index(drop=True)
        df_ordenado["acumulado"] = df_ordenado["PONDERA"].cumsum()
        mitad = df_ordenado["PONDERA"].sum() / 2
        fila_mediana = df_ordenado[df_ordenado["acumulado"] >= mitad].iloc[0]
        mediana = fila_mediana["CH06"]

        resultados.append({
            "Año": anio,
            "Trimestre": trimestre,
            "Edad media": round(media, 2),
            "Mediana edad":round(mediana,2),
            "Cantidad de personas": int(pondera.sum())
        })
    
    return pd.DataFrame(resultados).sort_values(by=["Año","Trimestre"])

# 1.3.2
def edad_promedio_por_aglomerado(path):
    """
    Calcula la edad promedio ponderada de personas por aglomerado para el último trimestre y año disponibles.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        resumen_edad: DataFrame con la edad promedio ponderada por aglomerado.
        max_anio: Año más reciente disponible.
        max_trimestre: Trimestre más reciente disponible.
    """
    try:
        datos = cargar_individuos(path)
    except FileNotFoundError:
        return None, None, None
    datos['ANO4'] = pd.to_numeric(datos['ANO4'], errors='coerce')
    datos['TRIMESTRE'] = pd.to_numeric(datos['TRIMESTRE'], errors='coerce')
    datos['CH06'] = pd.to_numeric(datos['CH06'], errors='coerce')
    datos['PONDERA'] = pd.to_numeric(datos['PONDERA'], errors='coerce')
    if datos.empty:
        return None, None, None
    max_anio = int(datos['ANO4'].max())
    datos_ultimo_anio = datos[datos['ANO4'] == max_anio]
    max_trimestre = int(datos_ultimo_anio['TRIMESTRE'].max())
    datos_filtrados = datos[
        (datos['ANO4'] == max_anio) & (datos['TRIMESTRE'] == max_trimestre)
    ].dropna(subset=['CH06', 'PONDERA'])
    if datos_filtrados.empty:
        return None, max_anio, max_trimestre
    datos_filtrados['AGLOMERADO'] = datos_filtrados['AGLOMERADO'].astype(str)
    resumen_edad = datos_filtrados.groupby('AGLOMERADO').apply(
        lambda x: (x['CH06'] * x['PONDERA']).sum() / x['PONDERA'].sum() if x['PONDERA'].sum() != 0 else 0
    ).reset_index(name='Edad Promedio Ponderada')
    resumen_edad['Edad Promedio Ponderada'] = resumen_edad['Edad Promedio Ponderada'].round(2)
    return resumen_edad, max_anio, max_trimestre

#1.3.3
def datos_dependencia_demografica(path, codigos_aglom):
    """
    Calcula el índice de dependencia demográfica por aglomerado y período.

    Args:
        path: Ruta al archivo CSV de individuos.
        codigos_aglom: Diccionario que mapea el código de aglomerado a su nombre.

    Returns:
        comparacion: DataFrame con el índice de dependencia por período.
        opciones_aglom: Lista de códigos de aglomerado disponibles.
        aglo_seleccionado: Código del aglomerado seleccionado.
    """
    try:
        df = cargar_individuos(path)
    except FileNotFoundError:
        return None, [], None
    df["CH06"] = pd.to_numeric(df["CH06"], errors="coerce")
    df["ANO4"] = pd.to_numeric(df["ANO4"], errors="coerce")
    df["TRIMESTRE"] = pd.to_numeric(df["TRIMESTRE"], errors="coerce")
    df = df.dropna(subset=["CH06", "ANO4", "TRIMESTRE"])

    opciones_aglom = ["Todos"] + sorted([str(a) for a in df["AGLOMERADO"].dropna().unique()])

    # Mostrar aglom por el nombre. El codigo debe ser string
    opciones_visibles = [("Todos", "Todos")] + [(codigos_aglom.get(cod, f"Aglomerado {cod}"), cod) for cod in opciones_aglom if cod != "Todos"] # Lista de tuplas (nombre, codigo)
    seleccion = st.selectbox("Seleccione un aglomerado:", opciones_visibles, format_func=lambda x: x[0])  # nombre del aglom
    aglo_seleccionado = seleccion[1]  # tomo el codigo del aglom elegido

    if aglo_seleccionado != "Todos":
        df = df[df["AGLOMERADO"] == int(aglo_seleccionado)]

    pob_activa = (
        df[(15 <= df["CH06"]) & (df['CH06'] <= 64)]
        .groupby(["ANO4", "TRIMESTRE"])["PONDERA"]
        .sum()
        .reset_index(name="Ponderados activa")
    )
    pob_pasiva = (
        df[(65 <= df["CH06"]) | (df['CH06'] < 15)]
        .groupby(["ANO4", "TRIMESTRE"])["PONDERA"]
        .sum()
        .reset_index(name="Ponderados pasiva")
    )

    comparacion = pob_activa.merge(pob_pasiva, on=["ANO4", "TRIMESTRE"], how="outer")
    comparacion['Dependencia'] = ((comparacion["Ponderados pasiva"] / comparacion["Ponderados activa"]) * 100).round(2)
    comparacion["Periodo"] = comparacion["ANO4"].astype(str) + " T" + comparacion["TRIMESTRE"].astype(str)
    comparacion = comparacion.sort_values(by=["Dependencia"])
    return comparacion, opciones_aglom, aglo_seleccionado

# 1.3.1
def datos_poblacion_edad_genero(path):
    """
    Calcula la distribución de la población por grupo de edad y sexo para un año y trimestre seleccionados.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        df_agrupado: DataFrame agrupado por grupo de edad y sexo.
        año: Año seleccionado.
        trimestre: Trimestre seleccionado.
    """
    try:
        df = cargar_individuos(path)
    except FileNotFoundError:
        return None, None, None
    columnas_necesarias = {'ANO4', 'TRIMESTRE', 'CH04', 'CH06'}
    if not columnas_necesarias.issubset(df.columns):
        return None, None, None
    años_disponibles = sorted(df['ANO4'].unique())
    año = st.selectbox("Selecciona un año", años_disponibles)
    trimestres_disponibles = sorted(df['TRIMESTRE'].unique())
    trimestre = st.selectbox("Seleccione un trimestre", trimestres_disponibles)
    df_filtrado = df[(df["ANO4"] == año) & (df["TRIMESTRE"] == trimestre)]
    if df_filtrado.empty:
        return None, año, trimestre
    grupos = pd.cut(
        df_filtrado['CH06'],
        bins=range(0, 101, 10),
        right=False,
        labels=[f'{i}-{i+9}' for i in range(0, 100, 10)]
    )
    df_agrupado = df_filtrado.groupby([grupos, df_filtrado['CH04']])['PONDERA'].sum().unstack(fill_value=0)
    return df_agrupado, año, trimestre

#1.6.1
def resumen_nivel_educativo_anual(path):
    """
    Calcula la cantidad de personas por nivel educativo para cada año.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        DataFrame con la cantidad de personas por nivel educativo y año.
    """
    try:
        datos = pd.read_csv(path, sep=";", encoding="utf-8")
    except FileNotFoundError:
        return None
    datos['ANO4'] = pd.to_numeric(datos['ANO4'], errors='coerce').fillna(0).astype(int)
    datos['PONDERA'] = pd.to_numeric(datos['PONDERA'], errors='coerce').fillna(0)
    if not {"ANO4", "NIVEL_ED_str", "PONDERA"}.issubset(datos.columns):
        return None
    datos['NIVEL_ED_str'] = datos['NIVEL_ED_str'].astype(str)
    resumen = datos.groupby(['ANO4', 'NIVEL_ED_str'])['PONDERA'].sum().reset_index(name='Cantidad de Personas')
    resumen = resumen.rename(columns={'ANO4': 'Año', 'NIVEL_ED_str': 'Nivel Educativo'})
    return resumen

#1.6.4
def resumen_lectura_escritura(path):
    """
    Calcula el porcentaje y cantidad de personas mayores de 6 años capaces e incapaces de leer y escribir, por año.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        DataFrame con los porcentajes y cantidades de personas capaces e incapaces de leer y escribir por año.
    """
    try:
        datos = pd.read_csv(path, sep=";", encoding="utf-8")
    except FileNotFoundError:
        return None
    if not {"ANO4", "CH06", "CH09", "PONDERA"}.issubset(datos.columns):
        return None
    datos_mayores_6 = datos[pd.to_numeric(datos['CH06'], errors='coerce') > 6].copy()
    if datos_mayores_6.empty:
        return None
    datos_mayores_6["CH09"] = datos_mayores_6["CH09"].astype(str).str.strip().str.lower()
    datos_mayores_6["capaz"] = datos_mayores_6["CH09"] == "1"
    datos_mayores_6["incapaz"] = datos_mayores_6["CH09"] == "2"
    resumen = datos_mayores_6.groupby("ANO4").apply(
        lambda df: pd.Series({
            "Capaces": df.loc[df["capaz"], "PONDERA"].sum(),
            "Incapaces": df.loc[df["incapaz"], "PONDERA"].sum()
        })
    ).reset_index()
    resumen["Porcentaje Capaces"] = ((resumen["Capaces"] / (resumen["Capaces"] + resumen["Incapaces"])) * 100).round(2)
    resumen["Porcentaje Incapaces"] = ((resumen["Incapaces"] / (resumen["Capaces"] + resumen["Incapaces"])) * 100).round(2)
    resumen = resumen.rename(columns={"ANO4": "Año"})
    return resumen

#1.6.2
def nivel_educacional_por_rango(path):
    """
    Calcula el nivel educacional más común por rango etario seleccionado.

    Args:
        path: Ruta al archivo CSV de individuos.

    Returns:
        DataFrame con el rango de edad y el nivel educacional más común para cada rango seleccionado.
    """
    niveles_dict = {
        1: "Jardín/preescolar",
        2: "Primario",
        3: "EGB",
        4: "Secundario",
        5: "Polimodal",
        6: "Terciario",
        7: "Universitario",
        8: "Posgrado universitario",
        9: "Educación especial (discapacitado)"
    }
    rangos = {
        "20-30": (20, 30),
        "30-40": (30, 40),
        "40-50": (40, 50),
        "50-60": (50, 60),
        "60+": (60, float('inf')),
    }
    
    try:
        df = pd.read_csv(path, sep=";", encoding="utf-8")
    except FileNotFoundError:
        return pd.DataFrame()
    
    df["CH06"] = pd.to_numeric(df["CH06"], errors="coerce")  # edad
    df["CH12"] = pd.to_numeric(df["CH12"], errors="coerce") # nivel
    
    st.subheader("Seleccione un rango etario para ver el nivel de educación alcanzado más común.")
    opciones = list(rangos.keys()) + ["Todos"]
    seleccionados = st.multiselect("Seleccione uno o más rangos etarios:", opciones)

    if "Todos" in seleccionados:
        seleccionados = list(rangos.keys())
    
    resultados = []

    for rango in seleccionados:
        edad_min, edad_max = rangos[rango]
        subset = df[(df["CH06"] >= edad_min) & (df["CH06"] < edad_max)]

        if not subset.empty:
            niveles_ponderados = subset.groupby("CH12")["PONDERA"].sum()

            if not niveles_ponderados.empty:
                nivel_mas_comun = niveles_ponderados.idxmax()
                descripcion = niveles_dict.get(nivel_mas_comun, f"Desconocido ({nivel_mas_comun})")
            else:
                descripcion = "Sin datos"
        else:
            descripcion = "Sin datos"

        resultados.append({
            "Rango de edad": rango,
            "Nivel educacional más común": descripcion
    })

    return pd.DataFrame(resultados)

#1.5.5
def calcular_evolucion_tasas_aglomerado(INDIVIDUOS_FUSIONADO):
    """
    Calcula la evolución de la tasa de empleo y desempleo por aglomerado entre el período más antiguo y el más reciente.

    Args:
        INDIVIDUOS_FUSIONADO: Ruta al archivo CSV de individuos fusionado.

    Returns:
        comparacion: DataFrame con la evolución de tasas por aglomerado.
        periodos: Tupla con el período más antiguo y el más reciente.
        error: Mensaje de error si corresponde, o None si no hay error.
    """
    try:
        df = pd.read_csv(INDIVIDUOS_FUSIONADO, sep=";", encoding="utf-8")
    except FileNotFoundError:
        return None, None, "No se encontró el archivo de individuos."

    df = df.dropna(subset=["ANO4", "TRIMESTRE", "ESTADO", "AGLOMERADO"])
    df["ANO4"] = pd.to_numeric(df["ANO4"].astype(str).str.strip(), errors="coerce")
    df["TRIMESTRE"] = pd.to_numeric(df["TRIMESTRE"].astype(str).str.strip(), errors="coerce")
    df["ESTADO"] = pd.to_numeric(df["ESTADO"], errors="coerce")
    df["AGLOMERADO"] = pd.to_numeric(df["AGLOMERADO"], errors="coerce")
    df = df.dropna(subset=["ANO4", "TRIMESTRE", "ESTADO", "AGLOMERADO"])

    # 1 ocupados y 0 desocupados
    df_validos = df[df["ESTADO"].isin([1, 2])]
    periodos = df_validos[["ANO4", "TRIMESTRE"]].drop_duplicates().sort_values(["ANO4", "TRIMESTRE"])

    if periodos.empty or len(periodos) < 2:
        return None, None, "No hay suficientes períodos con datos de empleo/desempleo para comparar."

    min_ano, min_trim = periodos.iloc[0]
    max_ano, max_trim = periodos.iloc[-1]

    def calcular_tasas_por_periodo(df_periodo, nombre_periodo):
        if df_periodo.empty:
            return pd.DataFrame()
        conteo = df_periodo.groupby(["AGLOMERADO", "ESTADO"]).size().unstack(fill_value=0)
        conteo = conteo.rename(columns={1: "Ocupados", 2: "Desocupados"})
        conteo["PEA"] = conteo.get("Ocupados", 0) + conteo.get("Desocupados", 0)
        conteo["Tasa_Empleo"] = (conteo["Ocupados"] / conteo["PEA"] * 100).round(2)
        conteo["Tasa_Desempleo"] = (conteo["Desocupados"] / conteo["PEA"] * 100).round(2)
        conteo["PERIODO"] = nombre_periodo
        return conteo.reset_index()

    df_antiguo = df_validos[(df_validos["ANO4"] == min_ano) & (df_validos["TRIMESTRE"] == min_trim)]
    df_reciente = df_validos[(df_validos["ANO4"] == max_ano) & (df_validos["TRIMESTRE"] == max_trim)]
    tasas_antiguo = calcular_tasas_por_periodo(df_antiguo, f"{min_ano}T{min_trim}")
    tasas_reciente = calcular_tasas_por_periodo(df_reciente, f"{max_ano}T{max_trim}")

    if tasas_antiguo.empty or tasas_reciente.empty:
        return None, None, "No hay datos suficientes para calcular tasas."

    comparacion = pd.merge(
        tasas_antiguo[["AGLOMERADO", "Tasa_Empleo", "Tasa_Desempleo"]],
        tasas_reciente[["AGLOMERADO", "Tasa_Empleo", "Tasa_Desempleo"]],
        on="AGLOMERADO", suffixes=("_ant", "_rec")
    )
    comparacion["Cambio_Empleo"] = comparacion["Tasa_Empleo_rec"] - comparacion["Tasa_Empleo_ant"]
    comparacion["Cambio_Desempleo"] = comparacion["Tasa_Desempleo_rec"] - comparacion["Tasa_Desempleo_ant"]
    comparacion["Empleo_Evolucion"] = comparacion["Cambio_Empleo"].apply(lambda x: "Aumentó" if x > 0 else "Disminuyó" if x < 0 else "Igual")
    comparacion["Desempleo_Evolucion"] = comparacion["Cambio_Desempleo"].apply(lambda x: "Aumentó" if x > 0 else "Disminuyó" if x < 0 else "Igual")

    return comparacion, (min_ano, min_trim, max_ano, max_trim), None
