from tkinter import Canvas, Event, messagebox
from PIL import Image, ImageTk
import random
from pathlib import Path
from math import inf
from typing import Tuple

from Sidja.field import Field
from Sidja.move import Move
from Sidja.constants import *
from Sidja.enums import CheckerType, SideType

class Game:
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int):
        self.__canvas = canvas
        self.__field = Field(x_field_size, y_field_size)
        self.__player_turn = True
        self.__hovered_cell = Point()
        self.__selected_cell = Point(-1, -1)
        self.__white_score = 0  # Инициализация счета для белых
        self.__black_score = 0  # Инициализация счета для черных
        self.__init_images()
        self.__draw()
        # Если игрок играет за чёрных, то совершить ход противника
        if PLAYER_SIDE == SideType.BLACK:
            self.__handle_enemy_turn()

    def __init_images(self):
        '''Инициализация изображений'''
        self.__images = {
            CheckerType.WHITE_REGULAR: ImageTk.PhotoImage(Image.open(Path('assets', 'white.png')).resize((CELL_SIZE, CELL_SIZE), Image.Resampling.LANCZOS)),
            CheckerType.BLACK_REGULAR: ImageTk.PhotoImage(Image.open(Path('assets', 'black.png')).resize((CELL_SIZE, CELL_SIZE), Image.Resampling.LANCZOS)),
        }

    def __draw(self):
        '''Отрисовка сетки поля и шашек'''
        self.__canvas.delete('all')
        self.__draw_field_grid()
        self.__draw_checkers()

    def __draw_field_grid(self):
        '''Отрисовка сетки поля'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                self.__canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE, fill=FIELD_COLORS[(y + x) % 2], width=0, tag='boards')
                if self.__selected_cell is not None and x == self.__selected_cell.x and y == self.__selected_cell.y:
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2, x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, outline=SELECT_BORDER_COLOR, width=BORDER_WIDTH, tag='border')
                elif (x == self.__hovered_cell.x and y == self.__hovered_cell.y):
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2, x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2, outline=HOVER_BORDER_COLOR, width=BORDER_WIDTH, tag='border')

                # Отрисовка возможных точек перемещения, если есть выбранная ячейка
                if (self.__selected_cell):
                    player_moves_list = self.__get_moves_list(PLAYER_SIDE)
                    for move in player_moves_list:
                        if (self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y):
                            self.__canvas.create_oval(move.to_x * CELL_SIZE + CELL_SIZE / 3, move.to_y * CELL_SIZE + CELL_SIZE / 3, move.to_x * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3), move.to_y * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3), fill=POSIBLE_MOVE_CIRCLE_COLOR, width=0, tag='posible_move_circle')

    def __draw_checkers(self):
        '''Отрисовка шашек'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Не отрисовывать пустые ячейки
                if (self.__field.type_at(x, y) != CheckerType.NONE):
                    self.__canvas.create_image(x * CELL_SIZE, y * CELL_SIZE, image=self.__images.get(self.__field.type_at(x, y)), anchor='nw', tag='checkers')

    def mouse_move(self, event: Event):
        '''Событие перемещения мышки'''
        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE
        if (x != self.__hovered_cell.x or y != self.__hovered_cell.y):
            self.__hovered_cell = Point(x, y)

            # Если ход игрока, то перерисовать
            if (self.__player_turn):
                self.__draw()

    def mouse_down(self, event: Event):
        '''Событие нажатия мышки'''
        if not (self.__player_turn): return

        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE

        # Если точка не внутри поля
        if not (self.__field.is_within(x, y)): return

        if (PLAYER_SIDE == SideType.WHITE):
            player_checkers = WHITE_CHECKERS
        elif (PLAYER_SIDE == SideType.BLACK):
            player_checkers = BLACK_CHECKERS
        else: return

        # Если нажатие по шашке игрока, то выбрать её
        if (self.__field.type_at(x, y) in player_checkers):
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif (self.__player_turn):
            try:
                move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)

                # Если нажатие по ячейке, на которую можно походить
                if (move in self.__get_moves_list(PLAYER_SIDE)):
                    if self.__field.type_at(x, y) == CheckerType.NONE and move in self.__get_moves_list(PLAYER_SIDE):
                        self.__handle_player_turn(move)
                else:
                    # Если не ход игрока, то ход противника
                    if not (self.__player_turn):
                        self.__handle_enemy_turn()
            except:
                pass

    def __handle_move(self, move: Move, draw: bool = True) -> bool:
        """Совершение хода и проверка на захват шашек без перемещения"""
        # Сохраняем тип шашки до перемещения
        moving_checker_type = self.__field.type_at(move.from_x, move.from_y)

        # Перемещаем шашку
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.NONE)
        self.__field.at(move.to_x, move.to_y).change_type(moving_checker_type)

        # Проверяем возможность захвата без фактического перемещения шашки игрока
        captured = self.__check_capture(move.to_x, move.to_y, moving_checker_type)

        if draw:
            self.__draw()

        return captured

    def __check_capture(self, x, y, player_type) -> bool:
        """Проверка на захват и выполнение захвата по вертикали и горизонтали."""
        captured = False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Ограничиваем направления проверки

        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            if self.__field.is_within(next_x, next_y):
                if self.__field.type_at(next_x, next_y) != player_type and self.__field.type_at(next_x,
                                                                                                next_y) != CheckerType.NONE:
                    # Если шашка противника находится рядом, проверяем, можно ли её "съесть"
                    opposite_x, opposite_y = next_x + dx, next_y + dy
                    if self.__field.is_within(opposite_x, opposite_y) and self.__field.type_at(opposite_x,
                                                                                               opposite_y) == player_type:
                        # Захватываем шашку противника
                        self.__field.at(next_x, next_y).change_type(CheckerType.NONE)
                        captured = True
        return captured

    def __get_next_capture_move(self, x: int, y: int) -> Move:
        '''Находит следующий возможный захват для шашки'''
        player_type = self.__field.type_at(x, y)
        enemy_type = CheckerType.WHITE_REGULAR if player_type == CheckerType.BLACK_REGULAR else CheckerType.BLACK_REGULAR

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x = x + dx * 2
            next_y = y + dy * 2
            between_x = x + dx
            between_y = y + dy

            if (self.__field.is_within(next_x, next_y) and
                    self.__field.type_at(between_x, between_y) == enemy_type and
                    self.__field.type_at(next_x, next_y) == CheckerType.NONE):
                return Move(x, y, next_x, next_y)

        return None

    def __handle_player_turn(self, move: Move):
        '''Обработка хода игрока и возможность продолжения хода'''
        self.__player_turn = False

        # Проверка наличия захвата после выполнения хода игрока
        captured = self.__handle_move(move)

        # Если после хода игрока не было захвата, передать ход компьютеру
        if not captured:
            self.__handle_enemy_turn()  # Передача хода компьютеру

        # Проверка на возможность продолжения хода в случае захвата
        while captured and self.__can_capture_again(move.to_x, move.to_y):
            self.__draw()  # Обновление доски
            move = self.__get_next_capture_move(move.to_x, move.to_y)
            captured = self.__handle_move(move)

        self.__player_turn = True
        self.__check_for_game_over()
        self.__selected_cell = None

    def __handle_enemy_turn(self):
        """Определение и выполнение хода компьютера."""
        enemy_side = SideType.opposite(PLAYER_SIDE)
        optimal_moves = self.__predict_optimal_moves(enemy_side)

        if optimal_moves:
            chosen_move = random.choice(optimal_moves)  # Выбираем случайный из оптимальных ходов
            captured = self.__handle_move(chosen_move)
            # Проверка на возможность повторного захвата
            while captured and self.__can_capture_again(chosen_move.to_x, chosen_move.to_y):
                next_move = self.__get_next_capture_move(chosen_move.to_x, chosen_move.to_y)
                if next_move:
                    chosen_move = next_move
                    captured = self.__handle_move(chosen_move)
        self.__player_turn = True
        self.__check_for_game_over()

    def __predict_optimal_moves(self, side: SideType) -> list[Move]:
        '''Предсказать оптимальный ход для заданной стороны.'''
        optimal_moves = []
        best_score_diff = -inf

        # Получаем список всех возможных ходов для заданной стороны
        possible_moves = self.__get_moves_list(side)

        for move in possible_moves:
            # Создаем копию доски для тестирования хода
            board_copy = Field.copy(self.__field)

            # Выполняем ход на копии доски
            self.__handle_move(move, draw=False)

            # Оцениваем результат хода
            white_score, black_score = self.__check_lines()
            score_diff = white_score - black_score if side == SideType.WHITE else black_score - white_score

            # Восстанавливаем исходное состояние доски
            self.__field = board_copy

            # Обновляем список оптимальных ходов
            if score_diff > best_score_diff:
                best_score_diff = score_diff
                optimal_moves = [move]
            elif score_diff == best_score_diff:
                optimal_moves.append(move)

        return optimal_moves

    def __can_capture_again(self, x, y) -> bool:
        '''Проверяет, может ли шашка на заданных координатах выполнить еще один захват.'''
        player_type = self.__field.type_at(x, y)
        enemy_type = CheckerType.WHITE_REGULAR if player_type == CheckerType.BLACK_REGULAR else CheckerType.BLACK_REGULAR

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            capture_x = x + dx * 2
            capture_y = y + dy * 2
            between_x = x + dx
            between_y = y + dy

            # Проверяем, что по направлению хода есть шашка противника и пустое поле для захвата
            if (self.__field.is_within(capture_x, capture_y) and
                    self.__field.type_at(between_x, between_y) == enemy_type and
                    self.__field.type_at(capture_x, capture_y) == CheckerType.NONE):
                return True

        return False

    def __check_for_game_over(self):
        '''Проверка на конец игры'''
        game_over = False

        white_moves_list = self.__get_moves_list(SideType.WHITE)
        if not (white_moves_list):
            # Белые проиграли
            answer = messagebox.showinfo('Конец игры', 'Чёрные выиграли')
            game_over = True

        black_moves_list = self.__get_moves_list(SideType.BLACK)
        if not (black_moves_list):
            # Чёрные проиграли
            answer = messagebox.showinfo('Конец игры', 'Белые выиграли')
            game_over = True

        if (game_over):
            # Новая игра
            self.__init__(self.__canvas, self.__field.x_size, self.__field.y_size)

    def __check_lines(self) -> Tuple[int, int]:
        '''Проверка наличия линий из шашек и начисление очков'''
        white_score = 0
        black_score = 0

        # Проверка горизонтальных линий
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size - 1):
                if self.__field.type_at(x, y) == CheckerType.WHITE_REGULAR and self.__field.type_at(x+1, y) == CheckerType.WHITE_REGULAR:
                    self.__field.at(x, y).change_type(CheckerType.NONE)
                    self.__field.at(x+1, y).change_type(CheckerType.NONE)
                    white_score += 1
                elif self.__field.type_at(x, y) == CheckerType.BLACK_REGULAR and self.__field.type_at(x+1, y) == CheckerType.BLACK_REGULAR:
                    self.__field.at(x, y).change_type(CheckerType.NONE)
                    self.__field.at(x+1, y).change_type(CheckerType.NONE)
                    black_score += 1

        # Проверка вертикальных линий
        for x in range(self.__field.x_size):
            for y in range(self.__field.y_size - 1):
                if self.__field.type_at(x, y) == CheckerType.WHITE_REGULAR and self.__field.type_at(x, y+1) == CheckerType.WHITE_REGULAR:
                    self.__field.at(x, y).change_type(CheckerType.NONE)
                    self.__field.at(x, y+1).change_type(CheckerType.NONE)
                    white_score += 1
                elif self.__field.type_at(x, y) == CheckerType.BLACK_REGULAR and self.__field.type_at(x, y+1) == CheckerType.BLACK_REGULAR:
                    self.__field.at(x, y).change_type(CheckerType.NONE)
                    self.__field.at(x, y+1).change_type(CheckerType.NONE)
                    black_score += 1


        return white_score, black_score

    def __get_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка ходов'''
        moves_list = self.__get_required_moves_list(side)
        if not (moves_list):
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка обязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
            enemy_checkers = BLACK_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
            enemy_checkers = WHITE_CHECKERS
        else:
            return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Для обычной шашки
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        new_x, new_y = x , y
                        # Проверяем только вертикальные и горизонтальные ходы
                        if self.__field.is_within(new_x, new_y):
                            # Проверяем, что клетка, куда мы хотим сделать ход, пуста
                            if self.__field.type_at(new_x, new_y) == CheckerType.NONE:
                                moves_list.append(Move(x, y, new_x, new_y))

        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка необязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
        else:
            return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Для обычной шашки
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        new_x, new_y = x + offset.x, y + offset.y
                        # Проверяем только вертикальные и горизонтальные ходы
                        if self.__field.is_within(new_x, new_y):
                            # Проверяем, что клетка, куда мы хотим сделать ход, пуста
                            if self.__field.type_at(new_x, new_y) == CheckerType.NONE:
                                moves_list.append(Move(x, y, new_x, new_y))

        return moves_list