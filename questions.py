import sys
import random

# Preguntas para el juego
questions = [
    "¿Qué función se usa para obtener la longitud de una cadena en Python?",
    "¿Cuál de las siguientes opciones es un número entero en Python?",
    "¿Cómo se solicita entrada del usuario en Python?",
    "¿Cuál de las siguientes expresiones es un comentario válido en Python?",
    "¿Cuál es el operador de comparación para verificar si dos valores son iguales?",
]

# Respuestas posibles para cada pregunta, en el mismo orden que las preguntas
answers = [
    ("size()", "len()", "length()", "count()"),
    ("3.14", "'42'", "10", "True"),
    ("input()", "scan()", "read()", "ask()"),
    (
    "// Esto es un comentario", 
    "/* Esto es un comentario */",
    "-- Esto es un comentario",
    "# Esto es un comentario",
    ),
    ("=", "==", "!=", "==="),
]

# Índice de la respuesta correcta para cada pregunta, en el mismo orden que las preguntas
correct_answers_index = [1, 2, 0, 3, 1]

# Combinar las tres listas usando zip
questions_to_ask = random.choices(list(zip(questions, answers, correct_answers_index)), k=3)

puntaje = float(0)

# El usuario deberá contestar 3 preguntas
for question, answer_choices, correct_answer_index in questions_to_ask:
    # Se muestra la pregunta y las respuestas posibles
    print(question)
    for i, answer in enumerate(answer_choices):
        print(f"{i + 1}. {answer}")
    
    # El usuario tiene 2 intentos para responder correctamente
    for intento in range(2):
        user_answer = input("Respuesta: ")
        
        # Validamos que la respuesta ingresada sea un número
        if not user_answer.isdigit():
            print('Respuesta no valida')
            sys.exit(1)  
        
        user_answer = int(user_answer)
        
        # Verificamos que la respuesta esté dentro del rango
        if not (1 <= user_answer <= 4):
            print('Respuesta no válida')
            sys.exit(1)  
        
        # Restamos 1 para que la respuesta esté en el rango de índices
        user_answer -= 1

        # Se verifica si la respuesta es correcta
        if user_answer == correct_answer_index:
            print("¡Correcto!")
            puntaje += 1
            break
        elif puntaje != 0:
                puntaje -= 0.5
    else:
        # Si el usuario no responde correctamente después de 2 intentos,
        # se muestra la respuesta correcta
        print("La respuesta correcta es:")
        print(answer_choices[correct_answer_index])

    # Se imprime un blanco al final de la pregunta  
    print()

print(f"Tu puntaje final fue de: {puntaje}")
