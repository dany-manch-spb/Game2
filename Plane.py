import os
import sys
import pygame
import random


class Plane(pygame.sprite.Sprite):

    def __init__(self, arr_group, arr_param):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(arr_group)

        # Расположение и размеры
        self.main_width, self.main_height, self.min_y, self.max_y, file_image, \
        file_image_boox, file_boox, x_v, y_v, self.shell_group, self.gun, self.plane_coef = arr_param

        self.x_delta = 0
        self.y_delta = 0
        self.x_v = x_v / 1000  # Скорость: пикселей в секунду по горизонтали
        self.y_v = y_v / 1000  # Скорость: пикселей в секунду по вертикали
        self.is_boox = False
        self.boox_timer = 0
        self.max_boox_timer = 500
        self.is_bomb = True

        # Загружаем изображение
        self.x_direction = 'right'
        self.y_direction = 'up'

        self.image = self.load_image(file_image, -1, self.x_direction)
        self.image_boox = self.load_image(file_image_boox, -1, None)
        self.rect = self.image.get_rect()

        # Позиционируем элемент (по умолчанию - (0, 0))
        self.rect.x = 0
        self.rect.y = random.randint(self.min_y, self.max_y)

        fullname = os.path.join('data', file_boox)
        self.sound_boox = pygame.mixer.Sound(fullname)

        # вычисляем маску для эффективного сравнения
#        self.mask = pygame.mask.from_surface(self.image)

    def load_image(self, name, colorkey=None, direction='left'):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname)

        # Обрезаем фон изображения
        # 1) Если при этом изображение уже прозрачно (это обычно бывает у картинок форматов png и gif),
        # то после загрузки вызываем функцию convert_alpha(), и загруженное изображение сохранит прозрачность.
        # 2) Если изображение было непрозрачным, то используем функцию Surface set_colorkey(colorkey),
        # и тогда переданный ей цвет станет прозрачным.
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)  # Если изображение не прозрачно
        else:
            image = image.convert_alpha()  # Если изображение прозрачно

        # Преобразуем изображение
        # image1 = pygame.transform.scale(image, (200, 100))
        # image2 = pygame.transform.scale(image, (100, 200))

        if (direction != None):
            image = pygame.transform.rotate(image, -20)     # Поворот

            # Уменьшаем размер самолёта (усложнение)
            rect = image.get_rect()
            image = pygame.transform.scale(image, (rect.width // 1.5 // self.plane_coef, rect.height // 1.5 // self.plane_coef))

        if (direction != None) and (direction == 'right'):
            image = pygame.transform.flip(image, True, False)     # Разворот

        return image

    def get_bomb(self, pos_gun):
        x = -1
        y = -1

        if (self.is_bomb) and (not self.is_boox):
            # Если до пушки не более 20 пикселей, то нужно отбомбиться
            delta = random.randint(20, 50)

            if (abs(pos_gun.x - self.rect.x) <= delta):
                self.is_bomb = False
                x = self.rect.x + self.rect.width // 2
                y = self.rect.y + self.rect.height

        return (x, y, self.x_direction)


    def update(self, delta_time):
        if (not self.is_boox):
            # Полёт самолёта
            self.x_delta += delta_time * self.x_v
            self.y_delta -= delta_time * self.y_v

            self.rect = self.rect.move(round(self.x_delta), round(self.y_delta))

            self.x_delta -= round(self.x_delta)
            self.y_delta -= round(self.y_delta)

            # Проверяем на выход за пределы экрана
            if (self.x_direction == 'right'):
                if (self.rect.x >= self.main_width - self.rect.width):
                    self.x_direction = 'left'
                    self.rect.x = self.main_width - self.rect.width
                    self.x_v = -self.x_v
                    self.is_bomb = True
                    self.image = pygame.transform.flip(self.image, True, False)  # Разворот
            else:
                if (self.rect.x <= 0):
                    self.x_direction = 'right'
                    self.rect.x = 0
                    self.x_v = -self.x_v
                    self.is_bomb = True
                    self.image = pygame.transform.flip(self.image, True, False)  # Разворот

            if (self.y_direction == 'up'):
                if (self.rect.y <= self.min_y):
                    self.y_direction = 'down'
                    self.rect.y = self.min_y
                    self.y_v = -self.y_v
            else:
                if (self.rect.y >= self.max_y):
                    self.y_direction = 'up'
                    self.rect.y = self.max_y
                    self.y_v = -self.y_v

            if pygame.sprite.spritecollide(self, self.shell_group, True):
                self.boox()

        else:
            # Показываем взрыв сколько положено
            if (self.boox_timer >= self.max_boox_timer):
                self.kill()
            else:
                self.boox_timer += delta_time

    def boox(self):
        self.is_boox = True
        rect = self.image_boox.get_rect()
        self.image = pygame.transform.scale(self.image_boox, (rect.width // 8, rect.height // 8))

        self.gun.downed_plane += 1

#        self.rect.y = self.rect.y - 30
#        self.rect.x = self.rect.x - 30

        self.sound_boox.play()
