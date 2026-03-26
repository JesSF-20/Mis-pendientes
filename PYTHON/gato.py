import random

def dibujar_tablero(tablero):
    """Imprime el tablero del Tres en Raya."""
    print(' ' + tablero[1] + ' | ' + tablero[2] + ' | ' + tablero[3])
    print('---+---+---')
    print(' ' + tablero[4] + ' | ' + tablero[5] + ' | ' + tablero[6])
    print('---+---+---')
    print(' ' + tablero[7] + ' | ' + tablero[8] + ' | ' + tablero[9])

def obtener_letra_jugador():
    """Permite al jugador elegir su letra ('X' o 'O')."""
    letra = ''
    while not (letra == 'X' or letra == 'O'):
        print('¿Quieres ser X o O?')
        letra = input().upper()

    if letra == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def quien_empieza():
    """Decide aleatoriamente quién hace el primer movimiento."""
    if random.randint(0, 1) == 0:
        return 'IA'
    else:
        return 'jugador'

def es_ganador(tablero, letra):
    """Devuelve True si la letra dada ha ganado."""
    # Se revisan las 8 posibles combinaciones ganadoras
    return ((tablero[7] == letra and tablero[8] == letra and tablero[9] == letra) or # fila superior
            (tablero[4] == letra and tablero[5] == letra and tablero[6] == letra) or # fila media
            (tablero[1] == letra and tablero[2] == letra and tablero[3] == letra) or # fila inferior
            (tablero[7] == letra and tablero[4] == letra and tablero[1] == letra) or # columna izquierda
            (tablero[8] == letra and tablero[5] == letra and tablero[2] == letra) or # columna media
            (tablero[9] == letra and tablero[6] == letra and tablero[3] == letra) or # columna derecha
            (tablero[7] == letra and tablero[5] == letra and tablero[3] == letra) or # diagonal \
            (tablero[9] == letra and tablero[5] == letra and tablero[1] == letra))    # diagonal /

def obtener_copia_tablero(tablero):
    """Crea una copia del tablero para que la IA pueda simular movimientos."""
    copia_tablero = []
    for i in tablero:
        copia_tablero.append(i)
    return copia_tablero

def es_espacio_libre(tablero, movimiento):
    """Devuelve True si el movimiento está disponible."""
    return tablero[movimiento] == ' '

def obtener_movimiento_jugador(tablero):
    """Permite al jugador ingresar su movimiento."""
    movimiento = ' '
    while movimiento not in '1 2 3 4 5 6 7 8 9'.split() or not es_espacio_libre(tablero, int(movimiento)):
        print('¿Cuál es tu próximo movimiento? (1-9)')
        movimiento = input()
    return int(movimiento)

# --------------------------------------------------------------------------
# LÓGICA DE LA INTELIGENCIA ARTIFICIAL (IA)
# --------------------------------------------------------------------------

def verificar_movimiento_ganador(tablero, letra, movimiento):
    """Chequea si la letra dada puede ganar con el movimiento propuesto."""
    copia = obtener_copia_tablero(tablero)
    copia[movimiento] = letra
    return es_ganador(copia, letra)

def obtener_movimiento_ia(tablero, letra_ia, letra_jugador):
    """
    La IA sigue una estrategia simple pero infalible:
    1. Ganar si es posible.
    2. Bloquear al jugador si va a ganar.
    3. Tomar el centro.
    4. Tomar esquinas.
    5. Tomar lados.
    """
    
    # 1. Chequear si podemos ganar en el siguiente movimiento
    for i in range(1, 10):
        if es_espacio_libre(tablero, i) and verificar_movimiento_ganador(tablero, letra_ia, i):
            return i

    # 2. Chequear si el jugador puede ganar en el siguiente movimiento y bloquearlo
    for i in range(1, 10):
        if es_espacio_libre(tablero, i) and verificar_movimiento_ganador(tablero, letra_jugador, i):
            return i

    # 3. Tomar el centro (es la mejor posición)
    if es_espacio_libre(tablero, 5):
        return 5

    # 4. Tomar una esquina si está libre
    esquinas = [1, 3, 7, 9]
    movimientos_disponibles = [i for i in esquinas if es_espacio_libre(tablero, i)]
    if movimientos_disponibles:
        return random.choice(movimientos_disponibles)

    # 5. Tomar un lado si está libre
    lados = [2, 4, 6, 8]
    movimientos_disponibles = [i for i in lados if es_espacio_libre(tablero, i)]
    if movimientos_disponibles:
        return random.choice(movimientos_disponibles)
    
    # Esto no debería ocurrir si el tablero no está lleno
    return None 

def es_tablero_lleno(tablero):
    """Devuelve True si todos los espacios han sido ocupados."""
    for i in range(1, 10):
        if es_espacio_libre(tablero, i):
            return False
    return True

# --------------------------------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO
# --------------------------------------------------------------------------

print('¡Bienvenido al Tres en Raya con IA Imbatible!')

while True:
    # 1. Inicialización
    el_tablero = [' '] * 10
    letra_jugador, letra_ia = obtener_letra_jugador()
    turno = quien_empieza()
    print('La ' + turno + ' irá primero.')
    
    juego_terminado = False

    while not juego_terminado:
        if turno == 'jugador':
            # Turno del jugador
            dibujar_tablero(el_tablero)
            movimiento = obtener_movimiento_jugador(el_tablero)
            el_tablero[movimiento] = letra_jugador

            if es_ganador(el_tablero, letra_jugador):
                dibujar_tablero(el_tablero)
                print('¡Felicidades! ¡Has ganado!')
                juego_terminado = True
            elif es_tablero_lleno(el_tablero):
                dibujar_tablero(el_tablero)
                print('¡El juego es un empate!')
                juego_terminado = True
            else:
                turno = 'IA'

        else:
            # Turno de la IA
            movimiento = obtener_movimiento_ia(el_tablero, letra_ia, letra_jugador)
            el_tablero[movimiento] = letra_ia

            if es_ganador(el_tablero, letra_ia):
                dibujar_tablero(el_tablero)
                print('¡La IA te ha ganado! ¡Has perdido!')
                juego_terminado = True
            elif es_tablero_lleno(el_tablero):
                dibujar_tablero(el_tablero)
                print('¡El juego es un empate!')
                juego_terminado = True
            else:
                turno = 'jugador'

    print('¿Quieres volver a jugar? (sí o no)')
    if not input().lower().startswith('s'):
        break