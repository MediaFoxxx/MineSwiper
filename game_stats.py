import os.path


class GameStats:
    """Отслеживание статистики дял игры English Game."""

    def __init__(self, eg_game):
        """Инициализирует статистику."""
        self.settings = eg_game.settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии.
        self.game_active = False
        # self.question_active = False

        # Рекорд не должен сбрасываться.
        # self.high_score = 0
        # self._set_high_score()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.mines_left = self.settings.mines_limit

    def _set_high_score(self):
        """Устанавливаем максимальный результат из файла."""
        if os.path.exists('data/high_score.txt'):
            with open("data/high_score.txt") as f:
                for line in f:
                    self.high_score = int(line)
