# Modifique el ejercicio 4 para que dada la lista de número genere dos nuevas
# listas, una con los número pares y otras con los que son impares. Imprima
# las listas al terminar de procesarlas
def separar_pares_impares(lista):
    pares = []
    impares = []
    
    for numero in lista:
        if numero % 2 == 0:
            pares.append(numero)
        else:
            impares.append(numero)
    
    return pares, impares

numeros = [10, 15, 22, 33, 40, 55, 66, 77, 88, 99, 100]

pares, impares = separar_pares_impares(numeros)

print("Lista de números pares:", pares)
print("Lista de números impares:", impares)