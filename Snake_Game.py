from random import randint
import pygame
from typing import Optional, Tuple, List

# Инициализация Pygame
pygame.init()

# Параметры экрана и сетки
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
NUM_CELLS_X = WIDTH // CELL_SIZE
NUM_CELLS_Y = HEIGHT // CELL_SIZE

# Направления движения
MOVEMENTS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# Цвета
BG_COLOR = (0, 0, 0)
CELL_BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость змейки
SNAKE_SPEED = 10

# Настройка игрового окна
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
game_clock = pygame.time.Clock()


class GameEntity:
    """Базовый класс для игровых объектов"""

    def __init__(self, pos: Optional[Tuple[int, int]] = None, color: Optional[Tuple[int, int, int]] = None) -> None:
        """Инициализация объекта на игровом поле."""
        self.position = pos or (WIDTH // 2, HEIGHT // 2)
        self.color = color or (255, 255, 255)

    def render(self, surface: pygame.Surface) -> None:
        """Метод для отрисовки объекта."""
        pass

    def render_cell(self, surface: pygame.Surface, pos: Tuple[int, int], color: Optional[Tuple[int, int, int]] = None) -> None:
        """Отрисовка ячейки на экране."""
        rect = pygame.Rect(pos, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, color or self.color, rect)
        pygame.draw.rect(surface, CELL_BORDER_COLOR, rect, 1)


class Apple(GameEntity):
    """Класс для яблока"""

    def __init__(self) -> None:
        """Инициализация яблока на поле."""
        super().__init__(None, APPLE_COLOR)
        self.random_position()

    def random_position(self) -> None:
        """Установка случайной позиции для яблока."""
        self.position = (randint(0, NUM_CELLS_X - 1) * CELL_SIZE,
                         randint(0, NUM_CELLS_Y - 1) * CELL_SIZE)

    def render(self, surface: pygame.Surface) -> None:
        """Отрисовка яблока на экране."""
        self.render_cell(surface, self.position)


class Snake(GameEntity):
    """Класс для змейки"""

    def __init__(self) -> None:
        """Инициализация змейки на старте игры."""
        super().__init__((NUM_CELLS_X // 2 * CELL_SIZE, NUM_CELLS_Y // 2 * CELL_SIZE), SNAKE_COLOR)
        self.length = 2
        self.body: List[Tuple[int, int]] = [self.position]
        self.direction = MOVEMENTS["RIGHT"]
        self.pending_direction: Optional[Tuple[int, int]] = None

    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """Изменяет направление движения змейки."""
        if new_direction != (self.direction[0] * -1, self.direction[1] * -1):
            self.pending_direction = new_direction

    def move(self) -> None:
        """
        Обновляет позицию змейки, добавляя новый сегмент на голову
        и удаляя хвост, если длина не увеличилась.
        """
        if self.pending_direction:
            self.direction = self.pending_direction
            self.pending_direction = None

        head_x, head_y = self.body[0]
        move_x, move_y = self.direction
        new_head = ((head_x + move_x * CELL_SIZE) % WIDTH,
                    (head_y + move_y * CELL_SIZE) % HEIGHT)

        # Проверка на столкновение с телом змейки
        if len(self.body) > 2 and new_head in self.body[2:]:
            self.reset()
        else:
            self.body.insert(0, new_head)
            if len(self.body) > self.length:
                self.body.pop()

    def render(self, surface: pygame.Surface) -> None:
        """Отрисовка змейки на экране."""
        for segment in self.body[:-1]:
            self.render_cell(surface, segment)

        head_position = self.body[0]
        self.render_cell(surface, head_position, SNAKE_COLOR)

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.body[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 2
        self.body = [self.position]
        self.direction = MOVEMENTS["RIGHT"]
        self.pending_direction = None


def process_input(snake: Snake) -> None:
    """Обработка нажатий клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(MOVEMENTS["UP"])
            elif event.key == pygame.K_DOWN:
                snake.change_direction(MOVEMENTS["DOWN"])
            elif event.key == pygame.K_LEFT:
                snake.change_direction(MOVEMENTS["LEFT"])
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(MOVEMENTS["RIGHT"])


def game_loop() -> None:
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        game_clock.tick(SNAKE_SPEED)

        process_input(snake)
        snake.move()

        # Проверка на съедание яблока
        if snake.get_head_position() == apple.position:
            print(snake.length)
            snake.length += 1

            # Добавляем новый сегмент в тело змейки
            snake.body.append(snake.body[-1])  # Добавляем новый сегмент в конец тела змейки
            apple.random_position()

        window.fill(BG_COLOR)
        snake.render(window)
        apple.render(window)

        pygame.display.update()


if __name__ == '__main__':
    game_loop()
