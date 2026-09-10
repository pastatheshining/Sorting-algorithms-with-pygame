import pygame
import sys
import random
import time

pygame.font.init()
pygame.init()

rounds = 0
swaps = 0
merging = True
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 48
pointer = 0
my_list = []
aux = []
pointera = 0
pointerb = how_many // 2

for i in range(how_many):
    item = random.randint(1, how_many)
    while item in my_list:
        item = random.randint(1, how_many)
    my_list.append(item)

color = pygame.Color(0, 0, 0)
clock = pygame.time.Clock()
delta_time = 0.1
running = True
total_w = 1300
bar_w = total_w / how_many
x_offset = (1440 - total_w) / 2
font_style = pygame.font.SysFont("Arial", 28)
start_clock = time.perf_counter()

def merge(start, end):
    global swaps, pointera, pointerb
    if start >= end:
        return
    mid = (start + end) // 2
    yield from merge(start, mid)
    yield from merge(mid + 1, end)
    pointera = mid
    pointerb = end
    if my_list[mid] > my_list[end]:
        my_list[mid], my_list[end] = my_list[end], my_list[mid]
        swaps += 1
    yield
    yield from merge(start, end - 1)
sorter = merge(0, how_many - 1)
sorting_finished = False

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
    if not sorting_finished:
        for idkvar in range(20):
            try:
                next(sorter)
            except StopIteration:
                sorting_finished = True
                pointera = -1
                pointerb = -1
                break
    pygame.display.flip()
    clock.tick(120)
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
