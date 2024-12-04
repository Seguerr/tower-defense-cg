import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA


"""Clase que representa una torreta en el juego.
Atributos:
upgrade_level (int): Nivel actual de la torreta.
range (int): Rango de disparo de la torreta.
cooldown (int): Tiempo de espera entre disparos.
last_shot (int): Tiempo del último disparo.
selected (bool): Indica si la torreta está seleccionada.
target (Enemy): Enemigo objetivo actual.
x (float): Coordenada X del centro de la torreta.
y (float): Coordenada Y del centro de la torreta.
shot_fx (pg.mixer.Sound): Efecto de sonido para los disparos.
animation_list (list): Lista de imágenes para animación.
frame_index (int): Índice del fotograma actual en la animación.
update_time (int): Última vez que se actualizó el fotograma.
angle (float): Ángulo de rotación de la torreta.
image (pg.Surface): Imagen actual de la torreta.
rect (pg.Rect): Rectángulo que delimita la torreta.
range_image (pg.Surface): Imagen que muestra el rango de la torreta.
range_rect (pg.Rect): Rectángulo que delimita el rango de la torreta.
"""
class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # Variables de posición
        self.tile_x = tile_x
        self.tile_y = tile_y
        # Calcular coordenadas del centro
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        # Efecto de sonido del disparo
        self.shot_fx = shot_fx

        # Variables de animación
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # Actualizar imagen
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Crear círculo transparente que muestra el rango
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet):
        # Extraer imágenes del spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, world):
        # Si hay un objetivo, reproducir la animación de disparo
        if self.target:
            self.play_animation()
        else:
            # Buscar un nuevo objetivo una vez que la torreta se haya enfriado
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # Encontrar un enemigo para apuntar
        x_dist = 0
        y_dist = 0
        # Comprobar la distancia a cada enemigo para ver si está en rango
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # Dañar al enemigo
                    self.target.health -= c.DAMAGE
                    # Reproducir efecto de sonido
                    self.shot_fx.play()
                    break

    def play_animation(self):
        # Actualizar imagen
        self.original_image = self.animation_list[self.frame_index]
        # Comprobar si ha pasado suficiente tiempo desde la última actualización
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            # Comprobar si la animación ha terminado y reiniciar a inactivo
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # Registrar el tiempo completado y limpiar el objetivo para que pueda comenzar el enfriamiento
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self):
        """Mejora el nivel de la torreta."""
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        # Mejorar imagen de la torreta
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        # Mejorar círculo de rango
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        """Dibuja la torreta y su rango si está seleccionada.

        Args:
                surface (pg.Surface): Superficie sobre la que se dibuja la torreta.
        """
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
