import pygame
import sys
import json
import os

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Editor de Mapas 2D")

# Colores
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
NEGRO = (0, 0, 0)
AZUL = (100, 150, 255)
VERDE = (100, 200, 100)
ROJO = (220, 100, 100)
NARANJA = (255, 180, 50)
MORADO = (170, 130, 255)

# Tipos de tiles (colores)
TILES = {
    1: (100, 200, 100),   # Pasto
    2: (100, 100, 255),   # Agua
    3: (150, 150, 150),   # Piedra
}

# Parámetros del mapa
TILE = 40
MAPA_ANCHO = 800
PALETA_X = MAPA_ANCHO + 20

filas = ALTO // TILE
columnas = MAPA_ANCHO // TILE
mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

tile_actual = 1

# Fuente
fuente = pygame.font.SysFont("Arial", 20)

# --- FUNCIONES AUXILIARES ---

def dibujar_boton(texto, x, y, color):
    """Crea un botón rectangular con texto"""
    rect = pygame.Rect(x, y, 140, 40)
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, NEGRO, rect, 2)
    texto_render = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_render, (x + 20, y + 10))
    return rect

def guardar_mapa(nombre="maps/mapa_guardado.json"):
    os.makedirs("maps", exist_ok=True)
    with open(nombre, "w") as archivo:
        json.dump(mapa, archivo)
    print(f"✅ Mapa guardado en {nombre}")

def cargar_mapa(nombre="maps/mapa_guardado.json"):
    global mapa
    try:
        with open(nombre, "r") as archivo:
            mapa = json.load(archivo)
        print(f"📂 Mapa cargado desde {nombre}")
    except FileNotFoundError:
        print("⚠️ No se encontró el archivo del mapa guardado.")

def limpiar_mapa():
    global mapa
    mapa = [[0 for _ in range(columnas)] for _ in range(filas)]
    print("🧹 Mapa limpiado.")

def exportar_mapa_json(nombre="export/mapa_exportado.json"):
    """Guarda el mapa en formato JSON para uso externo"""
    os.makedirs("export", exist_ok=True)
    datos_export = {
        "tile_size": TILE,
        "rows": filas,
        "cols": columnas,
        "data": mapa
    }
    with open(nombre, "w") as archivo:
        json.dump(datos_export, archivo, indent=2)
    print(f"🚀 Mapa exportado (JSON) a {nombre}")

def exportar_mapa_png(nombre="export/mapa_preview.png"):
    """Exporta el mapa actual como imagen PNG"""
    os.makedirs("export", exist_ok=True)

    # Crear una superficie del tamaño del mapa
    superficie = pygame.Surface((MAPA_ANCHO, ALTO))
    superficie.fill(BLANCO)

    # Dibujar tiles en la superficie
    for f in range(filas):
        for c in range(columnas):
            tipo = mapa[f][c]
            if tipo in TILES:
                pygame.draw.rect(superficie, TILES[tipo], (c*TILE, f*TILE, TILE, TILE))
    
    # Guardar como imagen PNG
    pygame.image.save(superficie, nombre)
    print(f"🖼️ Imagen exportada a {nombre}")

# --- BUCLE PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clics
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila = y // TILE
            columna = x // TILE

            if x < MAPA_ANCHO:
                if evento.button == 1:
                    mapa[fila][columna] = tile_actual
                elif evento.button == 3:
                    mapa[fila][columna] = 0
            else:
                opcion = y // 60 + 1
                if opcion in TILES:
                    tile_actual = opcion

                # Botones
                if boton_guardar.collidepoint(x, y):
                    guardar_mapa()
                elif boton_cargar.collidepoint(x, y):
                    cargar_mapa()
                elif boton_limpiar.collidepoint(x, y):
                    limpiar_mapa()
                elif boton_exportar_json.collidepoint(x, y):
                    exportar_mapa_json()
                elif boton_exportar_png.collidepoint(x, y):
                    exportar_mapa_png()

    # --- DIBUJAR ---
    pantalla.fill(BLANCO)

    # Dibujar tiles
    for f in range(filas):
        for c in range(columnas):
            tipo = mapa[f][c]
            if tipo in TILES:
                pygame.draw.rect(pantalla, TILES[tipo], (c*TILE, f*TILE, TILE, TILE))

    # Cuadrícula
    for x in range(0, MAPA_ANCHO, TILE):
        pygame.draw.line(pantalla, GRIS, (x, 0), (x, ALTO))
    for y in range(0, ALTO, TILE):
        pygame.draw.line(pantalla, GRIS, (0, y), (MAPA_ANCHO, y))

    # Paleta lateral
    y_paleta = 20
    for i, color in TILES.items():
        rect = pygame.Rect(PALETA_X, y_paleta, 60, 40)
        pygame.draw.rect(pantalla, color, rect)
        if i == tile_actual:
            pygame.draw.rect(pantalla, NEGRO, rect, 3)
        y_paleta += 60

    # Botones
    boton_guardar = dibujar_boton("Guardar", PALETA_X, 300, VERDE)
    boton_cargar = dibujar_boton("Cargar", PALETA_X, 350, AZUL)
    boton_limpiar = dibujar_boton("Limpiar", PALETA_X, 400, ROJO)
    boton_exportar_json = dibujar_boton("Exportar JSON", PALETA_X, 450, NARANJA)
    boton_exportar_png = dibujar_boton("Exportar PNG", PALETA_X, 500, MORADO)

    pygame.display.flip()
