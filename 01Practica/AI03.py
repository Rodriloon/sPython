# Crea un programa que calcule la suma de los primeros 100 números
# naturales utilizando un bucle for.
def suma_100_naturales():
    suma = 0
    for i in range(1, 101):  # Itera del 1 al 100
        suma += i
    print(f"La suma de los primeros 100 números naturales es: {suma}")

suma_100_naturales()