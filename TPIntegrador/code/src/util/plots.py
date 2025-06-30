import matplotlib.pyplot as plt

#1.4.2
def grafico_pie_viviendas_por_tipo(resumen):
    """
    Genera un gráfico de torta con la proporción de viviendas según su tipo.

    Args:
        resumen: DataFrame con columnas 'Tipo de vivienda' y 'Total ponderado de viviendas'.
    """
    fig, ax = plt.subplots()
    ax.pie(
        resumen["Total ponderado de viviendas"],
        labels=resumen["Tipo de vivienda"],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white"}
    )
    ax.axis("equal")
    return fig

#1.4.3
def grafico_barra_material_pisos(df, codigos_aglom):
    """
    Genera un gráfico de barras con la cantidad de hogares según el material predominante en pisos por aglomerado.

    Args:
        df: DataFrame con columnas 'AGLOMERADO' y 'PONDERA'.
        codigos_aglom: Diccionario que mapea el código de aglomerado a su nombre.
    """
    df = df.copy()
    # Mapear el número al nombre del aglomerado
    df['Aglomerado'] = df['AGLOMERADO'].astype(str).map(codigos_aglom)
    df_sorted = df.sort_values('PONDERA', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_sorted['Aglomerado'], df_sorted['PONDERA'], color='skyblue')
    ax.set_xlabel('Aglomerado')
    ax.set_ylabel('Cantidad de Hogares')
    ax.set_title('Material Predominante en Pisos por Aglomerado')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

#1.4.6
def grafico_barra_villas(df, codigos_aglom):
    """
    Genera un gráfico de barras con el porcentaje de viviendas en villa de emergencia por aglomerado.

    Args:
        df: DataFrame con columnas 'AGLOMERADO' y 'Porcentaje'.
        codigos_aglom: Diccionario que mapea el código de aglomerado a su nombre.
    """
    df = df.copy()
    df['Aglomerado'] = df['AGLOMERADO'].astype(str).map(codigos_aglom)
    df_sorted = df.sort_values('Porcentaje', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_sorted['Aglomerado'], df_sorted['Porcentaje'], color='tomato')
    ax.set_xlabel('Aglomerado')
    ax.set_ylabel('Porcentaje de viviendas en villa (%)')
    ax.set_title('Porcentaje de viviendas en villa de emergencia por aglomerado')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

#1.5.1
def grafico_barras_desocupados_estudio(resumen_filtrado):
    """
    Genera un gráfico de barras con la cantidad de personas desocupadas según el nivel de estudios alcanzado.

    Args:
        resumen_filtrado: DataFrame con columnas 'Estudios alcanzados' y 'Cantidad de Personas'.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(resumen_filtrado['Estudios alcanzados'], resumen_filtrado['Cantidad de Personas'], color='lightcoral')
    ax.set_xlabel('Estudios Alcanzados')
    ax.set_ylabel('Cantidad de Personas Desocupadas')
    ax.set_title('Desocupados por Nivel de Estudios')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

#1.5.2
def grafico_evolucion_tasa_desempleo(comparacion, aglo_seleccionado, codigos_aglom):
    """
    Genera un gráfico de líneas con la evolución de la tasa de desempleo para un aglomerado seleccionado.

    Args:
        comparacion: DataFrame con columnas 'Periodo' y 'Tasa_desempleo'.
        aglo_seleccionado: Código del aglomerado seleccionado.
        codigos_aglom: Diccionario que mapea el código de aglomerado a su nombre.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(comparacion["Periodo"], comparacion["Tasa_desempleo"], marker='o')
    ax.set_xlabel("Período (Año Trimestre)")
    ax.set_ylabel("Tasa de desempleo (%)")
    titulo = f"Evolución tasa de desempleo - {codigos_aglom.get(str(aglo_seleccionado), 'Todos los aglomerados')}"
    ax.set_title(titulo)
    ax.grid(True)
    plt.tight_layout()
    return fig

# 1.3.2
def grafico_edad_promedio_aglomerado(resumen_edad, max_anio, max_trimestre, codigos_aglom):
    """
    Genera un gráfico de barras horizontales con la edad promedio ponderada por aglomerado.

    Args:
        resumen_edad: DataFrame con columnas 'Aglomerado' y 'Edad Promedio Ponderada'.
        max_anio: Año del período mostrado.
        max_trimestre: Trimestre del período mostrado.
        codigos_aglom: Diccionario que mapea el código de aglomerado a su nombre.
    """
    df = resumen_edad.copy()
    if 'AGLOMERADO' in df.columns:
        df['Aglomerado'] = df['AGLOMERADO'].astype(str).map(codigos_aglom)
    df_sorted = df.sort_values('Edad Promedio Ponderada', ascending=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(df_sorted['Aglomerado'], df_sorted['Edad Promedio Ponderada'], color='skyblue')
    ax.set_xlabel('Edad Promedio Ponderada')
    ax.set_ylabel('Aglomerado')
    ax.set_title(f'Edad Promedio por Aglomerado - Año {max_anio}, Trimestre {max_trimestre}')
    plt.tight_layout()
    return fig

# 1.3.3
def grafico_dependencia_demografica(comparacion):
    """
    Genera un gráfico de líneas con el índice de dependencia demográfica a lo largo del tiempo.

    Args:
        comparacion: DataFrame con columnas 'Periodo' y 'Dependencia'.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(comparacion["Periodo"], comparacion["Dependencia"], marker="o", color="green")
    ax.set_xlabel("Periodo")
    ax.set_ylabel("Dependencia (%)")
    ax.set_title("Índice de Dependencia Demográfica")
    ax.grid(True)
    plt.tight_layout()
    return fig

# 1.3.1
def grafico_poblacion_edad_genero(df_agrupado, año, trimestre):
    """
    Genera un gráfico de barras apiladas con la distribución de la población por grupo de edad y sexo.

    Args:
        df_agrupado: DataFrame agrupado por grupo de edad y sexo.
        año: Año del período mostrado.
        trimestre: Trimestre del período mostrado.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    df_agrupado.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e'])
    ax.set_title(f"Distribución por grupo de edad y sexo - {año} T{trimestre}")
    ax.set_xlabel("Grupo de Edad")
    ax.set_ylabel("Cantidad de Personas")
    ax.legend(title="Sexo", loc='upper right')
    plt.tight_layout()
    return fig

#1.6.1
def grafico_nivel_educativo_anual(resumen_filtrado, anio_seleccionado):
    """
    Genera un gráfico de barras horizontales con la cantidad de personas por nivel educativo para un año seleccionado.

    Args:
        resumen_filtrado: DataFrame con columnas 'Nivel Educativo' y 'Cantidad de Personas'.
        anio_seleccionado: Año seleccionado.
    """
    resumen_sorted = resumen_filtrado.sort_values(by='Cantidad de Personas', ascending=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(resumen_sorted['Nivel Educativo'], resumen_sorted['Cantidad de Personas'], color='lightseagreen')
    ax.set_xlabel('Cantidad de Personas')
    ax.set_ylabel('Nivel Educativo Alcanzado')
    ax.set_title(f'Cantidad de Personas por Nivel Educativo - Año {anio_seleccionado}')
    # Agregar etiquetas de valor al final de cada barra
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{int(width):,}',  # separador de miles
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va='center',
                    ha='left',
                    fontsize=10,
                    color='black')
    plt.tight_layout()
    return fig

#1.6.4
def grafico_lectura_escritura(resumen):
    """
    Genera un gráfico de líneas con la evolución del porcentaje de personas mayores de 6 años capaces e incapaces de leer y escribir.

    Args:
        resumen: DataFrame con columnas 'Año', 'Porcentaje Capaces' y 'Porcentaje Incapaces'.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(resumen["Año"], resumen["Porcentaje Capaces"], marker='o', label="Capaces de leer y escribir")
    ax.plot(resumen["Año"], resumen["Porcentaje Incapaces"], marker='o', label="Incapaces de leer y escribir")
    ax.set_xlabel("Año")
    ax.set_ylabel("Porcentaje (%)")
    ax.set_title("Porcentaje de personas mayores a 6 años capaces/incapaces de leer y escribir")
    ax.legend()
    plt.tight_layout()
    return fig