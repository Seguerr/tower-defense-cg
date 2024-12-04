import pygame as pg

class Button:
    """
    Clase para manejar botones interactivos en una interfaz gráfica con Pygame.

    Atributos:
    ----------
    x : int
        Coordenada X de la posición inicial del botón.
    y : int
        Coordenada Y de la posición inicial del botón.
    image : pygame.Surface
        Imagen que representa el botón.
    single_click : bool
        Indica si el botón debe ser clicado solo una vez por acción.
    rect : pygame.Rect
        Rectángulo delimitador del botón basado en la imagen.
    clicked : bool
        Bandera para evitar múltiples activaciones del botón en un solo clic.
    """
    
    def __init__(self, x, y, image, single_click=True):
        """
        Inicializa un botón con una posición, imagen y configuración de clic.

        Parámetros:
        ----------
        x : int
            Posición X del botón.
        y : int
            Posición Y del botón.
        image : pygame.Surface
            Imagen a usar como representación del botón.
        single_click : bool, opcional
            Si el botón debe realizar una acción solo en el primer clic. (por defecto True)
        """
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.single_click = single_click
        self.clicked = False

    def draw(self, surface):
        """
        Dibuja el botón en la superficie proporcionada y maneja las interacciones.

        Parámetros:
        ----------
        surface : pygame.Surface
            Superficie donde se dibuja el botón.

        Retorna:
        -------
        bool
            Verdadero si el botón es clicado, falso en caso contrario.
        """
        action_triggered = False
        mouse_pos = pg.mouse.get_pos()  # Obtener la posición actual del mouse

        # Comprobar si el cursor está sobre el botón y si se ha clicado
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] and not self.clicked:
                action_triggered = True
                if self.single_click:
                    self.clicked = True  # Registrar clic si es de tipo único

        # Reiniciar el estado de clic cuando se libera el botón del mouse
        if not pg.mouse.get_pressed()[0]:
            self.clicked = False

        # Dibujar el botón en la pantalla
        surface.blit(self.image, self.rect)

        return action_triggered
