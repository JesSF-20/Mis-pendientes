import pygame
import sys
import re

# --- Leer archivo .lrc ---
def cargar_letras_linea(archivo_lrc):
    letras = []
    patron = re.compile(r"\[(\d+):(\d+\.\d+)\](.*)")
    with open(archivo_lrc, "r", encoding="utf-8") as f:
        for linea in f:
            match = patron.match(linea.strip())
            if match:
                minutos = int(match.group(1))
                segundos = float(match.group(2))
                texto = match.group(3).strip()
                tiempo_ms = int((minutos * 60 + segundos) * 1000)
                letras.append((tiempo_ms, texto))
    return letras

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Pantalla
screen_width, screen_height = 800, 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Karaoke WAV Windows")

# Colores y fuente
black, white, yellow = (0, 0, 0), (255, 255, 255), (255, 255, 0)
font_base_size = 64
font = pygame.font.Font(None, font_base_size)

# Cargar WAV y letras
sound = pygame.mixer.Sound("cancion.wav")  # WAV previamente convertido
letras = cargar_letras_linea("cancion.lrc")

# Función para dibujar la línea
def draw_karaoke_line(text, progress_ratio, x, y, max_width):
    font_size = font_base_size
    font_local = pygame.font.Font(None, font_size)
    text_width, _ = font_local.size(text)
    
    while text_width > max_width and font_size > 10:
        font_size -= 2
        font_local = pygame.font.Font(None, font_size)
        text_width, _ = font_local.size(text)
    
    # Texto completo en blanco
    text_surface = font_local.render(text, True, white)
    screen.blit(text_surface, (x - text_width // 2, y))
    
    # Parte resaltada en amarillo
    if progress_ratio > 0:
        highlight_width = int(text_width * progress_ratio)
        highlight_surface = font_local.render(text, True, yellow)
        screen.blit(highlight_surface, (x - text_width // 2, y), (0, 0, highlight_width, font_local.get_height()))

# --- Loop principal ---
current_index = 0
running = True
start_ticks = pygame.time.get_ticks()

sound.play()  # Reproducir WAV

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    
    elapsed = pygame.time.get_ticks() - start_ticks

    if current_index < len(letras) - 1 and elapsed >= letras[current_index + 1][0]:
        current_index += 1

    if current_index < len(letras):
        line_start_time = letras[current_index][0]
        if current_index < len(letras) - 1:
            line_end_time = letras[current_index + 1][0]
        else:
            line_end_time = line_start_time + 3000  # última línea aprox

        line_text = letras[current_index][1]
        progress_ratio = min(max((elapsed - line_start_time) / (line_end_time - line_start_time), 0), 1)
        draw_karaoke_line(line_text, progress_ratio, screen_width//2, screen_height//2, screen_width - 40)

    pygame.display.flip()

    if not pygame.mixer.get_busy():
        running = False

pygame.quit()
sys.exit()
