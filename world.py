import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA

class World:
    """
    Clase que representa el mundo del juego, incluyendo el mapa, puntos de control, 
    y la lógica de los enemigos.
    """

    def __init__(self, data, map_image):
        """
        Inicializa el mundo con datos de nivel, imagen del mapa y estado del juego.

        Args:
            data (dict): Datos del nivel que incluyen información del mapa y waypoints.
            map_image (Surface): Imagen del mapa que se renderiza en pantalla.
        """
        self.level = 1
        self.game_speed = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        """
        Procesa los datos del nivel para extraer la información del mapa y los waypoints.
        """
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    self.process_waypoints(obj["polyline"])

    def process_waypoints(self, data):
        """
        Procesa los waypoints y extrae las coordenadas X e Y.

        Args:
            data (list): Lista de puntos de un waypoint que contiene coordenadas X e Y.
        """
        for point in data:
            x = point.get("x")
            y = point.get("y")
            self.waypoints.append((x, y))

    def process_enemies(self):
        """
        Genera una lista de enemigos basándose en los datos de spawn del nivel actual
        y mezcla la lista para variar el orden de aparición.
        """
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type, count in enemies.items():
            self.enemy_list.extend([enemy_type] * count)
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        """
        Comprueba si el nivel actual se ha completado, evaluando si todos los enemigos
        han sido derrotados o han escapado.

        Returns:
            bool: True si el nivel está completo, False en caso contrario.
        """
        return (self.killed_enemies + self.missed_enemies) == len(self.enemy_list)

    def reset_level(self):
        """
        Reinicia el estado del nivel, incluyendo las listas de enemigos y contadores.
        """
        self.enemy_list.clear()
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface):
        """
        Dibuja el mapa en la superficie proporcionada.

        Args:
            surface (Surface): Superficie de Pygame donde se renderiza el mapa.
        """
        surface.blit(self.image, (0, 0))
