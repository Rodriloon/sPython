1. Clonar el repositorio:
- git clone --depth 1 --filter=blob:none --sparse https://github.com/Rodriloon/sPython.git
- cd sPython
- git sparse-checkout set Entrega02
- cd Entrega02
2. Crear y activar un entorno virtual:
  En Windows:
- python -m venv venv
- venv\Scripts\activate
  En MacOS / Linux
- python3 -m venv venv
- source venv/bin/activate
3. Instalar dependencias:
Para ejecutar este proyecto, es necesario tener Python 3 instalado. Se recomienda utilizar un entorno virtual para instalar las dependencias.
- pip install -r requirements.txt
Si no tienes Jupyter instalado, puedes hacerlo con:
- pip install notebook 
4.Ejecucion del programa:
a. Para ejecutar el código, abre el notebook con Jupyter:
- jupyter notebook notebooks/ranking_notebook.ipynb
b. Tambien puedes ejecutar el codigo desde Python:
- python src/ranking.py
