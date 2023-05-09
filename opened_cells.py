import pygame
from pygame.sprite import Sprite


class OpenedCells(Sprite):
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

        # Настройки шрифта для вывода цифры.
        self.text_color = (0, 0, 0)  # (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    def draw_cell(self, color):
        """Размещение ячейки на экране."""
        self.screen.fill(color, self.rect)  # self.settings.cell_color
        self.show_score()

    def prep_info(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = str(0)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.opened_cell_color)

        # Вывод счета выше кноки Play.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.rect.center
        # self.score_rect.centery -= 50

    # def prep_high_score(self):
    #     """Преобразует рекордный счет в графическое изображение."""
    #     high_score_str = f"Your record: {self.stats.high_score}"
    #     self.high_score_image = self.font.render(high_score_str, True,
    #                                              self.text_color, self.settings.bg_color)
    #
    #     # Рекорд выводится выше предыдущего счета.
    #     self.high_score_image_rect = self.high_score_image.get_rect()
    #     self.high_score_image_rect.center = self.screen_rect.center
    #     self.high_score_image_rect.centery -= 90

    def show_stats(self):
        """Выводит очки, уровень и количество кораблей на экран."""

        # Подготовка изображений счетов.
        self.prep_info()

        self.screen.blit(self.score_image, self.score_rect)

    def show_score(self):
        """Вывод счета во время игры."""

        self.prep_info()
        self.screen.blit(self.score_image, self.score_rect)

        # self.score_rect.bottom = 3 * (self.settings.cell_indent + self.settings.cell_height)
        # self.screen.blit(self.score_image, self.score_rect)
