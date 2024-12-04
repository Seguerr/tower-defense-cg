import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):
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

    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx):
        """Inicializa una nueva instancia de la torreta.

        Args:
            sprite_sheets (list): Lista de hojas de sprites para diferentes niveles de la torreta.
            tile_x (int): Coordenada X del tile en el que se ubica la torreta.
            tile_y (int): Coordenada Y del tile en el que se ubica la torreta.
            shot_fx (pg.mixer.Sound): Efecto de sonido para los disparos.
        """
        super().__init__()

        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1]["range"]
        self.cooldown = TURRET_DATA[self.upgrade_level - 1]["cooldown"]
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (tile_x + 0.5) * c.TILE_SIZE
        self.y = (tile_y + 0.5) * c.TILE_SIZE
        self.shot_fx = shot_fx

        self.sprite_sheets = sprite_sheets
        self.animation_list = self._load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self._create_range_circle()

    def _load_images(self, sprite_sheet):
        """Carga las imágenes de la hoja de sprites.

        Args:
            sprite_sheet (pg.Surface): Hoja de sprites.

        Returns:
            list: Lista de superficies extraídas de la hoja de sprites.
        """
        size = sprite_sheet.get_height()
        return [sprite_sheet.subsurface(x * size, 0, size, size) for x in range(c.ANIMATION_STEPS)]

    def _create_range_circle(self):
        """Crea una imagen circular para mostrar el rango de la torreta."""
        self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
        pg.draw.circle(self.range_image, (255, 255, 255, 100), (self.range, self.range), self.range)
        self.range_rect = self.range_image.get_rect(center=self.rect.center)

    def update(self, enemy_group, world):
        """Actualiza el estado de la torreta.

        Args:
            enemy_group (pg.sprite.Group): Grupo de enemigos en el juego.
            world (World): Objeto del mundo que contiene la velocidad del juego.
        """
        if self.target:
            self._play_animation()
        elif pg.time.get_ticks() - self.last_shot > self.cooldown / world.game_speed:
            self._pick_target(enemy_group)

    def _pick_target(self, enemy_group):
        """Selecciona un enemigo dentro del rango como objetivo.

        Args:
            enemy_group (pg.sprite.Group): Grupo de enemigos.
        """
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                if math.hypot(x_dist, y_dist) < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= c.DAMAGE
                    self.shot_fx.play()
                    break

    def _play_animation(self):
        """Reproduce la animación de disparo."""
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.animation_list)
            if self.frame_index == 0:
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self):
        """Mejora el nivel de la torreta."""
        self.upgrade_level += 1
        data = TURRET_DATA[self.upgrade_level - 1]
        self.range, self.cooldown = data["range"], data["cooldown"]
        self.animation_list = self._load_images(self.sprite_sheets[self.upgrade_level - 1])
        self._create_range_circle()

    def draw(self, surface):
        """Dibuja la torreta y su rango si está seleccionada.

        Args:
            surface (pg.Surface): Superficie sobre la que se dibuja la torreta.
        """
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
