import pygame


class Shell(pygame.sprite.Sprite):

    def __init__(self, arr_group, arr_param):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(arr_group)

        # Расположение и размеры
        x, y, r, direction, v = arr_param

        self.x_delta = 0
        self.y_delta = 0
        self.y_v = v / 1000   # Скорость 50 пикселей в секунду по вертикали

        # Скорость 50 пикселей в секунду по горизонтали
        if (direction == 'left'):
            self.x_v = -250 / 1000
        else:
            self.x_v = 250 / 1000

        # Создаём холст
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA, 32)   # Обязательные аргументы: размер
        pygame.draw.circle(self.image, pygame.Color("red"), (r, r), r)
        self.rect = pygame.Rect(0, 0, r * 2, r * 2)

        # Позиционируем элемент (по умолчанию - (0, 0))
        self.rect.x = x
        self.rect.y = y

        # вычисляем маску для эффективного сравнения
#        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        # Полёт снаряда
        self.x_delta += delta_time * self.x_v
        self.y_delta -= delta_time * self.y_v

        self.rect = self.rect.move(round(self.x_delta), round(self.y_delta))

        self.x_delta -= round(self.x_delta)
        self.y_delta -= round(self.y_delta)

        # Проверяем на вылет из поля
        if (self.rect.y < 0):
            self.kill()

