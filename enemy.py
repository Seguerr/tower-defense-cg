import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.enemy_type = enemy_type  # Asignamos enemy_type
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.max_health = self.health  # Salud máxima
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        # Define un waypoint objetivo
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            if not self.alive():  # Asegurarse de que solo decremente una vez
                return
            # El enemigo ha alcanzado el final del camino
            self.kill()
            world.health -= 1
            world.missed_enemies += 1
            return

        # Calcula la distancia al objetivo
        dist = self.movement.length()
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        # Calcula la distancia al siguiente waypoint
        dist = self.target - self.pos
        # Usa la distancia para calcular el ángulo
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # Rota la imagen y actualiza el rectángulo
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()

    def draw_health_bar(self, surface):
      # Define el ancho y alto de la barra
      bar_width = self.rect.width * 0.6  # Reduce el ancho de la barra al 60% del ancho del rectángulo
      bar_height = 5

      # Calcula la proporción de salud
      health_ratio = max(0, self.health / self.max_health)

      # Coordenadas de la barra
      bar_x = self.rect.left + (self.rect.width - bar_width) / 2  # Centra la barra encima del enemigo
      bar_y = self.rect.top - bar_height - 2  # Justo encima del enemigo

      # Dibuja el fondo de la barra (rojo)
      pg.draw.rect(surface, "red", (bar_x, bar_y, bar_width, bar_height))

      # Dibuja la parte de la barra que representa la salud actual (verde)
      pg.draw.rect(surface, "green", (bar_x, bar_y, bar_width * health_ratio, bar_height))