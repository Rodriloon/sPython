# Escribe un programa que tome una lista de números enteros como entrada
# del usuario. Luego, convierte cada número en la lista a string y únelos en
# una sola cadena, separados por guiones ('-'). Sin embargo, excluye cualquier
# número que sea múltiplo de 3 de la cadena final.
def procesar_numeros(lista):
    lista_filtrada = [str(num) for num in lista if num % 3 != 0]
    return "-".join(lista_filtrada)

entrada = input("Ingresa una lista de números enteros separados por espacio: ")
numeros = list(map(int, entrada.split()))

resultado = procesar_numeros(numeros)
print("Cadena resultante:", resultado)