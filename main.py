import pygame
import sys
import json
import os

pygame.init()

# --- CONFIGURACIÓN DE VENTANA ---
ANCHO, ALTO = 1200, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Editor de Mapas 2D - Configurable")

# --- COLORES ---
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
GRIS_OSCURO = (130, 130, 130)
NEGRO = (0, 0, 0)
AZUL_BARRA = (50, 90, 160)
AZUL = (100, 150, 255)
VERDE = (100, 200, 100)
ROJO = (220, 100, 100)
NARANJA = (255, 180, 50)
MORADO = (170, 130, 255)
AMARILLO = (255, 240, 120)

# --- ÁREAS DE INTERFAZ ---
BARRA_SUP = 40
FOOTER_ALTURA = 30
PANEL_IZQ = 200
PANEL_DER = 200

# --- PARÁMETROS BASE ---
TILE = 40
zoom = 1.0
offset_x, offset_y = 0, 0
moviendo = False
pos_mouse_anterior = (0, 0)
mensaje_estado = "Listo."

# --- FUENTE ---
fuente = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()


# ============================================================
#                  MENÚ INICIAL DE CONFIGURACIÓN
# ============================================================

def menu_configuracion():
    """Pantalla para configurar tamaño del mapa"""
    ancho_input = ""
    alto_input = ""
    activo_ancho = False
    activo_alto = False

    while True:
        pantalla.fill((240, 240, 240))
        titulo = fuente.render("🧱 Configura el tamaño del mapa (en tiles)", True, NEGRO)
        pantalla.blit(titulo, (320, 150))

        # Campos de texto
        rect_ancho = pygame.Rect(480, 250, 150, 40)
        rect_alto = pygame.Rect(480, 310, 150, 40)

        pygame.draw.rect(pantalla, BLANCO, rect_ancho)
        pygame.draw.rect(pantalla, NEGRO, rect_ancho, 2)
        pygame.draw.rect(pantalla, BLANCO, rect_alto)
        pygame.draw.rect(pantalla, NEGRO, rect_alto, 2)

        pantalla.blit(fuente.render("Ancho:", True, NEGRO), (400, 260))
        pantalla.blit(fuente.render(ancho_input, True, NEGRO), (490, 260))
        pantalla.blit(fuente.render("Alto:", True, NEGRO), (400, 320))
        pantalla.blit(fuente.render(alto_input, True, NEGRO), (490, 320))

        boton_iniciar = pygame.Rect(480, 380, 150, 45)
        pygame.draw.rect(pantalla, VERDE, boton_iniciar)
        pygame.draw.rect(pantalla, NEGRO, boton_iniciar, 2)
        pantalla.blit(fuente.render("Iniciar", True, NEGRO), (525, 390))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_ancho.collidepoint(evento.pos):
                    activo_ancho, activo_alto = True, False
                elif rect_alto.collidepoint(evento.pos):
                    activo_ancho, activo_alto = False, True
                elif boton_iniciar.collidepoint(evento.pos):
                    if ancho_input.isdigit() and alto_input.isdigit():
                        return int(ancho_input), int(alto_input)

            if evento.type == pygame.KEYDOWN:
                if activo_ancho:
                    if evento.key == pygame.K_BACKSPACE:
                        ancho_input = ancho_input[:-1]
                    elif evento.unicode.isdigit():
                        ancho_input += evento.unicode
                elif activo_alto:
                    if evento.key == pygame.K_BACKSPACE:
                        alto_input = alto_input[:-1]
                    elif evento.unicode.isdigit():
                        alto_input += evento.unicode

        pygame.display.flip()
        clock.tick(30)


# ============================================================
#                  EDITOR PRINCIPAL
# ============================================================

def editor_mapa(columnas, filas):
    global zoom, offset_x, offset_y, mensaje_estado

    MAPA_ANCHO = ANCHO - PANEL_IZQ - PANEL_DER
    MAPA_ALTO = ALTO - BARRA_SUP - FOOTER_ALTURA

    # --- CREAR MAPA VACÍO ---
    mapas = {
        "fondo": [[0 for _ in range(columnas)] for _ in range(filas)],
        "objetos": [[0 for _ in range(columnas)] for _ in range(filas)]
    }
    capa_actual = "fondo"

    # --- CARGAR TILES ---
    if not os.path.exists("assets"):
        os.makedirs("assets")

    TILES = {}
    id_tile = 1
    for archivo in os.listdir("assets"):
        if archivo.endswith(".png"):
            img = pygame.image.load(os.path.join("assets", archivo))
            img = pygame.transform.scale(img, (TILE, TILE))
            TILES[id_tile] = img
            id_tile += 1

    tile_actual = 1

    # --- FUNCIONES ---
    def dibujar_texto(texto, x, y, color=NEGRO):
        pantalla.blit(fuente.render(texto, True, color), (x, y))

    def dibujar_boton(texto, x, y, ancho, alto, color):
        rect = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, NEGRO, rect, 2)
        pantalla.blit(fuente.render(texto, True, NEGRO), (x + 10, y + 8))
        return rect

    def guardar_mapa():
        os.makedirs("maps", exist_ok=True)
        with open("maps/mapa_guardado.json", "w") as archivo:
            json.dump(mapas, archivo)
        return "✅ Mapa guardado correctamente."

    def cargar_mapa():
        nonlocal mapas
        try:
            with open("maps/mapa_guardado.json", "r") as archivo:
                mapas = json.load(archivo)
            return "📂 Mapa cargado correctamente."
        except FileNotFoundError:
            return "⚠️ No se encontró mapa guardado."

    def limpiar_mapa():
        for capa in mapas:
            for f in range(filas):
                for c in range(columnas):
                    mapas[capa][f][c] = 0
        return "🧹 Mapa limpiado."

    def exportar_mapa_png():
        os.makedirs("export", exist_ok=True)
        superficie = pygame.Surface((columnas * TILE, filas * TILE))
        superficie.fill(BLANCO)
        for capa in ["fondo", "objetos"]:
            for f in range(filas):
                for c in range(columnas):
                    tipo = mapas[capa][f][c]
                    if tipo in TILES:
                        superficie.blit(TILES[tipo], (c * TILE, f * TILE))
        pygame.image.save(superficie, "export/mapa_preview.png")
        return "🖼️ Exportado como imagen PNG."

    # --- LOOP PRINCIPAL ---
    moviendo = False
    while True:
        mensaje_estado = "Listo."
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- ZOOM ---
            if evento.type == pygame.MOUSEWHEEL:
                zoom += evento.y * 0.1
                zoom = max(0.5, min(2.0, zoom))

            # --- MOVER MAPA ---
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 2:
                    moviendo = True
                    pos_mouse_anterior = pygame.mouse.get_pos()
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 2:
                moviendo = False
            if evento.type == pygame.MOUSEMOTION and moviendo:
                x, y = pygame.mouse.get_pos()
                dx, dy = x - pos_mouse_anterior[0], y - pos_mouse_anterior[1]
                offset_x += dx
                offset_y += dy
                pos_mouse_anterior = (x, y)

            # --- PINTAR / BORRAR ---
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Dentro del área del mapa
                if PANEL_IZQ < x < ANCHO - PANEL_DER and BARRA_SUP < y < ALTO - FOOTER_ALTURA:
                    grid_x = int((x - PANEL_IZQ - offset_x) // (TILE * zoom))
                    grid_y = int((y - BARRA_SUP - offset_y) // (TILE * zoom))
                    if 0 <= grid_x < columnas and 0 <= grid_y < filas:
                        if evento.button == 1:
                            mapas[capa_actual][grid_y][grid_x] = tile_actual
                        elif evento.button == 3:
                            mapas[capa_actual][grid_y][grid_x] = 0

                # Paleta de tiles
                for i, img in TILES.items():
                    rect = pygame.Rect(70, 80 + (i - 1) * 50, 60, 40)
                    if rect.collidepoint(x, y):
                        tile_actual = i

                # Panel derecho botones
                boton_guardar = pygame.Rect(ANCHO - PANEL_DER + 25, 130, 150, 30)
                boton_cargar = pygame.Rect(ANCHO - PANEL_DER + 25, 170, 150, 30)
                boton_limpiar = pygame.Rect(ANCHO - PANEL_DER + 25, 210, 150, 30)
                boton_exportar = pygame.Rect(ANCHO - PANEL_DER + 25, 250, 150, 30)
                boton_capa = pygame.Rect(ANCHO - PANEL_DER + 25, 290, 150, 30)

                if boton_guardar.collidepoint(x, y):
                    mensaje_estado = guardar_mapa()
                elif boton_cargar.collidepoint(x, y):
                    mensaje_estado = cargar_mapa()
                elif boton_limpiar.collidepoint(x, y):
                    mensaje_estado = limpiar_mapa()
                elif boton_exportar.collidepoint(x, y):
                    mensaje_estado = exportar_mapa_png()
                elif boton_capa.collidepoint(x, y):
                    capa_actual = "objetos" if capa_actual == "fondo" else "fondo"
                    mensaje_estado = f"🪶 Capa actual: {capa_actual}"

        # --- DIBUJAR ---
        pantalla.fill(BLANCO)

        # Barra superior
        pygame.draw.rect(pantalla, AZUL_BARRA, (0, 0, ANCHO, BARRA_SUP))
        pantalla.blit(fuente.render("Archivo  |  Vista  |  Ayuda", True, BLANCO), (20, 10))

        # Área del mapa
        mapa_x, mapa_y = PANEL_IZQ, BARRA_SUP
        pygame.draw.rect(pantalla, (245, 245, 245), (mapa_x, mapa_y, ANCHO - PANEL_IZQ - PANEL_DER, ALTO - BARRA_SUP - FOOTER_ALTURA))
        for capa in ["fondo", "objetos"]:
            for f in range(filas):
                for c in range(columnas):
                    tipo = mapas[capa][f][c]
                    if tipo in TILES:
                        img = pygame.transform.scale(TILES[tipo], (int(TILE * zoom), int(TILE * zoom)))
                        pantalla.blit(img, (mapa_x + c*TILE*zoom + offset_x, mapa_y + f*TILE*zoom + offset_y))

        # Cuadrícula
        for x in range(columnas + 1):
            pygame.draw.line(pantalla, GRIS, (mapa_x + x*TILE*zoom + offset_x, mapa_y + offset_y),
                             (mapa_x + x*TILE*zoom + offset_x, mapa_y + filas*TILE*zoom + offset_y))
        for y in range(filas + 1):
            pygame.draw.line(pantalla, GRIS, (mapa_x + offset_x, mapa_y + y*TILE*zoom + offset_y),
                             (mapa_x + columnas*TILE*zoom + offset_x, mapa_y + y*TILE*zoom + offset_y))

        # Panel izquierdo (paleta)
        pygame.draw.rect(pantalla, (230, 230, 230), (0, BARRA_SUP, PANEL_IZQ, ALTO - FOOTER_ALTURA))
        pantalla.blit(fuente.render("🎨 Paleta", True, NEGRO), (60, 50))
        y = 80
        for i, img in TILES.items():
            mini = pygame.transform.scale(img, (60, 40))
            rect = pygame.Rect(70, y, 60, 40)
            pantalla.blit(mini, (70, y))
            if i == tile_actual:
                pygame.draw.rect(pantalla, ROJO, rect, 3)
            y += 50

        # Panel derecho
        pygame.draw.rect(pantalla, (240, 240, 240), (ANCHO - PANEL_DER, BARRA_SUP, PANEL_DER, ALTO - FOOTER_ALTURA))
        pantalla.blit(fuente.render("🧱 Capas", True, NEGRO), (ANCHO - PANEL_DER + 60, 50))
        pantalla.blit(fuente.render(f"Actual: {capa_actual}", True, NEGRO), (ANCHO - PANEL_DER + 20, 80))

        boton_guardar = dibujar_boton("Guardar", ANCHO - PANEL_DER + 25, 130, 150, 30, VERDE)
        boton_cargar = dibujar_boton("Cargar", ANCHO - PANEL_DER + 25, 170, 150, 30, AZUL)
        boton_limpiar = dibujar_boton("Limpiar", ANCHO - PANEL_DER + 25, 210, 150, 30, ROJO)
        boton_exportar = dibujar_boton("Exportar PNG", ANCHO - PANEL_DER + 25, 250, 150, 30, MORADO)
        boton_capa = dibujar_boton(f"Capa: {capa_actual}", ANCHO - PANEL_DER + 25, 290, 150, 30, AMARILLO)

        # Footer
        pygame.draw.rect(pantalla, GRIS_OSCURO, (0, ALTO - FOOTER_ALTURA, ANCHO, FOOTER_ALTURA))
        pantalla.blit(fuente.render(mensaje_estado, True, BLANCO), (10, ALTO - 25))

        pygame.display.flip()
        clock.tick(60)


# ============================================================
#                  EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":
    columnas, filas = menu_configuracion()
    editor_mapa(columnas, filas)
