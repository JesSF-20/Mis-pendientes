# Analizador de Texto

# Pedimos el nombre del archivo al usuario
archivo_nombre = r"C:\Users\José de Jesús\Documents\EjerciciosPython\PYTHON\prueba.txt"

with open(archivo_nombre, "r", encoding="utf-8") as archivo:
    contenido = archivo.read()


try:
    with open(archivo_nombre, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print("El archivo no existe.")
    contenido = ""

    palabras = contenido.split()  # separa por espacios
num_palabras = len(palabras)
print("Número de palabras:", num_palabras)

conteo_letras = {}
for letra in contenido:
    if letra.isalpha():  # solo letras
        letra = letra.lower()
        if letra in conteo_letras:
            conteo_letras[letra] += 1
        else:
            conteo_letras[letra] = 1

# Mostrar las 5 letras más frecuentes
top_letras = sorted(conteo_letras.items(), key=lambda x: x[1], reverse=True)[:5]
print("Letras más frecuentes:", top_letras)

num_oraciones = contenido.count(".") + contenido.count("?") + contenido.count("!")
print("Número de oraciones:", num_oraciones)

articulos = {"el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "de", "del"}
palabras_filtradas = [p.lower().strip(".,!?") for p in palabras if p.lower() not in articulos]

conteo_palabras = {}
for palabra in palabras_filtradas:
    if palabra in conteo_palabras:
        conteo_palabras[palabra] += 1
    else:
        conteo_palabras[palabra] = 1

top5_palabras = sorted(conteo_palabras.items(), key=lambda x: x[1], reverse=True)[:5]
print("5 palabras más usadas:", top5_palabras)

