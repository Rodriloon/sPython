from pathlib import Path

# ruta raíz del proyecto correspondiente a la carpeta TRABAJOINTEGRADOR
PROJECT_PATH = Path(__file__).resolve().parent.parent.parent

# carpeta donde se encuentran los archivos originales de EPH por trimestre, correspondiente a TRABAJOINTEGRADOR/files_eph/
FILES_PATH = PROJECT_PATH / "files_eph"

# carpeta donde se guardan los archivos fusionados de hogares e individuos, correspondiente a TRABAJOINTEGRADOR/fusion_eph/
FUSION_PATH = PROJECT_PATH / "fusion_eph"

# carpeta donde se guardan los archivos fusionados de hogares e individuos actualizados, correspondiente a TRABAJOINTEGRADOR/fusion_eph_actualizado/
INDIVIDUOS_FUSIONADO = FUSION_PATH / "individuos_fusionado_actualizado.csv"

# carpeta donde se guardan los archivos fusionados de hogares e individuos actualizados, correspondiente a TRABAJOINTEGRADOR/fusion_eph_actualizado/
HOGARES_FUSIONADO = FUSION_PATH / "hogares_fusionado_actualizado.csv"

# carpeta donde se guardan las coordenadas de los aglomerados 
COORDENADAS_JSON = PROJECT_PATH / "coordenadas" / "aglomerados_coordenadas.json"

# carpeta donde se guardan los archivos de ingresos
INGRESOS_PATH = PROJECT_PATH / "ingresos" / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv"