import time

import numpy as np
import pygame
import sys

from empty_cell import Cells
# from opened_cells import OpenedCells
from settings import Settings
from minesscore import MinesScore
from game_stats import GameStats
from button import Button
# from questions import Question
from main import Field


class MineSwiper:
    """Класс для управления поведением и ресурсами игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # Создание экрана игры.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Mine_Swiper")

        # Создание экземляра для хранения игровой статистики
        # и статистики результатов.
        self.stats = GameStats(self)
        self.ms = MinesScore(self)

        self.cells = pygame.sprite.Group()
        self.opened_cells = pygame.sprite.Group()
        self._create_grid_of_cells()

        # Создание кнопки PLay и кнопки выхода из уровня
        self.play_button = Button(self, self.settings.start_button, "Play")
        self.quit_level_button = Button(self, self.settings.start_button, "Quit level")
        self.quit_level_button.rect.bottom = 70   # 8 * (self.settings.cell_height + self.settings.cell_indent)
        self.quit_level_button.msg_image_rect.centery = self.quit_level_button.rect.centery

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            if self.stats.mines_left == 0:
                # self.sb.first_game = False
                # self.questions = Question(self)
                self.stats.game_active = False

            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.stats.game_active:
                    self._check_play_button(mouse_pos)
                else:
                    self._check_cells_button(mouse_pos)
                    # self._check_answer_buttons(mouse_pos)
                    self._check_quit_level_button(mouse_pos)

    def _quit_game(self):
        """Завершение игры и сохранение результатов."""

        # with open("data/high_score.txt", 'w') as f:
        #     f.write(str(self.stats.high_score))

        sys.exit()

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            self._quit_game()

    def _start_game(self):
        """Запускает новую игру при нажатии P или кнопки Play."""
        if not self.stats.game_active:
            # Создание поля
            self.field = Field(self.settings.x_cells, self.settings.y_cells, self.settings.mines_limit)

            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            # self.stats.question_active = False

            # Очистка всех ячеек.
            self.cells.empty()
            self.opened_cells.empty()

            # Создание ячеек с вопросами.
            self._create_grid_of_cells()

    def _set_first_mines(self, cur_cell):
        """Задание мин на начальном поле."""
        self._get_neighbors(cur_cell)
        neighs = [convert(cell.rect[0], cell.rect[1]) for cell in cur_cell.neighbors.copy()]
        neighs = [x + y * self.settings.x_cells for x, y in neighs]
        x, y = convert(cur_cell.rect[0], cur_cell.rect[1])
        neighs.append(x + y * self.settings.x_cells)

        field_arr = np.zeros((self.settings.x_cells * self.settings.y_cells - len(neighs)), dtype=int)

        for i in range(self.settings.mines_limit):
            field_arr[i] = 1
        np.random.shuffle(field_arr)

        for xy in sorted(neighs):
            field_arr = np.insert(field_arr, xy, 0)

        for num, cell in enumerate(self.cells):
            cell.is_mined = field_arr[num]

        for cell in self.cells:
            self._get_neighbors(cell)

            for neigh_cell in cell.neighbors:
                cell.num_mines += neigh_cell.is_mined

    def _get_neighbors(self, cell):
        """Нахождение соседей клетки."""
        cell_x, cell_y = convert(cell.rect[0], cell.rect[1])
        cell.neighbors = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == y == 0:
                    continue
                if cell_x + x in range(0, self.settings.x_cells) and cell_y + y in range(0, self.settings.y_cells):
                    xy = cell_x + x + (cell_y + y) * self.settings.x_cells
                    if not self.cells.sprites()[xy].is_shown:
                        cell.neighbors.append(self.cells.sprites()[xy])

    def _check_cells_button(self, mouse_pos):
        """Проверка нажатия на ячейку с вопросом."""
        for cell in self.cells:
            if cell.rect.collidepoint(mouse_pos):

                if self.stats.first_step:
                    self._set_first_mines(cell)
                    self.stats.first_step = False
                    # break

                if not cell.is_shown:
                    self._create_opened_cell(cell)
                if cell.num_mines == 0:
                    self._reveal(cell)

                # self.cells.remove(cell)
                # self.questions.get_new_question()
                break

    def _reveal(self, cell):
        """Открытие пустых ячеек."""
        cell.is_shown = True

        for nei_cell in cell.neighbors:

            if nei_cell.num_mines == 0 and not nei_cell.is_shown:
                nei_cell.is_shown = True
                self._reveal(nei_cell)
            else:
                nei_cell.is_shown = True


    # def _check_answer_buttons(self, mouse_pos):
    #     """Проверка нажатия на кноку ответа на вопрос."""
    #     if self.stats.question_active:
    #         count = 0
    #         for answer in self.questions.answers:
    #             if answer.rect.collidepoint(mouse_pos):
    #                 answer_keys = list(self.questions.answer.keys())
    #                 self.stats.score += self.questions.answer[answer_keys[count]]
    #                 self.stats.question_active = False
    #                 self.stats.questions_left -= 1
    #
    #                 break
    #             count += 1

    def _check_quit_level_button(self, mouse_pos):
        """Проверка нажатия на кнопку выхода из уровня."""
        if self.quit_level_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = False
            # self.sb.first_game = False

    def _create_grid_of_cells(self):
        """Создание ячеек для вопросов."""
        for row_number in range(self.settings.y_cells):
            for cell_number in range(self.settings.x_cells):
                self._create_cell(cell_number, row_number)

    def _create_cell(self, cell_number, row_number):
        """Создание ячейки и размещение ее в ряду."""
        cell = Cells(self)
        cell_width, cell_height = cell.rect.size
        cell.rect.x = self.settings.cell_indent * (1 + cell_number) + cell_number * cell_width + 160
        cell.rect.y = self.settings.cell_indent * (1 + row_number) + row_number * cell_height + 300
        self.cells.add(cell)

    def _create_opened_cell(self, cell):
        """Создание пустой ячейки и размещение ее в ряду."""
        # opened_cell = OpenedCells(self)
        # opened_cell.rect.x = cell.rect.x
        # opened_cell.rect.y = cell.rect.y
        # self.opened_cells.add(opened_cell)
        cell.is_shown = True

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            # self.ms.show_stats()
        else:
            for cell in self.cells.sprites():
                cell.draw_cell(self.settings.cell_color)

            for opened_cell in self.opened_cells.sprites():
                opened_cell.draw_cell(self.settings.opened_cell_color)

            # if self.stats.question_active:
            #     self.questions.draw_question()

            self.ms.show_score()
            self.quit_level_button.draw_button()

        pygame.display.flip()


def convert(x, y, forw=True):
    if forw:
        new_x = int((x - 170) / 50)
        new_y = int((y - 310) / 50)

        return new_x, new_y
    else:
        new_x = x * 50 + 170
        new_y = y * 50 + 310

        return new_x + new_y


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    eg = MineSwiper()
    eg.run_game()
