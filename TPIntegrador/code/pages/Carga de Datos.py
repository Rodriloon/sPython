import streamlit as st
import csv
from src.util.constantes import FUSION_PATH, FILES_PATH
from src.util.fusionador import fusionar_csv
import src.util.modulos_seccion_a as mod

def main():
    """
    Página principal para la carga y actualización de datos del sistema.

    Permite visualizar el rango de fechas de los datos cargados y actualizar el dataset fusionado.
    Verifica la existencia de los archivos necesarios antes de actualizar y muestra mensajes de éxito o error.
    """
    st.sidebar.title("CensAR")
    st.title("Carga de Datos")
    st.markdown("---")
    mostrar_fecha(FUSION_PATH / 'hogares_fusionado_actualizado.csv')
    st.markdown("---")
    if st.button("Actualizar dataset"):
        faltantes = archivos_faltantes(FILES_PATH)
        if faltantes:
            st.error("Faltan archivos necesarios para la actualización:")
            for mensaje in faltantes:
                st.write(mensaje)
            return
        else:
            st.success("No hay faltante de archivos.")
        actualizar_dataset()
        st.success("Dataset actualizado correctamente.")
    st.markdown("---")

def archivos_faltantes(ruta) -> list[str]:
    """
    Verifica si existen los archivos de hogares e individuos necesarios en cada subcarpeta de la ruta dada.

    Recorre las subcarpetas de la ruta y chequea la presencia de archivos que comiencen con 'usu_hogar' y 'usu_individual'.
    Si falta alguno, agrega un mensaje descriptivo a la lista de faltantes.

    Args:
        ruta: Ruta base (Path) donde buscar los archivos.

    Returns:
        Una lista de strings con los mensajes de archivos faltantes por subcarpeta.
    """
    faltantes = []
    if (ruta).is_dir():
        for subcarpeta in ruta.iterdir():
            if subcarpeta.is_dir():
                ok_hogar = False
                ok_indiv = False
                for archivo in subcarpeta.iterdir():
                    if archivo.is_file() and archivo.name.startswith("usu_hogar"):
                        ok_hogar = True
                    if archivo.is_file() and archivo.name.startswith("usu_individual"):
                        ok_indiv = True
                if (not ok_hogar or not ok_indiv):
                    año_trimestre = subcarpeta.name
                    if not ok_hogar:
                        faltantes.append(f"Falta el archivo 'usu_hogar_' en la carpeta {año_trimestre}.")
                    if not ok_indiv:
                        faltantes.append(f"Falta el archivo 'usu_individual_' en la carpeta {año_trimestre}.")
    return faltantes

def actualizar_fusionado_indiv(ruta):
    """
    Actualiza el archivo fusionado de individuos aplicando los puntos de procesamiento definidos en mod.

    Lee el archivo CSV de individuos, aplica los puntos de procesamiento (punto3, punto4, punto5_6)
    y guarda el archivo actualizado en la ruta correspondiente.

    Args:
        ruta: Ruta (Path) del archivo CSV de individuos fusionado.
    """
    with ruta.open(encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=";")
        datos_indiv = list(lector)
    
    mod.punto3(datos_indiv)
    mod.punto4(datos_indiv)
    mod.punto5_6(datos_indiv)
    ruta_actualizada = FUSION_PATH / "individuos_fusionado_actualizado.csv"
    mod.actualizar_archivo(datos_indiv, ruta_actualizada)

def actualizar_fusionado_hogar(ruta):
    """
    Actualiza el archivo fusionado de hogares aplicando los puntos de procesamiento definidos en mod.

    Lee el archivo CSV de hogares, aplica los puntos de procesamiento (punto7_9, punto8, punto10)
    y guarda el archivo actualizado en la ruta correspondiente.

    Args:
        ruta: Ruta (Path) del archivo CSV de hogares fusionado.
    """
    with ruta.open(encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=";")
        datos_hogar = list(lector)
    
    mod.punto7_9(datos_hogar)
    mod.punto8(datos_hogar)
    mod.punto10(datos_hogar)
    ruta_actualizada = FUSION_PATH / "hogares_fusionado_actualizado.csv"
    mod.actualizar_archivo(datos_hogar, ruta_actualizada)

def actualizar_dataset():
    """
    Fusiona los archivos de hogares e individuos y guarda los datasets actualizados.

    Llama a la función de fusión para hogares e individuos, y luego actualiza ambos archivos fusionados
    aplicando los puntos de procesamiento correspondientes.
    """
    salida_hogar = FUSION_PATH / "hogares_fusionado.csv"
    salida_individual = FUSION_PATH / "individuos_fusionado.csv"
    
    fusionar_csv("usu_hogar_", FILES_PATH, salida_hogar)
    fusionar_csv("usu_individual_", FILES_PATH, salida_individual)
    
    actualizar_fusionado_indiv(salida_individual)
    actualizar_fusionado_hogar(salida_hogar)

def mostrar_fecha(ruta):
    """
    Muestra el rango de fechas (año y trimestre) de los datos contenidos en el archivo fusionado.

    Lee el archivo CSV fusionado y determina el año y trimestre mínimo y máximo presentes,
    mostrando esa información en la interfaz de Streamlit.

    Args:
        ruta: Ruta (Path) del archivo CSV fusionado.
    """
    with open(ruta, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter=";")
        fechas = map(lambda x: (x['ANO4'], x['TRIMESTRE']), csv_reader)
        lista_fechas = list(fechas)
        min_ano = min(lista_fechas, key=lambda x: (x[0], x[1]))
        max_ano = max(lista_fechas, key=lambda x: (x[0], x[1]))
    st.write(f"El sistema contiene información desde el {int(min_ano[1]) * 3 - 2}/{int(min_ano[0])} hasta el {int(max_ano[1])*3}/{max_ano[0]}.")

if __name__ == "__main__":
    main()
