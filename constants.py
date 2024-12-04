ROWS = 15  # Número de filas en el mapa del juego
COLS = 15  # Número de columnas en el mapa del juego
TILE_SIZE = 48  # Tamaño de cada casilla en píxeles

SIDE_PANEL = 300  # Ancho del panel lateral en píxeles
SCREEN_WIDTH = TILE_SIZE * COLS  # Ancho total de la pantalla en píxeles
SCREEN_HEIGHT = TILE_SIZE * ROWS  # Altura total de la pantalla en píxeles

FPS = 60  # Cuadros por segundo para el bucle del juego
HEALTH = 1  # Salud inicial del jugador
MONEY = 700  # Dinero inicial del jugador
TOTAL_LEVELS = 3  # Total de niveles en el juego

SPAWN_COOLDOWN = 400  # Tiempo de espera entre la generación de enemigos (en ms)

TURRET_LEVELS = 4  # Número máximo de niveles de mejora para torretas
BUY_COST = 100  # Costo inicial para comprar una torreta
UPGRADE_COST = 50  # Costo para mejorar una torreta al siguiente nivel
KILL_REWARD = 5  # Recompensa en dinero por eliminar un enemigo
LEVEL_COMPLETE_REWARD = 100  # Recompensa al completar un nivel
ANIMATION_STEPS = 8  # Cantidad de pasos de animación para torretas
ANIMATION_DELAY = 15  # Retraso entre pasos de animación (en frames)
DAMAGE = 5  # Daño que inflige cada disparo de una torreta
