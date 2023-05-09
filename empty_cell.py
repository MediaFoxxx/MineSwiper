import pygame
from pygame.sprite import Sprite


class Cells(Sprite):
    """Класс для управления ячейками."""

    def __init__(self, eg_game):
        """Инициализирует ячейку и задает ее начальную позицию."""
        super().__init__()
        self.screen = eg_game.screen
        self.settings = eg_game.settings

        # Каждая новая ячейка появляется в левом верхнем углу экрана.
        self.rect = pygame.Rect(0, 0, self.settings.cell_width, self.settings.cell_height)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def draw_cell(self, color):
        """Размещение ячейки на экране."""
        self.screen.fill(color, self.rect)
