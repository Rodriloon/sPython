from pathlib import Path

"""
Une todos los archivos CSV que comienzan con un nombre dado en subcarpetas de `carpeta_entrada`
y los guarda en `archivo_salida`.

Parámetros:
- nombre_prefijo (str): ej 'usu_hogar_' o 'usu_individual_'
- carpeta_entrada (Path): carpeta principal que contiene las subcarpetas con los archivos por trimestre.
- archivo_salida (Path): ruta donde se va a guardar el archivo CSV unificado.
"""

def fusionar_csv(nombre_prefijo: str, carpeta_entrada: Path, archivo_salida: Path):

    esta_encabezado = False

    with archivo_salida.open("w", encoding="utf-8") as salida:
        for subcarpeta in carpeta_entrada.iterdir():
            if not subcarpeta.is_dir():
                continue

            for archivo in subcarpeta.glob(f"{nombre_prefijo}*.txt"):
                with archivo.open(encoding="utf-8") as f:
                    encabezado = f.readline()
                    if not esta_encabezado:
                        salida.write(encabezado)
                        esta_encabezado = True
                    for linea in f:
                        salida.write(linea)

    print(f"fusion de archivos generado: {archivo_salida.name}")