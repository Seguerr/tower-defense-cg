import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

# Inicializar pygame
pg.init()

# Crear reloj
clock = pg.time.Clock()

# Crear ventana del juego
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

# Variables del juego
game_over = False
game_outcome = 0  # -1 es derrota y 1 es victoria
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

# Cargar imágenes
map_image = pg.image.load('levels/level.png').convert_alpha()
turret_spritesheets = [pg.image.load(f'assets/images/turrets/turret_{x}.png').convert_alpha() for x in range(1, c.TURRET_LEVELS + 1)]
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
enemy_images = {
  "normal": pg.image.load('assets/images/enemies/drone_1.png').convert_alpha(),
  "medium": pg.image.load('assets/images/enemies/drone_2.png').convert_alpha(),
  "ufo": pg.image.load('assets/images/enemies/drone_3.png').convert_alpha(),
  "boss": pg.image.load('assets/images/enemies/boss.png').convert_alpha()
}
buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()

# Cargar sonidos
shot_fx = pg.mixer.Sound('assets/audio/laser.mp3')
shot_fx.set_volume(0.5)

# Cargar datos JSON del nivel
with open('levels/level.tmj') as file:
  world_data = json.load(file)

# Cargar fuentes para mostrar texto en la pantalla
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)

# Función para mostrar texto en la pantalla
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

# Función para mostrar datos en la pantalla
def display_data():
  pg.draw.rect(screen, "darkslategray", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
  pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT), 2)
  draw_text("Nivel: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
  draw_text("Salud: " + str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 10, 40)
  draw_text("$" + str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 10, 70)

# Función para crear una torreta
def create_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  if world.tile_map[mouse_tile_num] == 7:
    space_is_free = all((mouse_tile_x, mouse_tile_y) != (turret.tile_x, turret.tile_y) for turret in turret_group)
    if space_is_free:
      new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
      turret_group.add(new_turret)
      world.money -= c.BUY_COST

# Función para seleccionar una torreta
def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      return turret

# Función para limpiar la selección de torretas
def clear_selection():
  for turret in turret_group:
    turret.selected = False

# Crear mundo
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Crear grupos
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Crear botones
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)

# Bucle del juego
run = True
while run:
  clock.tick(c.FPS)

  #########################
  # SECCIÓN DE ACTUALIZACIÓN
  #########################

  if not game_over:
    if world.health <= 0:
      game_over = True
      game_outcome = -1  # Derrota
    if world.level > c.TOTAL_LEVELS:
      game_over = True
      game_outcome = 1  # Victoria

    enemy_group.update(world)
    turret_group.update(enemy_group, world)

    if selected_turret:
      selected_turret.selected = True

  #########################
  # SECCIÓN DE DIBUJO
  #########################

  world.draw(screen)
  enemy_group.draw(screen)
  for enemy in enemy_group:
    enemy.draw_health_bar(screen)
  for turret in turret_group:
    turret.draw(screen)

  display_data()

  if not game_over:
    if not level_started:
      if begin_button.draw(screen):
        level_started = True
    else:
      world.game_speed = 2
      if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
          enemy_type = world.enemy_list[world.spawned_enemies]
          enemy = Enemy(enemy_type, world.waypoints, enemy_images)
          enemy_group.add(enemy)
          world.spawned_enemies += 1
          last_enemy_spawn = pg.time.get_ticks()

    if world.check_level_complete():
      world.money += c.LEVEL_COMPLETE_REWARD
      world.level += 1
      level_started = False
      last_enemy_spawn = pg.time.get_ticks()
      world.reset_level()
      world.process_enemies()

    draw_text("$" + str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
    if turret_button.draw(screen):
      placing_turrets = True
    if placing_turrets:
      cursor_rect = cursor_turret.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_turret, cursor_rect)
      if cancel_button.draw(screen):
        placing_turrets = False
    if selected_turret:
      if selected_turret.upgrade_level < c.TURRET_LEVELS:
        draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
        if upgrade_button.draw(screen):
          if world.money >= c.UPGRADE_COST:
            selected_turret.upgrade()
            world.money -= c.UPGRADE_COST
  else:
    pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
    if game_outcome == -1:
      draw_text("GAME OVER", large_font, "grey0", 310, 230)
    elif game_outcome == 1:
      draw_text("YOU WIN!", large_font, "grey0", 315, 230)
    if restart_button.draw(screen):
      game_over = False
      level_started = False
      placing_turrets = False
      selected_turret = None
      last_enemy_spawn = pg.time.get_ticks()
      world = World(world_data, map_image)
      world.process_data()
      world.process_enemies()
      enemy_group.empty()
      turret_group.empty()

  for event in pg.event.get():
    if event.type == pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        selected_turret = None
        clear_selection()
        if placing_turrets:
          if world.money >= c.BUY_COST:
            create_turret(mouse_pos)
        else:
          selected_turret = select_turret(mouse_pos)

  pg.display.flip()

pg.quit()
