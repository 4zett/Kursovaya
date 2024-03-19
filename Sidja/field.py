from Sidja.enums import CheckerType
from Sidja.checker import Checker
import random
from Sidja.constants import WHITE_CHECKERS, BLACK_CHECKERS

from functools import reduce

class Field:
    def __init__(self, x_size: int, y_size: int):
        self.__x_size = x_size
        self.__y_size = y_size
        self.generate()

    @property
    def x_size(self) -> int:
        return self.__x_size

    @property
    def y_size(self) -> int:
        return self.__y_size

    @property
    def size(self) -> int:
        return max(self.x_size, self.y_size)

    @classmethod
    def copy(cls, field_instance):
        '''Создаёт копию поля из образца'''
        field_copy = cls(field_instance.x_size, field_instance.y_size)

        for y in range(field_instance.y_size):
            for x in range(field_instance.x_size):
                field_copy.at(x, y).change_type(field_instance.type_at(x, y))

        return field_copy

    def generate(self):
        '''Генерация поля с шашками'''
        self.__checkers = [[Checker() for _ in range(self.x_size)] for _ in range(self.y_size)]

        # Заблокировать центральную клетку
        central_x = self.x_size // 2
        central_y = self.y_size // 2
        self.__checkers[central_y][central_x].change_type(CheckerType.BLOCKED)

        # Расставляем 12 черных шашек
        black_coordinates = set()  # Множество для хранения выбранных координат черных шашек
        black_count = 0
        while black_count < 12:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if (x, y) not in black_coordinates and self.__checkers[y][x].type == CheckerType.NONE:
                self.__checkers[y][x].change_type(CheckerType.BLACK_REGULAR)
                black_coordinates.add((x, y))  # Добавляем координаты в множество
                black_count += 1

        # Расставляем 12 белых шашек
        white_coordinates = set()  # Множество для хранения выбранных координат белых шашек
        white_count = 0
        while white_count < 12:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if (x, y) not in black_coordinates and (x, y) not in white_coordinates and self.__checkers[y][
                x].type == CheckerType.NONE:
                self.__checkers[y][x].change_type(CheckerType.WHITE_REGULAR)
                white_coordinates.add((x, y))  # Добавляем координаты в множество
                white_count += 1

        # Разблокировать центральную клетку
        self.__checkers[central_y][central_x].change_type(CheckerType.NONE)

    def type_at(self, x, y):
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            if self.__checkers[y][x] is not None:
                return self.__checkers[y][x].type
        return None

    def at(self, x: int, y: int) -> Checker:
        '''Получение шашки на поле по координатам'''
        if 0 <= x < self.x_size and 0 <= y < self.y_size:
            return self.__checkers[y][x]
        else:
            # Возвращаем пустую шашку за пределами поля
            return Checker()  # Или любое другое значение, указывающее на отсутствие шашки

    def is_within(self, x: int, y: int) -> bool:
        '''Определяет лежит ли точка в пределах поля'''
        return (0 <= x < self.x_size and 0 <= y < self.y_size)
