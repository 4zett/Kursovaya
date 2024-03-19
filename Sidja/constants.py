from Sidja.point import Point
from Sidja.enums import CheckerType, SideType

# Сторона за которую играет игрок
PLAYER_SIDE = SideType.WHITE

# Размер поля
X_SIZE = Y_SIZE = 5
# Размер ячейки (в пикселях)
CELL_SIZE = 75

# Ширина рамки (Желательно должна быть чётной)
BORDER_WIDTH = 2 * 2

# Цвета игровой доски
FIELD_COLORS = ['#0D0D0D', '#A2A2A2']
# Цвет рамки при наведении на ячейку мышкой
HOVER_BORDER_COLOR = '#1AFF00'
# Цвет рамки при выделении ячейки
SELECT_BORDER_COLOR = '#0015FF'
# Цвет кружков возможных ходов
POSIBLE_MOVE_CIRCLE_COLOR = '#FF00E2'

# Возможные смещения ходов шашек
MOVE_OFFSETS = [
    Point(1, 0),  # Вправо
    Point(-1, 0), # Влево
    Point(0, 1),  # Вниз
    Point(0, -1)  # Вверх
]

# Массивы типов белых и чёрных шашек [Обычная пешка]
WHITE_CHECKERS = [CheckerType.WHITE_REGULAR]
BLACK_CHECKERS = [CheckerType.BLACK_REGULAR]