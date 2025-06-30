# Encuest.AR — Trabajo Integrador EPH

Este proyecto carga, fusiona y procesa los datos de la Encuesta Permanente de Hogares (EPH), generando visualizaciones y análisis a través de notebooks y una interfaz en Streamlit.

## 👥 Integrantes del grupo

- Violeta Paz Villavicencio 
- Esteban Forloni
- Rodrigo Javier Martinez 
- Tomas Ressia 
- Benjamin Cardozo

## 📁 Estructura del proyecto

- `files_eph/`: Contiene los archivos originales por trimestre.
- `fusion_eph/`: Contiene los archivos unificados de hogares e individuos.
- `notebooks/`: Notebooks Jupyter de procesamiento.
- `src/util/`: Funciones auxiliares y configuración de rutas.
- `pages/`: Páginas de la aplicación Streamlit.
- `requirements.txt`: Lista de dependencias necesarias.
- `main.py`: Archivo principal para ejecutar la app Streamlit.

## 💻 Cómo ejecutar el proyecto

1. **Clonar el repositorio:**  
   ```bash
   git clone git@gitlab.catedras.linti.unlp.edu.ar:python-2025/proyectos/grupo22/code.git
   cd code
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado):**  
   - En Linux/Mac:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - En Windows:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instalar las dependencias:**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación Streamlit:**  
   ```bash
   streamlit run main.py
   ```

## 🔎 Requisitos del proyecto

- Python 3.10 o superior
- Las siguientes bibliotecas de Python (todas incluidas en `requirements.txt`):
  - streamlit
  - notebook
  - matplotlib
  - pandas
  - numpy
  - pydeck

## 📝 Notas

- Los archivos `.csv` originales de la EPH deben colocarse dentro de `files_eph/`.
- Las notebooks permiten explorar, fusionar y limpiar los datos.
- La interfaz de usuario en Streamlit permite visualizar estadísticas y gráficos de forma interactiva.