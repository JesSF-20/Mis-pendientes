# Juego del ahorcado
import random

palabras = ["python", "programa", "computadora", "juego", "ahorcado"]
palabra = random.choice(palabras)

palabra_oculta = ["_"] * len(palabra) # Devuelve el número de letras de la palabra seleccionada.
intentos = 6  # máximo de errores permitidos
letras_adivinadas = []  # para no repetir letras

while True: # Esto crea un bucle infinito, que seguirá ejecutándose hasta que se encuentre un break.
    print(" ".join(palabra_oculta)) # Muestra la palabra al usuario, pero con _ en las letras que aún no adivinó.
    print("Intentos restantes:", intentos)
    letra = input("Adivina una letra: ").lower()

    if letra in letras_adivinadas:
        print("Ya intentaste esa letra. Intenta otra.")
        continue

    letras_adivinadas.append(letra)

    if letra in palabra: 
        for i in range(len(palabra)):
            if palabra[i] == letra:
                palabra_oculta[i] = letra
    # Si la letra está en la palabra, se entra en un bucle for que recorre la palabra 
    # y reemplaza los _ correspondientes.
    else:
        intentos -= 1
        print("Letra incorrecta.")

    # Verificar si ganó
    if "_" not in palabra_oculta:
        print("¡Ganaste! La palabra era:", palabra)
        break

    # Verificar si perdió
    if intentos == 0:
        print("¡Perdiste! La palabra era:", palabra)
        break
