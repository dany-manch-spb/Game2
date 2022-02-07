import pygame


class Land(pygame.sprite.Sprite):

    def __init__(self, arr_group, arr_param):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(arr_group)

        # Расположение и размеры
        x, y, width, height = arr_param

        # Создаём холст
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)   # Обязательные аргументы: размер
        # Рисуем на холсте
        self.rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, (200, 200, 200), self.rect)

        # Позиционируем элемент (по умолчанию - (0, 0))
        self.rect.x = x
        self.rect.y = y

        # вычисляем маску для эффективного сравнения
#        self.mask = pygame.mask.from_surface(self.image)

