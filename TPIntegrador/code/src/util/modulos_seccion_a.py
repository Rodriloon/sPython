from pathlib import Path
import csv
from csv import DictWriter

def actualizar_archivo(datos, ruta):

    with ruta.open("w", encoding="utf-8", newline="") as f:
        columnas = datos[0].keys()
        escritor = DictWriter(f, fieldnames=columnas, delimiter=";")
        escritor.writeheader()
        escritor.writerows(datos)

# MODULOS DE INDIVIDUOS

def punto3(datos_indiv):

    for fila in datos_indiv:
        ch04 = fila.get("CH04") 

        if ch04 == "1":
            fila["CH04_str"] = "Masculino"
        elif ch04 == "2":
            fila["CH04_str"] = "Femenino"
        elif ch04 == "" or ch04 is None:
            fila["CH04_str"] = "Dato faltante"
        else:
            fila["CH04_str"] = f"Valor desconocido ({ch04})"


def punto4 (datos_indiv):

    for fila in datos_indiv:
        nivel = fila.get("NIVEL_ED")

        if nivel == "1":
            fila["NIVEL_ED_str"] = "Primario incompleto"
        elif nivel == "2":
            fila["NIVEL_ED_str"] = "Primario completo"
        elif nivel == "3":
            fila["NIVEL_ED_str"] = "Secundario incompleto"
        elif nivel == "4":
            fila["NIVEL_ED_str"] = "Secundario completo"
        elif nivel in ["5", "6"]:
            fila["NIVEL_ED_str"] = "Superior o universitario"
        elif nivel == "" or nivel is None:
            fila["NIVEL_ED_str"] = "Dato faltante"
        elif nivel in ["7", "9"]:
            fila["NIVEL_ED_str"] = "Sin información"


def punto5_6(datos_indiv):
    # Procesa los datos para agregar las columnas CONDICION_LABORAL y UNIVERSITARIO
    for individuo in datos_indiv:
        estado = individuo.get('ESTADO')
        cat_ocup = individuo.get('CAT_OCUP')
        edad = individuo.get('CH06')    #CH06 = Edad cumplida del individuo
        nivel_edu = individuo.get('NIVEL_ED')

        # Lógica para CONDICION_LABORAL
        if estado == '1':
            if cat_ocup in ('1', '2'):
                individuo['CONDICION_LABORAL'] = 'Ocupado autónomo'
            elif cat_ocup in ('3', '4', '9'):
                individuo['CONDICION_LABORAL'] = 'Ocupado dependiente'
            else:
                individuo['CONDICION_LABORAL'] = 'Fuera de categoría/sin información'
        elif estado == '2':
            individuo['CONDICION_LABORAL'] = 'Desocupado'
        elif estado == '3':
            individuo['CONDICION_LABORAL'] = 'Inactivo'
        elif estado == '4':
            individuo['CONDICION_LABORAL'] = 'Fuera de categoría/sin información'
        else:
            individuo['CONDICION_LABORAL'] = 'Fuera de categoría/sin información'

        # Lógica para UNIVERSITARIO
        if edad is not None and nivel_edu is not None:
            try:
                edad = int(edad)
                if edad >= 18:
                    if nivel_edu == '6':    #NIVEL_ED 6 = Superior universitario completo 
                        individuo['UNIVERSITARIO'] = 1
                    else:
                        individuo['UNIVERSITARIO'] = 0
                else:
                    individuo['UNIVERSITARIO'] = 2
            except ValueError:
                individuo['UNIVERSITARIO'] = 2
        else:
            individuo['UNIVERSITARIO'] = 2

# MODULOS DE HOGAR
def punto7_9(datos_hogar):

    for hogar in datos_hogar:
        cantidad_personas = hogar.get('IX_TOT')    #Cantidad de miembros del hogar
        habitaciones = hogar.get('II2')     #Cantidad de ambientes/habitaciones usan habitualmente para dormir

        # Calcula TIPO_HOGAR
        if cantidad_personas is not None:
            cantidad_personas = int(cantidad_personas)
            if cantidad_personas == 1:
                hogar['TIPO_HOGAR'] = "Unipersonal"
            elif cantidad_personas in [2, 3, 4]:
                hogar['TIPO_HOGAR'] = "Nuclear"
            else:
                hogar['TIPO_HOGAR'] = "Extendido"
        else:
            hogar['TIPO_HOGAR'] = "No aplica"

        # Calcula DENSIDAD_HOGAR
        if habitaciones is not None and cantidad_personas is not None:
            try:
                habitaciones = int(habitaciones)
                if habitaciones > 0:
                    densidad = cantidad_personas / habitaciones
                    if densidad < 1:
                        hogar['DENSIDAD_HOGAR'] = "Bajo"
                    elif 1 <= densidad <= 2:
                        hogar['DENSIDAD_HOGAR'] = "Medio"
                    else:
                        hogar['DENSIDAD_HOGAR'] = "Alto"
                else:
                    hogar['DENSIDAD_HOGAR'] = "No aplica"
            except ValueError:
                hogar['DENSIDAD_HOGAR'] = "No aplica"
        else:
            hogar['DENSIDAD_HOGAR'] = "No aplica"



def punto8(datos_hogar):
    for fila in datos_hogar:
        v4 = fila["V4"]

        if v4 in ["1", "2", "3", "4"]:
            fila["MATERIAL_TECHUMBRE"] = "Material durable"
        elif v4 in ["5", "6", "7"]:
            fila["MATERIAL_TECHUMBRE"] = "Material precario"
        elif v4 == "9":
            fila["MATERIAL_TECHUMBRE"] = "No aplica"



def punto10(datos_hogar):
    for fila in datos_hogar:
        cocina = fila["II4_1"]
        agua = fila["IV6"]
        bano_tenencia = fila["II9"]
        piso = fila["IV3"]
        bano_exclusivo = fila["IV8"]
        techo = fila.get("MATERIAL_TECHUMBRE", "")

        if (
            cocina == "2" and
            agua == "3" and
            bano_tenencia in ["3", "4"] and
            piso == "3" and
            techo == "Material precario"
        ):
            fila["CONDICION_DE_HABITABILIDAD"] = "insuficiente"

        elif (
            cocina == "1" and
            agua == "3" and
            bano_tenencia == "2" and
            piso == "2" and
            techo == "Material precario"
        ):
            fila["CONDICION_DE_HABITABILIDAD"] = "regular"

        elif (
            cocina == "1" and
            agua == "2" and
            bano_exclusivo == "1" and
            piso in ["2", "3"] and
            techo == "Material durable"
        ):
            fila["CONDICION_DE_HABITABILIDAD"] = "saludables"

        elif (
            cocina == "1" and
            agua == "1" and
            bano_exclusivo == "1" and
            piso in ["2", "3"] and
            techo == "Material durable"
        ):
            fila["CONDICION_DE_HABITABILIDAD"] = "buena"

        else:
            fila["CONDICION_DE_HABITABILIDAD"] = "sin clasificar"