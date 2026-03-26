import time

# Mensaje inicial
print("🎉 ¡Feliz Día, Mamá! 🎉")
time.sleep(1)
print("Hoy quiero regalarte algo especial...")
time.sleep(1.5)

# Dibujo de corazón con caracteres
print("""
   ******       ******
  ********     ********
 **********   **********
 *********** ***********
 ***********************
  *********************
   *******************
     ***************
       ***********
         *******
           ***
            *
""")
time.sleep(2)

# Mensaje personalizado
print("\nMamá, eres la persona más increíble del mundo 💖")
time.sleep(2)
print("Gracias por tu amor, paciencia y por siempre apoyarme.")
time.sleep(2)

# Pequeño juego interactivo
print("\nVamos a hacer un juego rápido. Responde las preguntas sobre mamá.")
score = 0

q1 = input("¿Cuál es el color favorito de mamá? ").lower()
if q1 == "rosa":
    print("¡Correcto! 🎀")
    score += 1
else:
    print("¡Casi! El color favorito es rosa.")

q2 = input("¿A mamá le gusta más el chocolate o la vainilla? ").lower()
if q2 == "chocolate":
    print("¡Correcto! 🍫")
    score += 1
else:
    print("¡Casi! Le encanta el chocolate.")

# Resultado del juego
print(f"\nTu puntuación: {score}/2")
if score == 2:
    print("¡Eres un experto sobre mamá! 💖")
else:
    print("No te preocupes, lo importante es que la amas 💕")

# Mensaje final
print("\nTe quiero mucho, mamá. ¡Feliz Día! 🌹")
