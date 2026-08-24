import pygame
import sys
import random
import time
import math
pygame.font.init()
pygame.init()
rounds = 0
swaps = 0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 2048
my_list = []
for i in range(how_many):
    item = random.randint(1, how_many)
    while item in my_list:
        item = random.randint(1, how_many)
    my_list.append(item)
pointera = 0
pointerb = 0
color = pygame.Color(0, 0, 0)
clock = pygame.time.Clock()
delta_time = 0.1
running = True
total_w = 1300
bar_w = total_w / how_many
x_offset = (1440 - total_w) / 2
font_style = pygame.font.SysFont("Arial", 28)
def quicksort_ll_generator(low, high):
    global pointera, pointerb, swaps
    if low >= high:
        return
    pivot = my_list[high]
    pointera = low
    pointerb = low
    while pointerb < high:
        if my_list[pointerb] < pivot:
            my_list[pointera], my_list[pointerb] = my_list[pointerb], my_list[pointera]
            swaps += 1
            pointera += 1
        pointerb += 1
        yield
    my_list[pointera], my_list[high] = my_list[high], my_list[pointera]
    swaps += 1
    yield
    yield from quicksort_ll_generator(low, pointera - 1)
    yield from quicksort_ll_generator(pointera + 1, high)
sort_pipeline = quicksort_ll_generator(0, how_many - 1)
start_clock = time.perf_counter()
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 40))
    where_at = 0
    for i in range(how_many):
        num = my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at == pointera or where_at == pointerb:
            color.hsva = (0, 0, 100, 100)
        else:
            color.hsva = (colorvar % 360, 100, 100, 100)
        bar_h = (num / how_many) * 700
        pygame.draw.rect(screen, color, (x_offset + (where_at * bar_w), (800 - bar_h) / 2, max(1, bar_w - 1), bar_h))
        where_at += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for idkvar in range(20):
        try:
            next(sort_pipeline)
        except StopIteration:
            pass
    if my_list == sorted(my_list):
        running = False
    pygame.display.flip()
    clock.tick(120)
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
