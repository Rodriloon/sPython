from pathlib import Path
import csv
from collections import Counter
from collections import defaultdict

codigos_region = {
    "1": "Gran Buenos Aires",
    "40": "Noroeste",
    "41": "Noreste",
    "42": "Cuyo",
    "43": "Pampeana",
    "44": "Patagonia"
}


codigos_aglom = {
    "2": "Gran La Plata",
    "3": "Bahía Blanca - Cerri",
    "4": "Gran Rosario",
    "5": "Gran Santa Fé",
    "6": "Gran Paraná",
    "7": "Posadas",
    "8": "Gran Resistencia",
    "9": "Comodoro Rivadavia - Rada Tilly",
    "10": "Gran Mendoza",
    "12": "Corrientes",
    "13": "Gran Córdoba",
    "14": "Concordia",
    "15": "Formosa",
    "17": "Neuquén - Plottier",
    "18": "Santiago del Estero - La Banda",
    "19": "Jujuy - Palpalá",
    "20": "Río Gallegos",
    "22": "Gran Catamarca",
    "23": "Gran Salta",
    "25": "La Rioja",
    "26": "Gran San Luis",
    "27": "Gran San Juan",
    "29": "Gran Tucumán - Tafí Viejo",
    "30": "Santa Rosa - Toay",
    "31": "Ushuaia - Río Grande",
    "32": "Ciudad Autonoma de Buenos Aires",
    "33": "Partidos del GBA",
    "34": "Mar del Plata",
    "36": "Río Cuarto",
    "38": "San Nicolás - Villa Constitución",
    "91": "Rawson - Trelew",
    "93": "Viedma - Carmen de Patagones"
}

educativos = [
    "Primario incompleto",
    "Primario completo",
    "Secundario incompleto",
    "Secundario completo",
    "Superior o universitario"
]



from collections import defaultdict

def calcular_porcentaje_lectura_escritura(lista_individuos: list) -> dict:
    """
    Calcula el porcentaje de personas mayores de 6 años capaces e incapaces de leer y escribir, por año.
    Considera el último trimestre DISPONIBLE para cada año.

    Args:
        lista_individuos: Una lista de diccionarios, donde cada diccionario representa a un individuo
                          y debe contener las claves 'ANO4' (año), 'TRIMESTRE' (trimestre),
                          'CH06' (edad), y 'CH09' (sabe leer y escribir).

    Returns:
        Un diccionario donde las claves son los años, y los valores son diccionarios con las claves
        'porcentaje_pueden_leer_escribir' y 'porcentaje_no_pueden_leer_escribir'.
        También se incluye el 'trimestre_considerado' para cada año en el resultado.
    """

    # --- Paso 1: Encontrar el último trimestre disponible para cada año ---
    latest_quarter_per_year = defaultdict(int) # Almacenará el trimestre máximo encontrado para cada año

    for individuo in lista_individuos:
        anio_str = individuo.get("ANO4")
        trimestre_str = individuo.get("TRIMESTRE")

        # Validación básica para asegurar que tenemos año y trimestre
        if anio_str is None or trimestre_str is None:
            continue

        try:
            anio = int(anio_str)
            trimestre = int(trimestre_str)
            # Actualiza el trimestre máximo si encontramos uno mayor para este año
            if trimestre > latest_quarter_per_year[anio]:
                latest_quarter_per_year[anio] = trimestre
        except (ValueError, TypeError):
            # Ignora si el año o el trimestre no son números válidos
            continue

    # --- Paso 2: Calcular los porcentajes usando el último trimestre determinado para cada año ---
    conteo_por_anio = defaultdict(lambda: {
        "total_mayores_6": 0,
        "pueden_leer_escribir": 0,
        "no_pueden_leer_escribir": 0,
        "trimestre_considerado": None # Para almacenar el trimestre que realmente se usó
    })

    for individuo in lista_individuos:
        anio_str = individuo.get("ANO4")
        trimestre_str = individuo.get("TRIMESTRE")
        edad_str = individuo.get("CH06")
        ch09 = individuo.get("CH09")

        # Validación básica para campos esenciales
        if anio_str is None or trimestre_str is None or edad_str is None or ch09 is None:
            continue

        try:
            anio = int(anio_str)
            edad = int(edad_str)
            current_trimestre = int(trimestre_str)
        except (ValueError, TypeError):
            continue # Saltar si la edad o el trimestre no son números válidos

        # Solo procesar si este individuo pertenece al último trimestre para su año
        # y si el año fue registrado en latest_quarter_per_year (es decir, tenía trimestre válido)
        if anio in latest_quarter_per_year and current_trimestre == latest_quarter_per_year[anio]:
            # Verifica si el individuo es mayor de 6 años
            if edad > 6:
                conteo_por_anio[anio]["total_mayores_6"] += 1
                conteo_por_anio[anio]["trimestre_considerado"] = latest_quarter_per_year[anio] # Guarda el trimestre usado

                # Clasifica si sabe leer/escribir o no
                if ch09 == "1":  # "1" representa "Sí"
                    conteo_por_anio[anio]["pueden_leer_escribir"] += 1
                elif ch09 == "2":  # "2" representa "No"
                    conteo_por_anio[anio]["no_pueden_leer_escribir"] += 1

    resultados = {}
    # Ordenar los años para que los resultados estén en orden cronológico
    for anio in sorted(conteo_por_anio.keys()):
        conteo = conteo_por_anio[anio]
        total_mayores_6 = conteo["total_mayores_6"]
        pueden_leer_escribir = conteo["pueden_leer_escribir"]
        no_pueden_leer_escribir = conteo["no_pueden_leer_escribir"]
        trimestre_considerado = conteo["trimestre_considerado"] # Recupera el trimestre considerado

        if total_mayores_6 > 0:
            porcentaje_pueden_leer_escribir = (pueden_leer_escribir / total_mayores_6) * 100
            porcentaje_no_pueden_leer_escribir = (no_pueden_leer_escribir / total_mayores_6) * 100
        else:
            porcentaje_pueden_leer_escribir = 0
            porcentaje_no_pueden_leer_escribir = 0

        resultados[anio] = {
            "porcentaje_pueden_leer_escribir": porcentaje_pueden_leer_escribir,
            "porcentaje_no_pueden_leer_escribir": porcentaje_no_pueden_leer_escribir,
            "trimestre_considerado": trimestre_considerado # Añadir al diccionario final
        }
    return resultados





def aglomerado_mas_viviendas(ruta):
    '''
    Imprime en pantalla el aglomerado que tiene más viviendas sin baño y mas de dos ocupantes, y cuántas.
    Args:
        ruta (Path): Debe contener la ruta en string del archivo de hogar actualizado.
    '''

    with open(ruta, encoding= "utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter= ";")
     
        sin_baño = filter(lambda x: x.get("IV8", "").strip() == "2", csv_reader)

        mas_ocupantes= list(filter(lambda x: int(x['IX_TOT']) > 2, sin_baño))

        #ponderado = sum(int(x['PONDERA']) for x in mas_ocupantes)
        result = Counter(x['AGLOMERADO'] for x in mas_ocupantes).most_common(1)

        if result:
            aglomerado, cantidad = result[0]
            ponderado = sum(int(x['PONDERA']) for x in mas_ocupantes if x['AGLOMERADO']== codigos_aglom.get(aglomerado, aglomerado))
            print(f"Aglomerado con más viviendas sin baño y con más de 2 ocupantes: {codigos_aglom.get(aglomerado, 'Código no válido')}")
            print(f"Cantidad de viviendas: {cantidad * ponderado}")
        else:
            print("No se encontraron viviendas que cumplan con las condiciones.")
    



def total_universitarios(ruta):
    '''
    Para cada aglomerado cuenta el total de individuos y cuántos cursan o cursaron nivel superior o universitario.
    Informa el porcentaje de universitarios por aglomerado.
    Args:
        ruta (Path): Debe ser el path del archivo individual actualizado.
    '''
    cod_universitario = {"5", "6"}

    
    with open(ruta, encoding = "utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter= ";")

        contador = {}
        for linea in csv_reader:
            aglomerado = linea["AGLOMERADO"]
            nivel = linea["NIVEL_ED"]
            ponderado = int(linea["PONDERA"])
            
            if aglomerado not in contador:
                contador[aglomerado] = {"total": 0, "universitarios": 0}
            
            contador[aglomerado]["total"] += ponderado

            if nivel in cod_universitario:
                contador[aglomerado]["universitarios"] += ponderado
        #print(contador)
        print("Porcentaje de individuos que cursaron nivel superior de cada aglomerado.")
        for aglom, datos in contador.items():
            if datos["total"] == 0:
                porcentaje = 0
            else:
                porcentaje = (datos["universitarios"] / datos["total"] * 100)
            
            print(F"Aglomerado {codigos_aglom.get(aglom, aglom)}: {porcentaje:.2f}% de personas cursaron el nivel superior o universitario.")




def porcentaje_inquilinos(ruta):
    ''' 
        Ordena e informa las regiones según el porcentaje de viviendas ocupadas por inquilinos.
        Args:
            ruta (Path): Debe contener el path del archivo actualizado de hogares.
    '''
    with open(ruta, encoding = "utf-8")as f:
        csv_reader = csv.DictReader(f, delimiter=";")

        contador = {}
        for linea in csv_reader:
            region = linea["REGION"]
            inquilinos = linea["II7"]
            ponderado = int(linea["PONDERA"])
            
            if region not in contador:
                contador[region] = {"total": 0, "inquilinos": 0}

            contador[region]["total"] += ponderado

            if inquilinos == "3":
                contador[region]["inquilinos"] += ponderado

        contador_ordenado = sorted(contador.items(), key=lambda x: (int(x[1]["inquilinos"]) / int(x[1]["total"])), reverse=True)

        #print(contador_ordenado)
        print("Regiones ordenadas por porcentaje de viviendas ocupadas por inquilinos de cada Region.")  
        for reg, datos in contador_ordenado:
            if datos["total"] == 0:
                porcentaje = 0
            else:
                porcentaje = (datos["inquilinos"] / datos["total"] * 100)
            
            print(f"{codigos_region.get(reg, reg)}: {porcentaje:.2f}% de inquilinos.")




def tabla_nivel_estudios(ruta):
    '''retorna una tabla que contenga la cantidad de personas mayores de edad según su
    nivel de estudios alcanzados.
    '''
    from collections import defaultdict

    print("Ingrese un aglomerado: (A modo de ejemplo usa el aglomerado 2: Gran La Plata)")
    aglom = "2"
    
    with open(ruta, encoding= "utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter= ";")
     
        datos_aglom = filter(lambda x: x["AGLOMERADO"] == aglom, csv_reader)

        datos_aglom_mayores = filter(lambda x: int(x["CH06"]) > 18, datos_aglom)
        

        datos_ordenados = sorted(datos_aglom_mayores, key=lambda x: (int(x['ANO4']), int(x['TRIMESTRE'])))

        tabla = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for linea in datos_ordenados:
            ano = linea["ANO4"]
            trim = linea['TRIMESTRE']
            nivel = linea['NIVEL_ED_str']
            ponderado = int(linea['PONDERA'])

            if nivel not in educativos:
                continue

            tabla[ano][trim][nivel] += ponderado

        #imprimo encabezado de la tabla
        print("-"*200)
        print(f"{'Año':<10} {'Trimestre':<12} {educativos[0]:<25} {educativos[1]:<25} {educativos[2]:<25} {educativos[3]:<25} {educativos[4]:<25}")
        print("-"*200)
        
        for ano in tabla:
            for trim in tabla[ano]:
                valores= list(tabla[ano][trim].values())
                print(f"{ano:<10} {trim:<15} {valores[0]:<25} {valores[1]:<25}{valores[2]:<25} {valores[3]:<25} {valores[4]:<25}")





def porcentaje_extranjeros_universitarios(datos: list, año: int, trimestre: int) -> float:
    """
    Retorna el porcentaje de personas no nacidas en Argentina (CH06 ≠ 1)
    que hayan cursado nivel universitario o superior (NIVEL_ED 5 o 6),
    para el año y trimestre indicados.
    """
    total_extranjeros = 0
    total_extranjeros_universitarios = 0

    for fila in datos:
        if int(fila["ANO4"]) == año and int(fila["TRIMESTRE"]) == trimestre:
            nacido_argentina = int(fila["CH06"]) == 1
            nivel_educativo = int(fila["NIVEL_ED"])
            pondera = int(fila["PONDERA"])

            if not nacido_argentina:
                total_extranjeros += pondera
                if nivel_educativo in (5, 6):
                    total_extranjeros_universitarios += pondera

    if total_extranjeros == 0:
        return 0.0  

    porcentaje = (total_extranjeros_universitarios / total_extranjeros) * 100
    return round(porcentaje, 2)



def menor_desocupacion(datos):
    """
    Calcula el año y trimestre con menor desocupación, considerando la ponderación.

    Args:
        datos (list): Lista de diccionarios con los datos de individuos.

    Returns:
        tupla: Año y trimestre con menor desocupación, o (0, 0) si no hay datos válidos.
    """
    desocupacion_por_periodo = {}

    for fila in datos:
        # Validar que los campos necesarios existan
        ano = fila.get("ANO4")
        trimestre = fila.get("TRIMESTRE")
        condicion = fila.get("CONDICION_LABORAL")
        pondera = fila.get("PONDERA")

        if condicion == "Desocupado":
            periodo = (int(ano), int(trimestre))
            desocupacion_por_periodo[periodo] = desocupacion_por_periodo.get(periodo, 0) + int(pondera)

    # Retornar el período con menor desocupación o (0, 0) si no hay datos
    return min(desocupacion_por_periodo, key=desocupacion_por_periodo.get, default=(0, 0))



def ranking_aglomerados_hogares(datos_hogar, datos_indiv):
    """
    Devuelve los 5 aglomerados con mayor porcentaje de hogares donde al menos
    un ocupante tiene estudios universitarios o superiores. Se cuentan solo 
    hogares con 2 o más personas.
    """
    hogares_universitarios = {}
    for indiv in datos_indiv:
        cod_hogar = indiv.get("CODUSU")
        nro_hogar = indiv.get("NRO_HOGAR")
        nivel = indiv.get("NIVEL_ED")
        if nivel in ("5", "6"):
            hogares_universitarios[(cod_hogar, nro_hogar)] = True

    conteo = {}
    for hogar in datos_hogar:
        aglo = hogar.get("AGLOMERADO")
        cod_hogar = hogar.get("CODUSU")
        nro_hogar = hogar.get("NRO_HOGAR")
        ocupantes = int(hogar.get("IX_TOT", 0)or 0)
        pondera = int(hogar.get("PONDERA", 0)or 0)

        if ocupantes >= 2 and aglo != "":
            clave = (cod_hogar, nro_hogar)

            if aglo in conteo:
                conteo[aglo]["hogares"] += pondera
                if clave in hogares_universitarios:
                    conteo[aglo]["universitarios"] += pondera
            else:
                conteo[aglo] = {
                    "hogares": pondera,
                    "universitarios": pondera if clave in hogares_universitarios else 0
                }

    ranking = {}

    for aglo, datos in conteo.items():
        porcentaje = (datos["universitarios"] / datos["hogares"]) * 100
        ranking[aglo] = porcentaje 

    ranking_ordenado = dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:5])
    return ranking_ordenado



def porcentaje_viviendas_propietarios(datos_hogar):
    """
    Calcula el porcentaje de viviendas ocupadas por sus propietarios para cada aglomerado.
    """
    aglomerados = {}

    for hogar in datos_hogar:
        aglomerado = int(hogar.get("AGLOMERADO"))
        tenencia = hogar.get("IV1")
        pondera = int(hogar.get("PONDERA", 0))

        if pondera > 0:
            if aglomerado in aglomerados:
                aglomerados[aglomerado]["total"] += pondera
                if tenencia == "1":
                    aglomerados[aglomerado]["propietarios"] += pondera
            else:
                aglomerados[aglomerado] = {
                    "total": pondera,
                    "propietarios": pondera if tenencia == "1" else 0
                }

    porcentajes = {}
    for aglomerado, datos in aglomerados.items():
        total = datos["total"]
        propietarios = datos["propietarios"]
        porcentajes[aglomerado] = round((propietarios / total) * 100, 2)

    return porcentajes



def tabla_año_trimestre_aglomerado(datos_indiv,aglo1,aglo2):
    """ Calcula el Porcentaje de Personas Mayores Sin Secundario completo en 2 anglomerados introducidos e imprime una tabla.
    Args : datos_indiv (list): Lista de Diccionario con los datos de los individuos
            aglo1: (int) numero del aglomerado que se encuentra en el dataset
            aglo2: (int) numero del aglomerado que se encuentra en el dataset
    returns: imprime una tabla con los datos
    """


    def porcentaje_Aglomerado(datos_indiv,aglo1,aglo2):
        #Inicializo los contadores de cada alglomerado
        resultados = {
            aglo1: {"total": 0, "incompleto": 0},
            aglo2: {"total": 0, "incompleto": 0}
        }
        #Calculo los totales por aglomerado para el año y trimestre 
        for persona in datos_indiv:
            aglomerado = persona.get("AGLOMERADO")
            edad = persona.get("CH06")
            edad = int(edad)
            nivel_ed = persona.get("NIVEL_ED_str")
            if aglomerado in [aglo1,aglo2]:
                if edad >= 60:
                    resultados[aglomerado]["total"]+=1
                    if nivel_ed == "Secundario incompleto":
                        resultados[aglomerado]["incompleto"]+=1
        #Calcular porcentaje para cada alglomerado
        porcentajes = {}
        for aglo in [aglo1,aglo2]:
            total=resultados[aglo]["total"]
            incompleto=resultados[aglo]["incompleto"]
            if total == 0:
                porcentajes[aglo]=0.0
            else:
                porcentajes[aglo] = (incompleto / total)*100
        return porcentajes
    # obtengo los años y trimestres unicos del dataset
    años_trimestres = set((persona.get("ANO4"),persona.get("TRIMESTRE"))for persona in datos_indiv)

    #imprimo el encabezado de la tabla
    print(f"{'Año':<10} {'Trimestre':<12} {'Aglomerado 1':<20} {'Aglomerado 2':<20}")
    print ("-"*62)

    #calculo los resultados para cada año y trimestre 
    for año,trimestre in años_trimestres:
        #filtro los datos que necesito a ese año y trimestre
        datos_año_trimestre = [persona for persona in datos_indiv if persona.get("ANO4")== año and persona.get("TRIMESTRE")== trimestre]
        #llamo a la funcion para calcular el porcentaje de cada aglomerado en ese año y trimestre
        resultados= porcentaje_Aglomerado(datos_año_trimestre,aglo1,aglo2)

        #Imprimir Resultados
        print(f"{año:<10} {trimestre:<12} {resultados[aglo1]:<20.2f} {resultados[aglo2]:<20.2f}")



def porcentaje_material(datos_hogar,año_usuario):
    #genero diccionarios para contear
    conteo_total = {}
    conteo_precario = {}
    for hogar in datos_hogar:
        type(hogar)
        año = hogar.get("ANO4")
        trimestre = hogar.get("TRIMESTRE")
        aglomerado = hogar.get("AGLOMERADO")
        material = hogar.get("MATERIAL_TECHUMBRE")
        if año == año_usuario and trimestre == "4":
            conteo_total[aglomerado]= conteo_total.get(aglomerado,0)+1
            if material == "Material precario":
                conteo_precario[aglomerado] = conteo_precario.get(aglomerado,0)+1
    porcentajes = {}
    #calculo los porcentajes 
    for aglo in conteo_total:
        total=conteo_total[aglo]
        precarios=conteo_precario.get(aglo,0)
        porcentaje=(precarios/total)*100
        porcentajes[aglo] = porcentaje
        #si porcentajes tiene elementos utilizo lambda para obtener el max y min
    if porcentajes:
        aglo_mayor = max(porcentajes, key=porcentajes.get)
        aglo_menor = min(porcentajes, key=porcentajes.get)

        return [
        {
            'tipo': 'mayor',
            'aglomerado': aglo_mayor,
            'porcentaje': porcentajes[aglo_mayor]
        },
        {
            'tipo': 'menor',
            'aglomerado': aglo_menor,
            'porcentaje': porcentajes[aglo_menor]
        }
        ]
    else:
        return []
    



def calcular_porcentaje_jubilados_habitalidad(datos_hogar,datos_indiv):
    #Obtengo El año maximo y el trimestre maximo de ese año del dataset de individuos
    max_año = max(p['ANO4']for p in datos_indiv)
    max_trimestre = max(p['TRIMESTRE']for p in datos_indiv if p['ANO4']== max_año)
    #filtro por año y trimestre asi obtengo solo los que necesito
    personas_filtradas = [p for p in datos_indiv if p['ANO4']== max_año and p['TRIMESTRE']== max_trimestre]
    hogares_filtrados = [h for h in datos_hogar if h['ANO4']== max_año and h['TRIMESTRE']== max_trimestre]

    hogares_dic = {h['CODUSU']:h for h in hogares_filtrados}
    #diccionarios con clave Aglomerado que calculan total e insuficientes 
    jubilados_totales = {}
    jubilados_insuficiente = {}

    for persona in personas_filtradas:
        if persona ['CAT_INAC']== "1":
            # (prueba para ver si encontraba jubilados) print("Jubilado encontrado:", persona['CODUSU'])
            id_hogar = persona.get("CODUSU")
            hogar = hogares_dic.get(id_hogar)
            if hogar:
                aglomerado=persona.get("AGLOMERADO")
                jubilados_totales[aglomerado] = jubilados_totales.get(aglomerado, 0) + 1
                if hogar.get("CONDICION_DE_HABITABILIDAD") == "INSUFICIENTE":
                    jubilados_insuficiente[aglomerado] = jubilados_insuficiente.get(aglomerado, 0) + 1
    porcentajes = {}
    for aglomerado in jubilados_totales:
        total= jubilados_totales[aglomerado]
        insuf = jubilados_insuficiente.get(aglomerado,0)
        porcentaje = (insuf/total)*100
        porcentajes[aglomerado]=porcentaje
    return porcentajes




def cant_uni_habitalidad(datos_hogar,datos_indiv,año):
    #filtro personas y hogares con el año introducido por el usuario y el ultimo trimestre
    personas_filtradas = [p for p in datos_indiv if p['ANO4']== año and p ['TRIMESTRE']== "4"]
    hogares_filtrados = [h for h in datos_hogar if h['ANO4']== año and h['TRIMESTRE']== "4"]
    #genero un diccionario con el codusu con los hogares filtrados
    hogares_dic = {h['CODUSU']:h for h in hogares_filtrados}

    total=0
    for persona in personas_filtradas:
        if persona['NIVEL_ED_str']== "Superior o universitario":
            id_hogar = persona.get("CODUSU")
            hogar = hogares_dic.get(id_hogar)
            if hogar:
                condicion = hogar.get("CONDICION_DE_HABITABILIDAD")
                if condicion == "insuficiente":
                    total+=1
    return total