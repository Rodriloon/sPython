# Implementa un programa que solicite al usuario que ingrese una lista de
# números. Luego, imprime la lista pero detén la impresión si encuentras un
# número negativo. Nota: utilice la sentencia break cuando haga falta.
def imprimir_hasta_negativo(lista):
    for numero in lista:
        if numero < 0:
            print("Número negativo encontrado. Deteniendo la impresión.")
            break
        print(numero)

entrada = input("Ingresa una lista de números separados por espacio: ")
numeros = list(map(int, entrada.split()))

print("Números ingresados (hasta el primer negativo):")
imprimir_hasta_negativo(numeros)