import pygame.font


class MinesScore:
    """Класс для вывода игровой информации."""

    def __init__(self, eg_game):
        """Инициализируем атрибуты подсчета очков."""
        self.eg_game = eg_game
        self.screen = eg_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = eg_game.settings
        self.stats = eg_game.stats

        # self.first_game = True

        # Настройки шрифта для вывода счета.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

    def prep_images(self):
        """Функция подготовки изображений перед обновлением экрана."""
        self.prep_score()
        # self.prep_high_score()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = f"Your score: {self.stats.mines_left}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Вывод счета выше кноки Play.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.screen_rect.center
        self.score_rect.centery -= 50

    def show_score(self):
        """Вывод счета во время игры."""

        self.prep_score()
        self.score_rect.bottom = 3 * (self.settings.cell_indent + self.settings.cell_height)
        self.screen.blit(self.score_image, self.score_rect)
