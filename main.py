import pygame
import sys
import json
import os
import time

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
CYAN = (100, 200, 255)
ROSA = (255, 150, 200)
VERDE_OSCURO = (60, 160, 60)
AZUL_OSCURO = (70, 130, 200)
AZUL_CIELO = (135, 206, 235)
VERDE_BOSQUE = (34, 139, 34)
DORADO = (255, 215, 0)

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

# --- FUENTES ---
fuente = pygame.font.SysFont("Arial", 20)
fuente_grande = pygame.font.SysFont("Arial", 28)
fuente_titulo = pygame.font.SysFont("Arial", 36, bold=True)
clock = pygame.time.Clock()


# ============================================================
#                  MENÚ INICIAL DE CONFIGURACIÓN MEJORADO
# ============================================================

def menu_configuracion():
    """Pantalla para configurar tamaño del mapa - MEJORADA"""
    ancho_input = ""
    alto_input = ""
    activo_ancho = False
    activo_alto = False
    
    # Cargar imagen de fondo si existe
    fondo = None
    if os.path.exists("assets"):
        for archivo in os.listdir("assets"):
            if archivo.endswith(".png") and "pasto" in archivo.lower():
                try:
                    fondo = pygame.image.load(os.path.join("assets", archivo))
                    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
                    break
                except:
                    pass

    while True:
        # Fondo con gradiente o imagen
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            # Gradiente azul-verde
            for y in range(ALTO):
                color = (
                    max(0, 100 - y//10),
                    min(255, 150 + y//8),
                    min(255, 200 + y//12)
                )
                pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))
        
        # Panel central semi-transparente
        panel_central = pygame.Rect(200, 100, 800, 500)
        s = pygame.Surface((800, 500), pygame.SRCALPHA)
        s.fill((255, 255, 255, 220))  # Blanco semi-transparente
        pantalla.blit(s, (200, 100))
        pygame.draw.rect(pantalla, DORADO, panel_central, 4, border_radius=15)
        
        # Título con efecto
        titulo = fuente_titulo.render("🎮 EDITOR DE MAPAS 2D 🎮", True, AZUL_OSCURO)
        subtitulo = fuente_grande.render("Configura el tamaño de tu mapa (en tiles)", True, GRIS_OSCURO)
        
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 200))
        
        # Iconos decorativos
        pygame.draw.rect(pantalla, VERDE_BOSQUE, (300, 250, 40, 40), border_radius=8)
        pygame.draw.rect(pantalla, AZUL, (860, 250, 40, 40), border_radius=8)
        pantalla.blit(fuente_grande.render("🗺️", True, NEGRO), (308, 252))
        pantalla.blit(fuente_grande.render("⚡", True, NEGRO), (868, 252))

        # Campos de texto mejorados
        rect_ancho = pygame.Rect(450, 280, 200, 50)
        rect_alto = pygame.Rect(450, 350, 200, 50)

        # Efecto de campo activo
        color_borde_ancho = DORADO if activo_ancho else GRIS_OSCURO
        color_borde_alto = DORADO if activo_alto else GRIS_OSCURO
        
        pygame.draw.rect(pantalla, BLANCO, rect_ancho, border_radius=8)
        pygame.draw.rect(pantalla, color_borde_ancho, rect_ancho, 3, border_radius=8)
        
        pygame.draw.rect(pantalla, BLANCO, rect_alto, border_radius=8)
        pygame.draw.rect(pantalla, color_borde_alto, rect_alto, 3, border_radius=8)

        # Etiquetas con iconos
        pantalla.blit(fuente_grande.render("📏 Ancho:", True, NEGRO), (320, 290))
        pantalla.blit(fuente_grande.render("📐 Alto:", True, NEGRO), (320, 360))
        
        # Texto de entrada
        texto_ancho = fuente_grande.render(ancho_input if ancho_input else "0", True, NEGRO)
        texto_alto = fuente_grande.render(alto_input if alto_input else "0", True, NEGRO)
        
        pantalla.blit(texto_ancho, (460, 290))
        pantalla.blit(texto_alto, (460, 360))

        # Botón de iniciar mejorado
        boton_iniciar = pygame.Rect(450, 430, 200, 60)
        color_boton = VERDE if ancho_input.isdigit() and alto_input.isdigit() else GRIS
        pygame.draw.rect(pantalla, color_boton, boton_iniciar, border_radius=12)
        pygame.draw.rect(pantalla, DORADO, boton_iniciar, 3, border_radius=12)
        
        texto_boton = fuente_titulo.render("🚀 INICIAR", True, BLANCO)
        pantalla.blit(texto_boton, (ANCHO//2 - texto_boton.get_width()//2, 445))

        # Información adicional
        info_texto = fuente.render("💡 Tip: Los mapas grandes (ej: 50x50) pueden ser más lentos de editar", True, GRIS_OSCURO)
        pantalla.blit(info_texto, (ANCHO//2 - info_texto.get_width()//2, 520))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_ancho.collidepoint(evento.pos):
                    activo_ancho, activo_alto = True, False
                elif rect_alto.collidepoint(evento.pos):
                    activo_ancho, activo_alto = False, True
                elif boton_iniciar.collidepoint(evento.pos) and ancho_input.isdigit() and alto_input.isdigit():
                    return int(ancho_input), int(alto_input)
                else:
                    activo_ancho, activo_alto = False, False

            if evento.type == pygame.KEYDOWN:
                if activo_ancho:
                    if evento.key == pygame.K_BACKSPACE:
                        ancho_input = ancho_input[:-1]
                    elif evento.unicode.isdigit() and len(ancho_input) < 3:
                        ancho_input += evento.unicode
                elif activo_alto:
                    if evento.key == pygame.K_BACKSPACE:
                        alto_input = alto_input[:-1]
                    elif evento.unicode.isdigit() and len(alto_input) < 3:
                        alto_input += evento.unicode

        # Efecto hover en botón
        if boton_iniciar.collidepoint(pygame.mouse.get_pos()) and ancho_input.isdigit() and alto_input.isdigit():
            pygame.draw.rect(pantalla, DORADO, boton_iniciar, 4, border_radius=12)

        pygame.display.flip()
        clock.tick(30)


# ============================================================
#                  EDITOR PRINCIPAL
# ============================================================

def editor_mapa(columnas, filas):
    global zoom, offset_x, offset_y, mensaje_estado

    MAPA_ANCHO = ANCHO - PANEL_IZQ - PANEL_DER
    MAPA_ALTO = ALTO - BARRA_SUP - FOOTER_ALTURA

    # --- CREAR MAPA VACÍO CON CAPAS COMPLETAS ---
    mapas = {
        "fondo": [[0 for _ in range(columnas)] for _ in range(filas)],
        "objetos": [[0 for _ in range(columnas)] for _ in range(filas)],
        "colisiones": [[0 for _ in range(columnas)] for _ in range(filas)],
        "spawn_points": [[0 for _ in range(columnas)] for _ in range(filas)]
    }
    capa_actual = "fondo"

    # --- VARIABLES PARA MENSAJES TEMPORALES ---
    mensaje_temporal = ""
    tiempo_mensaje = 0
    duracion_mensaje = 5  # segundos

    # --- SISTEMA UNDO/REDO ---
    historial = []
    historial_indice = -1
    MAX_HISTORIAL = 50

    def guardar_estado_undo():
        nonlocal historial, historial_indice
        estado = {
            "fondo": [fila[:] for fila in mapas["fondo"]],
            "objetos": [fila[:] for fila in mapas["objetos"]],
            "colisiones": [fila[:] for fila in mapas["colisiones"]],
            "spawn_points": [fila[:] for fila in mapas["spawn_points"]]
        }
        historial = historial[:historial_indice+1]
        historial.append(estado)
        if len(historial) > MAX_HISTORIAL:
            historial.pop(0)
        historial_indice = len(historial) - 1

    def deshacer():
        nonlocal historial_indice
        if historial_indice > 0:
            historial_indice -= 1
            estado = historial[historial_indice]
            for capa in mapas:
                if capa in estado:
                    for f in range(filas):
                        for c in range(columnas):
                            mapas[capa][f][c] = estado[capa][f][c]
            return "↩️ Deshecho"
        return "❌ No hay más acciones para deshacer"

    def rehacer():
        nonlocal historial_indice
        if historial_indice < len(historial) - 1:
            historial_indice += 1
            estado = historial[historial_indice]
            for capa in mapas:
                if capa in estado:
                    for f in range(filas):
                        for c in range(columnas):
                            mapas[capa][f][c] = estado[capa][f][c]
            return "↪️ Rehecho"
        return "❌ No hay más acciones para rehacer"

    # Guardar estado inicial
    guardar_estado_undo()

    # --- HERRAMIENTAS ---
    herramientas = ["lapiz", "borrador", "relleno", "seleccion"]
    herramienta_actual = "lapiz"
    seleccion_activa = False
    seleccion_rect = pygame.Rect(0, 0, 0, 0)
    seleccion_inicio = (0, 0)

    # --- CARGAR TILES ---
    if not os.path.exists("assets"):
        os.makedirs("assets")

    TILES = {}
    PROPIEDADES_TILES = {
        1: {"nombre": "Pasto", "colision": False, "tipo": "suelo"},
        2: {"nombre": "Agua", "colision": True, "tipo": "liquido"},
        3: {"nombre": "Árbol", "colision": True, "tipo": "obstaculo"},
        4: {"nombre": "Suelo", "colision": False, "tipo": "suelo"}
    }
    
    id_tile = 1
    for archivo in os.listdir("assets"):
        if archivo.endswith(".png"):
            img = pygame.image.load(os.path.join("assets", archivo))
            img = pygame.transform.scale(img, (TILE, TILE))
            TILES[id_tile] = img
            id_tile += 1

    tile_actual = 1

    # --- FUNCIONES MEJORADAS ---
    def dibujar_texto(texto, x, y, color=NEGRO):
        pantalla.blit(fuente.render(texto, True, color), (x, y))

    def dibujar_mensaje_temporal(mensaje):
        nonlocal mensaje_temporal, tiempo_mensaje
        mensaje_temporal = mensaje
        tiempo_mensaje = time.time()

    def dibujar_boton_mejorado(texto, x, y, ancho, alto, color_base, hover=False, activo=False):
        rect = pygame.Rect(x, y, ancho, alto)
        
        # Efecto hover - botón más grande
        if hover:
            rect.inflate_ip(6, 6)  # Agranda el botón
            color = [min(c + 30, 255) for c in color_base]  # Color más claro
        else:
            color = color_base
        
        # Efecto activo - borde especial
        if activo:
            pygame.draw.rect(pantalla, NARANJA, rect, 0, border_radius=8)  # Fondo naranja para activo
            pygame.draw.rect(pantalla, DORADO, rect, 3, border_radius=8)    # Borde dorado
        else:
            pygame.draw.rect(pantalla, color, rect, 0, border_radius=8)
            pygame.draw.rect(pantalla, NEGRO, rect, 2, border_radius=8)    # Borde normal
        
        # Texto centrado
        texto_surf = fuente.render(texto, True, NEGRO)
        texto_rect = texto_surf.get_rect(center=rect.center)
        pantalla.blit(texto_surf, texto_rect)
        
        return rect

    def herramienta_relleno(grid_x, grid_y, tile_id):
        """Algoritmo de relleno (flood fill)"""
        target_tile = mapas[capa_actual][grid_y][grid_x]
        if target_tile == tile_id:
            return
        
        stack = [(grid_x, grid_y)]
        cambiados = set()
        
        while stack:
            x, y = stack.pop()
            if (0 <= x < columnas and 0 <= y < filas and 
                mapas[capa_actual][y][x] == target_tile and 
                (x, y) not in cambiados):
                
                mapas[capa_actual][y][x] = tile_id
                cambiados.add((x, y))
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

    def guardar_mapa():
        os.makedirs("maps", exist_ok=True)
        try:
            with open("maps/mapa_guardado.json", "w") as archivo:
                json.dump(mapas, archivo, indent=2)
            return "✅ Mapa guardado correctamente en maps/mapa_guardado.json"
        except Exception as e:
            return f"❌ Error al guardar: {str(e)}"

    def cargar_mapa():
        nonlocal mapas
        try:
            with open("maps/mapa_guardado.json", "r") as archivo:
                datos = json.load(archivo)
            
            # Validar estructura
            if not all(capa in datos for capa in ["fondo", "objetos"]):
                return "❌ Archivo de mapa corrupto"
                
            mapas = datos
            guardar_estado_undo()  # Guardar estado después de cargar
            return "📂 Mapa cargado correctamente desde maps/mapa_guardado.json"
        except FileNotFoundError:
            return "⚠️ No se encontró maps/mapa_guardado.json"
        except Exception as e:
            return f"❌ Error al cargar: {str(e)}"

    def limpiar_mapa():
        for capa in mapas:
            for f in range(filas):
                for c in range(columnas):
                    mapas[capa][f][c] = 0
        guardar_estado_undo()
        return "🧹 Mapa completamente limpiado"

    def exportar_mapa_png():
        os.makedirs("export", exist_ok=True)
        try:
            superficie = pygame.Surface((columnas * TILE, filas * TILE))
            superficie.fill(BLANCO)
            for capa in ["fondo", "objetos"]:
                for f in range(filas):
                    for c in range(columnas):
                        tipo = mapas[capa][f][c]
                        if tipo in TILES:
                            superficie.blit(TILES[tipo], (c * TILE, f * TILE))
            
            nombre_archivo = "export/mapa_exportado.png"
            pygame.image.save(superficie, nombre_archivo)
            mensaje = f"🖼️ ¡EXPORTADO EXITOSO! Archivo: {nombre_archivo}"
            dibujar_mensaje_temporal(mensaje)
            return mensaje
        except Exception as e:
            return f"❌ Error al exportar: {str(e)}"

    def obtener_posicion_mapa(pos):
        """Convierte posición de pantalla a posición en el mapa"""
        x, y = pos
        if PANEL_IZQ < x < ANCHO - PANEL_DER and BARRA_SUP < y < ALTO - FOOTER_ALTURA:
            grid_x = int((x - PANEL_IZQ - offset_x) // (TILE * zoom))
            grid_y = int((y - BARRA_SUP - offset_y) // (TILE * zoom))
            if 0 <= grid_x < columnas and 0 <= grid_y < filas:
                return grid_x, grid_y
        return None, None

    # --- LOOP PRINCIPAL ---
    moviendo = False
    mouse_pos_actual = (0, 0)
    
    while True:
        tiempo_actual = time.time()
        mouse_pos_actual = pygame.mouse.get_pos()
        mensaje_estado = f"Herramienta: {herramienta_actual} | Capa: {capa_actual} | Mapa: {columnas}x{filas}"

        # Limpiar mensaje temporal después de 5 segundos
        if mensaje_temporal and tiempo_actual - tiempo_mensaje > duracion_mensaje:
            mensaje_temporal = ""

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- CONTROLES DE TECLADO (UNDO/REDO) ---
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    mensaje_estado = deshacer()
                elif evento.key == pygame.K_y and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    mensaje_estado = rehacer()

            # --- ZOOM ---
            if evento.type == pygame.MOUSEWHEEL:
                zoom += evento.y * 0.1
                zoom = max(0.5, min(2.0, zoom))

            # --- MOVER MAPA ---
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 2:  # Botón del medio
                    moviendo = True
                    pos_mouse_anterior = pygame.mouse.get_pos()
                elif evento.button == 1:  # Click izquierdo
                    grid_x, grid_y = obtener_posicion_mapa(evento.pos)
                    if grid_x is not None:
                        if herramienta_actual == "relleno":
                            guardar_estado_undo()
                            herramienta_relleno(grid_x, grid_y, tile_actual)
                        elif herramienta_actual == "seleccion":
                            seleccion_activa = True
                            seleccion_inicio = (grid_x, grid_y)
                            seleccion_rect = pygame.Rect(grid_x, grid_y, 1, 1)

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
                grid_x, grid_y = obtener_posicion_mapa((x, y))
                
                if grid_x is not None:
                    if evento.button == 1:  # Click izquierdo
                        if herramienta_actual == "lapiz":
                            guardar_estado_undo()
                            mapas[capa_actual][grid_y][grid_x] = tile_actual
                        elif herramienta_actual == "borrador":
                            guardar_estado_undo()
                            mapas[capa_actual][grid_y][grid_x] = 0
                    elif evento.button == 3:  # Click derecho
                        mapas[capa_actual][grid_y][grid_x] = 0

                # Paleta de tiles
                for i, img in TILES.items():
                    rect = pygame.Rect(70, 80 + (i - 1) * 50, 60, 40)
                    if rect.collidepoint(x, y):
                        tile_actual = i

                # Panel izquierdo - Herramientas
                herramientas_y = 350
                for i, herramienta in enumerate(herramientas):
                    rect_herramienta = pygame.Rect(50, herramientas_y + i * 40, 100, 30)
                    if rect_herramienta.collidepoint(x, y):
                        herramienta_actual = herramienta

        # --- DIBUJAR ---
        pantalla.fill(BLANCO)

        # Barra superior
        pygame.draw.rect(pantalla, AZUL_BARRA, (0, 0, ANCHO, BARRA_SUP))
        pantalla.blit(fuente.render("Archivo | Vista | Ayuda | Ctrl+Z: Deshacer | Ctrl+Y: Rehacer", True, BLANCO), (20, 10))

        # Área del mapa
        mapa_x, mapa_y = PANEL_IZQ, BARRA_SUP
        pygame.draw.rect(pantalla, (245, 245, 245), (mapa_x, mapa_y, ANCHO - PANEL_IZQ - PANEL_DER, ALTO - BARRA_SUP - FOOTER_ALTURA))
        
        # Dibujar tiles
        for capa in ["fondo", "objetos"]:
            for f in range(filas):
                for c in range(columnas):
                    tipo = mapas[capa][f][c]
                    if tipo in TILES:
                        img = pygame.transform.scale(TILES[tipo], (int(TILE * zoom), int(TILE * zoom)))
                        pantalla.blit(img, (mapa_x + c*TILE*zoom + offset_x, mapa_y + f*TILE*zoom + offset_y))

        # Dibujar colisiones (en rojo semitransparente)
        for f in range(filas):
            for c in range(columnas):
                if mapas["colisiones"][f][c] == 1:
                    rect = pygame.Rect(mapa_x + c*TILE*zoom + offset_x, mapa_y + f*TILE*zoom + offset_y, 
                                     int(TILE * zoom), int(TILE * zoom))
                    s = pygame.Surface((int(TILE * zoom), int(TILE * zoom)), pygame.SRCALPHA)
                    s.fill((255, 0, 0, 100))  # Rojo semitransparente
                    pantalla.blit(s, rect)

        # Dibujar spawn points (en verde semitransparente)
        for f in range(filas):
            for c in range(columnas):
                if mapas["spawn_points"][f][c] == 1:
                    rect = pygame.Rect(mapa_x + c*TILE*zoom + offset_x, mapa_y + f*TILE*zoom + offset_y, 
                                     int(TILE * zoom), int(TILE * zoom))
                    s = pygame.Surface((int(TILE * zoom), int(TILE * zoom)), pygame.SRCALPHA)
                    s.fill((0, 255, 0, 100))  # Verde semitransparente
                    pantalla.blit(s, rect)

        # Cuadrícula
        for x in range(columnas + 1):
            pygame.draw.line(pantalla, GRIS, (mapa_x + x*TILE*zoom + offset_x, mapa_y + offset_y),
                             (mapa_x + x*TILE*zoom + offset_x, mapa_y + filas*TILE*zoom + offset_y))
        for y in range(filas + 1):
            pygame.draw.line(pantalla, GRIS, (mapa_x + offset_x, mapa_y + y*TILE*zoom + offset_y),
                             (mapa_x + columnas*TILE*zoom + offset_x, mapa_y + y*TILE*zoom + offset_y))

        # Panel izquierdo (paleta y herramientas)
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

        # Herramientas en panel izquierdo
        pantalla.blit(fuente.render("🛠️ Herramientas", True, NEGRO), (50, 320))
        herramientas_y = 350
        colores_herramientas = {
            "lapiz": AZUL,
            "borrador": ROJO, 
            "relleno": VERDE,
            "seleccion": MORADO
        }
        
        botones_herramientas = []
        for i, herramienta in enumerate(herramientas):
            hover = pygame.Rect(50, herramientas_y + i * 40, 100, 30).collidepoint(mouse_pos_actual)
            activo = herramienta_actual == herramienta
            rect_herramienta = dibujar_boton_mejorado(
                herramienta.capitalize(), 
                50, herramientas_y + i * 40, 
                100, 30, 
                colores_herramientas.get(herramienta, GRIS),
                hover=hover,
                activo=activo
            )
            botones_herramientas.append(rect_herramienta)

        # Panel derecho
        pygame.draw.rect(pantalla, (240, 240, 240), (ANCHO - PANEL_DER, BARRA_SUP, PANEL_DER, ALTO - FOOTER_ALTURA))
        pantalla.blit(fuente.render("🧱 Capas y Acciones", True, NEGRO), (ANCHO - PANEL_DER + 40, 50))
        
        # Botones de acciones con hover
        boton_guardar_rect = dibujar_boton_mejorado("💾 Guardar", ANCHO - PANEL_DER + 25, 130, 150, 30, VERDE_OSCURO,
                                                   hover=pygame.Rect(ANCHO - PANEL_DER + 25, 130, 150, 30).collidepoint(mouse_pos_actual))
        boton_cargar_rect = dibujar_boton_mejorado("📂 Cargar", ANCHO - PANEL_DER + 25, 170, 150, 30, AZUL_OSCURO,
                                                  hover=pygame.Rect(ANCHO - PANEL_DER + 25, 170, 150, 30).collidepoint(mouse_pos_actual))
        boton_limpiar_rect = dibujar_boton_mejorado("🧹 Limpiar", ANCHO - PANEL_DER + 25, 210, 150, 30, ROJO,
                                                   hover=pygame.Rect(ANCHO - PANEL_DER + 25, 210, 150, 30).collidepoint(mouse_pos_actual))
        boton_exportar_rect = dibujar_boton_mejorado("🖼️ Exportar PNG", ANCHO - PANEL_DER + 25, 250, 150, 30, MORADO,
                                                    hover=pygame.Rect(ANCHO - PANEL_DER + 25, 250, 150, 30).collidepoint(mouse_pos_actual))
        
        # Botones de capas con hover y activo
        colores_capas = {
            "fondo": AZUL,
            "objetos": VERDE, 
            "colisiones": ROJO,
            "spawn_points": AMARILLO
        }
        
        boton_capa_fondo_rect = dibujar_boton_mejorado("🌍 Fondo", ANCHO - PANEL_DER + 25, 290, 150, 30, 
                                                      colores_capas["fondo"],
                                                      hover=pygame.Rect(ANCHO - PANEL_DER + 25, 290, 150, 30).collidepoint(mouse_pos_actual),
                                                      activo=capa_actual == "fondo")
        boton_capa_objetos_rect = dibujar_boton_mejorado("🎯 Objetos", ANCHO - PANEL_DER + 25, 330, 150, 30, 
                                                        colores_capas["objetos"],
                                                        hover=pygame.Rect(ANCHO - PANEL_DER + 25, 330, 150, 30).collidepoint(mouse_pos_actual),
                                                        activo=capa_actual == "objetos")
        boton_capa_colisiones_rect = dibujar_boton_mejorado("🚫 Colisiones", ANCHO - PANEL_DER + 25, 370, 150, 30, 
                                                           colores_capas["colisiones"],
                                                           hover=pygame.Rect(ANCHO - PANEL_DER + 25, 370, 150, 30).collidepoint(mouse_pos_actual),
                                                           activo=capa_actual == "colisiones")
        boton_capa_spawn_rect = dibujar_boton_mejorado("👤 Spawn Points", ANCHO - PANEL_DER + 25, 410, 150, 30, 
                                                      colores_capas["spawn_points"],
                                                      hover=pygame.Rect(ANCHO - PANEL_DER + 25, 410, 150, 30).collidepoint(mouse_pos_actual),
                                                      activo=capa_actual == "spawn_points")

        # Detectar clics en botones del panel derecho
        if pygame.mouse.get_pressed()[0]:  # Si click izquierdo está presionado
            if boton_guardar_rect.collidepoint(mouse_pos_actual):
                mensaje_estado = guardar_mapa()
            elif boton_cargar_rect.collidepoint(mouse_pos_actual):
                mensaje_estado = cargar_mapa()
            elif boton_limpiar_rect.collidepoint(mouse_pos_actual):
                mensaje_estado = limpiar_mapa()
            elif boton_exportar_rect.collidepoint(mouse_pos_actual):
                mensaje_estado = exportar_mapa_png()
            elif boton_capa_fondo_rect.collidepoint(mouse_pos_actual):
                capa_actual = "fondo"
            elif boton_capa_objetos_rect.collidepoint(mouse_pos_actual):
                capa_actual = "objetos"
            elif boton_capa_colisiones_rect.collidepoint(mouse_pos_actual):
                capa_actual = "colisiones"
            elif boton_capa_spawn_rect.collidepoint(mouse_pos_actual):
                capa_actual = "spawn_points"

        # --- DIBUJAR MENSAJE TEMPORAL GRANDE ---
        if mensaje_temporal:
            # Fondo del mensaje
            mensaje_rect = pygame.Rect(50, 50, 600, 80)
            s = pygame.Surface((600, 80), pygame.SRCALPHA)
            s.fill((50, 50, 50, 200))  # Fondo oscuro semi-transparente
            pantalla.blit(s, (50, 50))
            pygame.draw.rect(pantalla, DORADO, mensaje_rect, 3, border_radius=10)
            
            # Texto del mensaje
            lineas = mensaje_temporal.split('\n')
            for i, linea in enumerate(lineas):
                texto = fuente_grande.render(linea, True, BLANCO)
                pantalla.blit(texto, (70, 70 + i * 30))

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
