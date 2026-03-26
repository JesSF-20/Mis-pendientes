# Generador de Contraseñas

import random
import string

longitud = int(input("Ingresa la longitud que tendrá la contraseña: "))
caracteres = string.ascii_letters + string.digits + string.punctuation
#Se crea la variable caracteres donde con el operador "+" se concatenan 
#Las tres cadenas (letras, números, símbolos) en una sola.

password = ""
for i in range(longitud):
  password += random.choice(caracteres)
# Se crea un bucle donde según la longitud del usuario, dará una vuelta y se 
# Elige un carácter al azar para generar la contraseña y guardarla en la variable.

print("Tu contraseña es:", password)

