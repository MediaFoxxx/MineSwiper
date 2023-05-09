import pygame
from pygame.sprite import Sprite


class Cells(Sprite):
    """Класс для управления ячейками."""

    def __init__(self, eg_game):
        """Инициализирует ячейку и задает ее начальную позицию."""
        super().__init__()
        self.screen = eg_game.screen
        self.settings = eg_game.settings

        # Игровые параметры ячейки
        self.is_mined = 0
        self.num_mines = 0
        self.is_shown = False
        self.is_marked = False

        # Каждая новая ячейка появляется в левом верхнем углу экрана.
        self.rect = pygame.Rect(0, 0, self.settings.cell_width, self.settings.cell_height)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Настройки шрифта для вывода цифры.
        self.text_color = (0, 0, 0)  # (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    def draw_cell(self, color):
        """Размещение ячейки на экране."""
        self.screen.fill(color, self.rect)
        if self.is_shown or self.is_marked:
            self.show_score()

    def prep_info(self):
        """Отрисовка информации на открытой ячейке."""
        if self.is_marked:
            info_str = 'F'
        elif self.is_mined == 1:
            info_str = '*'
        else:
            info_str = str(self.num_mines)
        self.info_image = self.font.render(info_str, True, self.text_color, self.settings.cell_color)

        # Вывод счета ниже кнопки Play.
        self.info_rect = self.info_image.get_rect()
        self.info_rect.center = self.rect.center

    def show_score(self):
        """Вывод кол-ва мин во время игры."""
        self.prep_info()
        self.screen.blit(self.info_image, self.info_rect)
