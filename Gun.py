import os
import sys
import pygame


class Gun(pygame.sprite.Sprite):

    def __init__(self, arr_group, arr_param):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(arr_group)

        # Расположение и размеры
        self.main_width, self.main_height, file_image, file_boox, self.ammo = arr_param
        self.downed_plane = 0
        self.is_boox = False

        self.recharge = 2000     # Перезарядка пушки - 2 сек
        self.recharge_time = 2000

        # Загружаем изображение
        self.direction = 'left'

        self.image = self.load_image(file_image, -1, self.direction)
        self.rect = self.image.get_rect()

        # Позиционируем элемент (по умолчанию - (0, 0))
        self.rect.x = (self.main_width - self.rect.width) // 7 * 6
        self.rect.y = self.main_height - self.rect.height - 5

        fullname = os.path.join('data', file_boox)
        self.sound1 = pygame.mixer.Sound(fullname)

        # вычисляем маску для эффективного сравнения
#        self.mask = pygame.mask.from_surface(self.image)

    def get_text(self):
        str1 = 'Снарядов - ' + str(self.ammo) + '   Сбито - ' + str(self.downed_plane)
        if (self.recharge_time < self.recharge):
            str1 += '      ПЕРЕЗАРЯДКА'
        else:
            str1 += '      ГОТОВ'

        font = pygame.font.Font(None, 20)

        text = font.render(str1, 1, pygame.Color('red'))
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = self.main_height - text_rect.height - 5

        return (text, text_rect)


    # Выстрел
    def my_shell(self):
        if (self.recharge_time < self.recharge):
            return (0, 0, 'Pause')
        else:
            if (self.ammo > 0) and (not self.is_boox):
                self.recharge_time = 0    # Сбрасываем время перезарядки

                if (self.direction == 'left'):
                    x = self.rect.x + 8
                    y = self.rect.y - 5
                else:
                    x = self.rect.x + 58
                    y = self.rect.y - 5

                self.ammo -= 1
                self.sound1.play()

                return (x, y, self.direction)
            else:
                return (0, 0, None)


    def my_left(self, delta):
        if (not self.is_boox):
            self.rect.x -= delta
            if (self.rect.x < 10):
                self.rect.x = 10

    def my_right(self, delta):
        if (not self.is_boox):
            self.rect.x += delta
            if (self.rect.x > self.main_width - self.rect.width - 10):
                self.rect.x = self.main_width - self.rect.width - 10

    def my_rotate(self):
        if (not self.is_boox):
            if (self.direction == 'left'):
                self.direction = 'right'
            else:
                self.direction = 'left'

            self.image = pygame.transform.flip(self.image, True, False)  # Разворот


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

        image = pygame.transform.rotate(image, 15)     # Поворот

        if (direction == 'left'):
            image = pygame.transform.flip(image, True, False)     # Разворот

        return image

    def update(self, delta_time):
        self.recharge_time += delta_time