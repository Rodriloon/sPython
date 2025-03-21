# Cree un programa que dada una lista de números imprima sólo los que son
# pares. Nota: utilice la sentencia continue donde haga falta.
def imprimir_lista_pares(lista):
    for numero in lista:
        if numero % 2 != 0: 
            continue  
        print(numero)

numeros = [10, 15, 22, 33, 40, 55, 66, 77, 88, 99, 100]
print("Números pares en la lista:")
imprimir_lista_pares(numeros)