import pygame
import sys
import re
import os

# --- CONFIGURACIÓN DE ARCHIVOS Y CONSTANTES ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LRC_FILE = os.path.join(SCRIPT_DIR, "Beba.lrc")
MP3_FILE = os.path.join(SCRIPT_DIR, "Beba.mp3") 

# Pantalla y Colores
screen_width, screen_height = 800, 300 
black, white, yellow = (0, 0, 0), (255, 255, 255), (255, 255, 0)
font_base_size = 64
MAX_LINE_WIDTH = screen_width - 40 # 760px máximo de ancho para texto
# -----------------------------------------------

# --- Leer archivo .lrc (Soporte para Formato Simple y Avanzado) ---
def cargar_letras_avanzadas(archivo_lrc):
    # (Misma función anterior, omitida por brevedad, pero debe estar aquí)
    lyrics_data = []
    line_pattern = re.compile(r'\[(\d{1,2}):(\d{2}\.\d{2,3})\](.*)')
    word_pattern = re.compile(r'<(\d{1,2}):(\d{2}\.\d{2,3})>([^<]+)')
    modo_compatibilidad = False

    try:
        with open(archivo_lrc, "r", encoding="utf-8") as f:
            for line_str in f:
                line_match = line_pattern.match(line_str.strip())
                if line_match:
                    min_l, sec_l, remaining_text = line_match.groups()
                    line_start_s = int(min_l) * 60 + float(sec_l)
                    line_start_ms = int(line_start_s * 1000)
                    
                    words_in_line = []
                    for word_match in word_pattern.finditer(remaining_text):
                        min_w, sec_w, word_text = word_match.groups()
                        word_start_s = int(min_w) * 60 + float(sec_w)
                        word_start_ms = int(word_start_s * 1000)
                        words_in_line.append((word_start_ms, word_text.strip()))
                    
                    if not words_in_line and remaining_text.strip():
                        modo_compatibilidad = True
                        words_in_line.append((line_start_ms, remaining_text.strip()))

                    if words_in_line:
                        lyrics_data.append((line_start_ms, words_in_line))
                        
    except FileNotFoundError:
        return [], False
    
    if modo_compatibilidad:
        print("\n*** MODO COMPATIBILIDAD LRC ACTIVO ***: Letra se colorea por LÍNEA.\n")
    return lyrics_data, modo_compatibilidad

# --- NUEVA FUNCIÓN: Ajuste Dinámico de Fuente ---
def get_scaled_font(text, max_width, initial_size, font_name=None):
    """
    Reduce el tamaño de la fuente hasta que todo el texto quepa en el ancho máximo.
    Devuelve la fuente ajustada y su tamaño.
    """
    current_size = initial_size
    
    # Intentar usar System Font por robustez
    if font_name is None:
        try:
            temp_font = pygame.font.SysFont('Arial', current_size)
        except:
            temp_font = pygame.font.Font(None, current_size)
    else:
        temp_font = pygame.font.Font(font_name, current_size)
        
    text_width = temp_font.size(text)[0]

    # Reducir el tamaño si el texto es demasiado largo
    while text_width > max_width and current_size > 20:
        current_size -= 2
        if font_name is None:
            try:
                temp_font = pygame.font.SysFont('Arial', current_size)
            except:
                temp_font = pygame.font.Font(None, current_size)
        else:
            temp_font = pygame.font.Font(font_name, current_size)
            
        text_width = temp_font.size(text)[0]
    
    return temp_font, current_size
# -----------------------------------------------

# --- Funciones de Dibujo ---

def draw_word_line(screen, word_info_list, x_center, y, elapsed_ms, font, base_color, active_color, is_compatible_mode):
    """Dibuja una sola línea de palabras ya ajustada, centrada y coloreada."""
    
    line_width = sum(info[2] for info in word_info_list) 
    current_x = x_center - line_width // 2 # Posición X inicial para centrar la línea
    
    for time_ms, word, word_width in word_info_list:
        
        if is_compatible_mode:
            color = active_color 
        else:
            color = active_color if elapsed_ms >= time_ms else base_color
        
        # Ojo: Usamos la fuente que se nos pasa como argumento (ya escalada)
        word_surface_colored = font.render(word + " ", True, color) 
        screen.blit(word_surface_colored, (current_x, y))
        current_x += word_width


def draw_karaoke_words(screen, words_list, elapsed_ms, x_center, y, max_width, base_color, active_color, is_compatible_mode, current_font):
    """
    Dibuja la letra completa con ajuste de línea (Word Wrapping).
    current_font es la fuente ya escalada para la línea actual.
    """
    if not words_list:
        return

    current_line_width = 0
    words_on_current_display_line = []
    font_height = current_font.get_height()
    current_y = y

    for time_ms, word in words_list:
        # Usar la fuente escalada para medir
        word_surface_test = current_font.render(word + " ", True, base_color)
        word_width = word_surface_test.get_width()

        if current_line_width + word_width < max_width:
            words_on_current_display_line.append((time_ms, word, word_width))
            current_line_width += word_width
        else:
            draw_word_line(screen, words_on_current_display_line, x_center, current_y, elapsed_ms, current_font, base_color, active_color, is_compatible_mode)
            
            current_y += font_height + 5 
            words_on_current_display_line = [(time_ms, word, word_width)]
            current_line_width = word_width

    draw_word_line(screen, words_on_current_display_line, x_center, current_y, elapsed_ms, current_font, base_color, active_color, is_compatible_mode)


# --- Bloque Principal de Ejecución ---
def main():
    
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(f"Karaoke - {os.path.basename(MP3_FILE)}")
    
    # 2. Fuentes (Se reajustarán dinámicamente, esto es solo para el texto siguiente)
    font_next = pygame.font.Font(None, 40)
    
    letras_avanzadas, modo_compatibilidad = cargar_letras_avanzadas(LRC_FILE)

    try:
        pygame.mixer.music.load(MP3_FILE)
    except pygame.error as e:
        print(f"ERROR al cargar el MP3: {e}.")
        pygame.quit(); sys.exit()
    
    if not letras_avanzadas:
        print("El programa no pudo continuar sin LRC válido. Revise la ruta.")
        pygame.quit(); sys.exit()

    current_line_index = 0
    running = True
    pygame.mixer.music.play() 
    start_time_real = pygame.time.get_ticks() 
    clock = pygame.time.Clock()

    print("\n--- INICIANDO KARAOKE ---")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.fill(black)
        
        elapsed_ms = pygame.mixer.music.get_pos() 
        if elapsed_ms < 0: 
            elapsed_ms = pygame.time.get_ticks() - start_time_real

        # --- Lógica de avance de línea ---
        if current_line_index < len(letras_avanzadas):
            next_line_start_time = float('inf') 
            if current_line_index < len(letras_avanzadas) - 1:
                next_line_start_time = letras_avanzadas[current_line_index + 1][0]
            
            if elapsed_ms >= next_line_start_time:
                current_line_index += 1

        # --- Dibujar la línea actual ---
        if current_line_index < len(letras_avanzadas):
            current_line_words_data = letras_avanzadas[current_line_index][1]
            
            # 1. Obtener el texto completo para el ajuste
            full_line_text = " ".join([word for time, word in current_line_words_data])
            
            # 2. ESCALADO DINÁMICO de fuente para que quepa en una sola línea (antes del wrapping)
            scaled_font, final_size = get_scaled_font(full_line_text, MAX_LINE_WIDTH, font_base_size)
            
            # 3. Posicionamiento Y centrado basado en la fuente escalada
            center_y = screen_height // 2 - scaled_font.get_height() // 2 
            
            # 4. Colorear y dibujar
            active_color_for_line = yellow
            if elapsed_ms < letras_avanzadas[current_line_index][0]:
                 active_color_for_line = white # No pintar si la línea no ha iniciado
            
            draw_karaoke_words(screen, current_line_words_data, elapsed_ms, 
                               screen_width // 2, center_y, 
                               MAX_LINE_WIDTH, white, active_color_for_line, modo_compatibilidad, scaled_font)
            
        # --- Dibujar la línea siguiente ---
        if current_line_index + 1 < len(letras_avanzadas):
            next_line_words_data = letras_avanzadas[current_line_index + 1][1]
            next_text = " ".join([word for time, word in next_line_words_data])
            
            next_line_y = screen_height - 30 # Posición fija abajo
            
            text_surface = font_next.render(next_text, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(screen_width//2, next_line_y))
            screen.blit(text_surface, text_rect)


        pygame.display.flip()

        if not pygame.mixer.music.get_busy() and current_line_index >= len(letras_avanzadas) - 1:
            running = False
            
        clock.tick(60) 

    # 5. Limpieza final:
    if pygame.mixer.get_busy():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()