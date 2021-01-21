import pygame
import copy
import math
import random
from pygame_button import Button

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)

BUTTON_STYLE = {
    "hover_color": BLACK,
    "clicked_color": GREEN,
    "clicked_font_color": BLACK,
    "hover_font_color": ORANGE,
}


# класс игры - жизнь, придуманная математиком Джоном Конвеем
class gameoflife(object):
    def __init__(self):
        # инициализация окна
        pygame.init()
        # задание название окна
        pygame.display.set_caption('игра жизнь')
        # задание размеров окна
        self.screen = pygame.display.set_mode((500, 700))
        # буфер в котором определяется жива клетка или нет (0 мертва, 1 жива)
        self.data = [[0 for j in range(50)] for i in range(50)]
        # переменная отвечающая за запуск программы
        self.run = True
        # переменная времени
        self.clock = pygame.time.Clock()
        # запуск игры
        self.start = False
        # переменная инициализации
        self.initial = True
        self.startButton = Button((0, 0, 100, 100), GREEN, self.set_start, text='Старт', **BUTTON_STYLE)
        self.randomButton = Button((0, 0, 100, 100), RED, self.set_random, text='Рандом',
                                   **BUTTON_STYLE)
        self.resetButton = Button((0, 0, 100, 100), BLUE, self.set_clear, text='Очистка',
                                  **BUTTON_STYLE)
        self.screen_rect = self.screen.get_rect()
        self.startButton.rect.center = (self.screen_rect.centerx + 100, 600)
        self.randomButton.rect.center = (self.screen_rect.centerx, 600)
        self.resetButton.rect.center = (self.screen_rect.centerx - 100, 600)

    def getData(self):
        return self.data

    def set_random(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = random.randint(0, 1)

    def set_start(self):
        # если запуск уже произведен, т.е. значение self.start = true, то меняем значение на false, иначе true
        if self.start:
            self.start = False
            self.initial = True
        else:
            self.start = True
            self.initial = False

    def set_clear(self):
        # передаем новый массив с нулям
        self.data = [[0 for j in range(50)] for i in range(50)]
        # выводим в консоль для отслеживания действий
        print("очистка поля")
        # указываем что игра заверщена в этот момент
        self.start = False
        # указываем что пользователь может расставлять клетки, эта переменная активирует действия в функции сверху
        self.initial = True

        # функция поиска соседей
    def get_neighbour(self, i, j):
        neighbour = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1], [i + 1, j + 1], [i - 1, j + 1], [i + 1, j - 1],
                     [i - 1, j - 1]]
        neighbour = [i for i in neighbour if 0 <= i[0] < 50 and 0 <= i[1] < 50]
        return neighbour

    # функция новой эволюции клетки
    def next_generation(self):
        # возвращаем прошлую версию массива
        self.last_generation = copy.deepcopy(self.data)
        # проходимся по массиву
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                # ищем количество соседних клеток
                self.count = [self.last_generation[k[0]][k[1]] for k in self.get_neighbour(i, j)].count(1)
                # в зависимости от количества соседних, оживляем
                if self.last_generation[i][j] == 1:
                    self.data[i][j] = 1 if self.count in range(2, 4) else 0
                elif self.last_generation[i][j] == 0:
                    self.data[i][j] = 1 if self.count == 3 else 0

    # обновление окна
    def update(self):
        # закрашивание окна черным
        self.screen.fill((0, 0, 0))
        # установка кнопок
        # вывод клеток
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == 1:
                    pygame.draw.rect(self.screen, ORANGE, (j * 10, i * 10, 10, 10))
        self.resetButton.update(self.screen)
        self.startButton.update(self.screen)
        self.randomButton.update(self.screen)

    # функция действий пользователя - расстановка клеток и удаление
    def user_initial(self):
        if self.initial:
            x, y = pygame.mouse.get_pos()
            # до 500 по Y расположено окно игры
            if y < 500:
                if pygame.mouse.get_pressed()[0]:
                    self.data[math.floor(y / 10)][math.floor(x / 10)] = 1
                if pygame.mouse.get_pressed()[2]:
                    self.data[math.floor(y / 10)][math.floor(x / 10)] = 0
            self.clock.tick(60)

    def event_loop(self):
        for event in pygame.event.get():
            # если окно закрыто, программа завершается
            if event.type == pygame.QUIT:
                self.run = False
            self.randomButton.check_event(event)
            self.resetButton.check_event(event)
            self.startButton.check_event(event)

    # функция запуска
    def start_game(self):
        while self.run:
            # обработка событий окна
            self.event_loop()
            # обновление объектов в окне
            self.update()
            # вызов функции в которой происходит расположение пользователем клеток, в случае initial = True
            self.user_initial()
            # если игра начата
            if self.start:
                # происходит вызов функции в которой происходит новое поколение клеток
                self.next_generation()
                # задержка(иначе будет все слишком быстро)
                self.clock.tick(10)
            # обновление окна
            pygame.display.update()


if __name__ == '__main__':
    # создаем объекты класса игры
    game = gameoflife()
    # вызываем функцию запуска игры
    game.start_game()
