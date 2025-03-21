# Haz un programa que pida al usuario que ingrese una temperatura en grados Celsius 
# y luego convierta esa temperatura a grados Fahrenheit, mostrando el resultado.
def cambio_de_celsius_a_fahrenheit():
    celsius = float(input("Ingrese una temperatura en grados Celsius: "))
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C equivale a {fahrenheit:.2f}°F")
    return

cambio_de_celsius_a_fahrenheit()
