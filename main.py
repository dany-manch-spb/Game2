import os
import sys
import random
import pygame

from Land import Land
from Gun import Gun
from Shell import Shell
from Plane import Plane
from Bomb import Bomb


if __name__ == '__main__':

    # Считываем параметры из командной строки  file_map_name = sys.argv[1]
    sys_arg_count = len(sys.argv)    # кол-во самолётов, изменение размера самолёта, width, height
#    print('sys_arg_count =', sys_arg_count)
#    print('')

#    for value1 in sys.argv:
#        print(value1)

    # ---------------------------------
    # https://www.pygame.org/docs/ref/transform.html#pygame.transform
    # инициализация Pygame:
    pygame.init()

    # размеры окна:
    width = 1200
    if (sys_arg_count > 4):
        width = int(sys.argv[4])
    height = 800
    if (sys_arg_count > 5):
        height = int(sys.argv[5])

    size = width, height      # 1200, 800      1500, 1100
    screen = pygame.display.set_mode(size)

    # Заголовок окна
    pygame.display.set_caption('Игра "Зенитка"')
    # Первоначальная заливка формы
#    screen.fill(pygame.Color('white'))  # pygame.Color(255, 255, 255)
#    pygame.display.update()
#    pygame.display.flip()  # смена кадра

    pygame.mouse.set_visible(False)       # Скрываем курсор мышки

    # ---------------------------------
    # Отображаем  заставку
    # ---------------------------------
#    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    image = pygame.image.load('data/fon.jpg')
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (0, 0))
    # Переключаем экран
    pygame.display.flip()

    # Ждём 1 sec
    pygame.time.wait(1000)


    # ---------------------------------
    # Переменные
    # ---------------------------------
    fps = 60 # количество кадров в секунду
    clock1 = pygame.time.Clock()     # Timer
    # pygame.time.get_ticks() - количество миллисекунд с момента вызова pygame.init()
    # pygame.time.Clock().tick() - количество миллисекунд с момента предыдущего вызова - НЕ РАБОТАЕТ БЕЗ ПАРАМЕТРА

    # ---------------------------------
    # Создаём спрайты
    # ---------------------------------
    # создадим группу, содержащую все спрайты
    # основной персонаж
    gun = None
    gun_delta = 30
    shell_r = 5

    ammo = 50     # Количество снарядов
    if (sys_arg_count > 3):
        ammo = int(sys.argv[3])

    max_plane_count = 5     # Количество самолётов
    if (sys_arg_count > 1):
        max_plane_count = int(sys.argv[1])

    shell_v = 650     # Скорость снаряда: пикселей в секунду
    plane_vx = 200     # Скорость самолёта: пикселей в секунду по горизонтали
    plane_vy = 30      # Скорость самолёта: пикселей в секунду по вертикали

    plane_coef = 1     # Коэффициент уменьшения самолёта
    if (sys_arg_count > 2):
        plane_coef = float(sys.argv[2])

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    gun_group = pygame.sprite.Group()
    shell_group = pygame.sprite.Group()
    plane_group = pygame.sprite.Group()
    land_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()

    arr_plane = list()

    # Земля
    Land((all_sprites, land_group), (0, height - 30, width, 30))
    # Пушка
    gun = Gun((all_sprites, gun_group), (width, height, 'gun_64.png', 'gun_boox.mp3', ammo))

    #    all_sprites.draw(screen)

    # ---------------------------------
    # главный игровой цикл
    # ---------------------------------
    delta_time_plane = 0
    delta_time_plane_start = 1000
    plane_count = 0

    delta_time = 0
    running = True
    while running:
        # Цикл обработки событий
        for event in pygame.event.get():

            if (event.type == pygame.QUIT):               # Выход из игры
                running = False

            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):        # Перемещение пушки
                    if (event.mod & pygame.KMOD_CTRL):
                        gun.my_left(gun_delta * 4)
                    else:
                        gun.my_left(gun_delta)
                elif (event.key == pygame.K_RIGHT):     # Перемещение пушки
                    if (event.mod & pygame.KMOD_CTRL):
                        gun.my_right(gun_delta * 4)
                    else:
                        gun.my_right(gun_delta)

                elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN):  # Разворот пушки
                    gun.my_rotate()

                elif (event.key == pygame.K_SPACE):     # Выстрел
                    x, y, direction = gun.my_shell()
                    if (direction != None):
                        if (direction != 'Pause'):
                            Shell((all_sprites, shell_group), (x, y, shell_r, direction, shell_v))
                    else:
                        running = False     # Конец игры: снаряды закончились


            # обработка остальных событий
            # ...

        if ((gun.downed_plane > 0) and (gun.downed_plane >= len(arr_plane))):
            running = False  # Конец игры: все самолёты сбиты
        elif (gun.is_boox):
            running = False  # Конец игры: Пушка подбита

        # изменение игрового мира

        # Выпускаем самолёты
        if (plane_count < max_plane_count):
            delta_time_plane += delta_time
            if (delta_time_plane >= delta_time_plane_start):
                delta_time_plane = 0
                plane_count += 1
                plane = Plane((all_sprites, plane_group),
                      (width, height, 0, 100, 'plane_64.png', 'boox.png', 'plane_boox.wav',
                       plane_vx, plane_vy, shell_group, gun, plane_coef))
                arr_plane.append(plane)

        # Выпускаем бомбы
        for plane in arr_plane:
            x, y, direction = plane.get_bomb(gun.rect)
            if (x > 0):
                # Выпускаем бомбу
                Bomb((all_sprites, bomb_group), (height, x, y, 'bomb.png', 'boox.png', 'bomba_boox.wav',
                                                 20, shell_v // 2, direction, land_group, gun_group))

        # формирование кадра
        screen.fill(pygame.Color('white'))

        all_sprites.draw(screen)
        all_sprites.update(delta_time)
        screen.blit(*gun.get_text())     # Отображаем текст
#        shell_group.update()

        pygame.display.flip()  # смена кадра

        # временная задержка
        delta_time = clock1.tick(fps)    # количество миллисекунд с момента предыдущего вызова

    # Заставка: игра окончена
    screen.fill(pygame.Color('black'))

    str1 = 'GAME OVER'
    font = pygame.font.Font(None, 50)

    text = font.render(str1, 1, pygame.Color('white'))
    text_rect = text.get_rect()
    text_rect.x = (width - text_rect.width) // 2
    text_rect.y = (height - text_rect.height) // 2

    screen.blit(text, text_rect)  # Отображаем текст
    # Переключаем экран
    pygame.display.flip()

    # Ждём 1 sec
    pygame.time.wait(1000)

