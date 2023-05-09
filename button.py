import pygame.font


class Button:

    def __init__(self, eg_game, params, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = eg_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров кнопок.
        self.width, self.height = params["width"], params["height"]
        self.button_color = params["button_c"]
        self.text_color = params["text_c"]
        self.font = pygame.font.SysFont(params["font_name"], params["font_size"])

        # Построение объекта rect кнопки и выранивание по центру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = params["centery"]

        # Сообщение кнопки создает только один раз.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Отображение пустой кнопки и вывод сообщения."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
