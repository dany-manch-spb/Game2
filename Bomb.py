import os
import sys
import pygame


class Bomb(pygame.sprite.Sprite):

    def __init__(self, arr_group, arr_param):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(arr_group)

        # Расположение и размеры
        self.main_height, x, y, file_image, file_image_boox, file_boox, x_v, y_v, x_direction,\
        self.land_group, self.gun_group = arr_param

        self.x_delta = 0
        self.y_delta = 0
        self.x_v = x_v / 1000  # Скорость: пикселей в секунду по горизонтали
        self.y_v = y_v / 1000  # Скорость: пикселей в секунду по вертикали
        self.is_boox = False
        self.boox_timer = 0
        self.max_boox_timer = 500

        if (x_direction == 'left'):
            self.x_v = -self.x_v

        # Загружаем изображение
        self.image = self.load_image(file_image, -1, x_direction)
        self.image_boox = self.load_image(file_image_boox, -1, None)
        self.rect = self.image.get_rect()

        # Позиционируем элемент (по умолчанию - (0, 0))
        self.rect.x = x
        self.rect.y = y

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

#        image = pygame.transform.rotate(image, -20)     # Поворот

        # Подгоняем под размер
        rect = image.get_rect()
        image = pygame.transform.scale(image, (rect.width // 4, rect.height // 4))

        if (direction == 'right'):
            image = pygame.transform.flip(image, True, False)     # Разворот

        return image

    def boox(self, dx, dy):
        self.is_boox = True
        rect = self.image_boox.get_rect()
        self.image = pygame.transform.scale(self.image_boox, (rect.width // 2, rect.height // 2))

        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy

        self.sound_boox.play()

    def update(self, delta_time):
        if (not self.is_boox):
            # Полёт бомбы
            self.x_delta += delta_time * self.x_v
            self.y_delta += delta_time * self.y_v

            self.rect = self.rect.move(round(self.x_delta), round(self.y_delta))

            self.x_delta -= round(self.x_delta)
            self.y_delta -= round(self.y_delta)

            # Проверяем на вылет из поля
            # (возвращает список спрайтов из группы, с которыми произошло пересечение)
            item = pygame.sprite.spritecollide(self, self.gun_group, False)
            if len(item) > 0:
                self.boox(-30, 30)
                item[0].is_boox = True
            elif pygame.sprite.spritecollide(self, self.land_group, False):
                self.boox(-30, -30)


        else:
            # Показываем взрыв сколько положено
            if (self.boox_timer >= self.max_boox_timer):
                self.kill()
            else:
                self.boox_timer += delta_time