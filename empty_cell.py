import pygame
from pygame.sprite import Sprite


class Cells(Sprite):
    """Класс для управления ячейками."""

    def __init__(self, eg_game):
        """Инициализирует ячейку и задает ее начальную позицию."""
        super().__init__()
        self.screen = eg_game.screen
        self.settings = eg_game.settings

        #
        self.is_mined = 0
        self.num_mines = 0
        self.is_shown = False

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
        if self.is_shown:
            self.show_score()

    def prep_info(self):
        """Преобразует текущий счет в графическое изображение."""
        if self.is_mined == 1:
            score_str = '*'
        else:
            score_str = str(self.num_mines)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.cell_color)

        # Вывод счета выше кноки Play.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.rect.center
        # self.score_rect.centery -= 50

    def show_score(self):
        """Вывод счета во время игры."""

        self.prep_info()
        self.screen.blit(self.score_image, self.score_rect)

        # self.score_rect.bottom = 3 * (self.settings.cell_indent + self.settings.cell_height)
        # self.screen.blit(self.score_image, self.score_rect)