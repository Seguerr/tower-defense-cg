import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    """
    Clase para manejar enemigos en el juego.

    Atributos:
    ----------
    enemy_type : str
        Tipo de enemigo, usado para obtener datos específicos del enemigo.
    waypoints : list[tuple]
        Lista de puntos de control que el enemigo debe seguir.
    pos : Vector2
        Posición actual del enemigo.
    target_waypoint : int
        Índice del siguiente waypoint objetivo.
    health : int
        Salud actual del enemigo.
    max_health : int
        Salud máxima del enemigo.
    speed : float
        Velocidad de movimiento del enemigo.
    angle : float
        Ángulo de rotación actual del enemigo.
    original_image : pygame.Surface
        Imagen original sin rotación.
    image : pygame.Surface
        Imagen actual del enemigo, rotada según el ángulo.
    rect : pygame.Rect
        Rectángulo delimitador de la imagen actual.
    """

    def __init__(self, enemy_type, waypoints, images):
        """
        Inicializa un enemigo con un tipo, waypoints y una imagen.

        Parámetros:
        ----------
        enemy_type : str
            Tipo de enemigo, utilizado para definir salud, velocidad, etc.
        waypoints : list[tuple]
            Lista de coordenadas que el enemigo debe seguir.
        images : dict
            Diccionario que mapea tipos de enemigos con sus imágenes respectivas.
        """
        super().__init__()
        self.enemy_type = enemy_type
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA[enemy_type]["health"]
        self.max_health = self.health
        self.speed = ENEMY_DATA[enemy_type]["speed"]
        self.angle = 0
        self.original_image = images[enemy_type]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, world):
        """
        Actualiza el estado del enemigo en cada fotograma.

        Parámetros:
        ----------
        world : World
            Instancia del mundo del juego que contiene el estado global.
        """
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        """
        Mueve al enemigo hacia el siguiente waypoint.

        Parámetros:
        ----------
        world : World
            Instancia del mundo del juego, utilizada para manejar la salud y velocidad.
        """
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Alcanza el final del camino
            if self.alive():
                self.kill()
                world.health -= 1
                world.missed_enemies += 1
            return

        distance = self.movement.length()
        move_distance = self.speed * world.game_speed
        if distance >= move_distance:
            self.pos += self.movement.normalize() * move_distance
        else:
            self.pos += self.movement.normalize() * distance
            self.target_waypoint += 1

    def rotate(self):
        """
        Rota la imagen del enemigo hacia el siguiente waypoint.
        """
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist.y, dist.x))
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def check_alive(self, world):
        """
        Verifica si el enemigo está vivo y lo elimina si su salud es 0.

        Parámetros:
        ----------
        world : World
            Instancia del mundo del juego que maneja estadísticas como dinero y enemigos muertos.
        """
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()

    def draw_health_bar(self, surface):
        """
        Dibuja una barra de salud sobre el enemigo.

        Parámetros:
        ----------
        surface : pygame.Surface
            Superficie donde se dibuja la barra de salud.
        """
        bar_width = self.rect.width * 0.6
        bar_height = 5
        health_ratio = max(0, self.health / self.max_health)

        bar_x = self.rect.left + (self.rect.width - bar_width) / 2
        bar_y = self.rect.top - bar_height - 2

        # Barra de fondo (rojo)
        pg.draw.rect(surface, "red", (bar_x, bar_y, bar_width, bar_height))

        # Barra de salud actual (verde)
        pg.draw.rect(surface, "green", (bar_x, bar_y, bar_width * health_ratio, bar_height))
