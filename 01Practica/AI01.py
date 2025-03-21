# Desarrolla un programa que solicite al usuario que ingrese su edad y luego
# calcule y muestre cuántos años le faltan para alcanzar los 100 años.
def calcular_anios_para_100():
    edad = int(input("Ingresa tu edad actual: "))
    if edad <= 0:
        print("La edad ingresada debe ser un número positivo.")
        return   
    anios_para_100 = 100 - edad
    if anios_para_100 > 0:
        print(f"Te faltan {anios_para_100} años para alcanzar los 100 años.")
    else:
        print("¡Ya tienes 100 años o más!")

calcular_anios_para_100()