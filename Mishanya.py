import pygame
import random

width = 360
height = 480
fps = 30

# Задаем цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_trava = (160, 255, 100)
color_voda = (70, 120, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init() # Звук
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(fps)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    
    # Рендеринг
    screen.fill(color_voda)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
