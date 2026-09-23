import pygame
import sys
import random
import time
import math
import pyaudio 
pygame.font.init()
pygame.init()
swaps = 0
current2 = 0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 3072
heap_length = how_many
heap_building = True
where_at = how_many // 2 + 1
my_list = []
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
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 20))
    where_at2 = 0
    for i in range(how_many):
        num = my_list[where_at2]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at2 != where_at:
            color.hsva = (colorvar % 360, 100, 100, 100)
        else:
            color.hsva = (0, 0, 100, 100)
        bar_h = (num / how_many) * 700
        pygame.draw.rect(screen, color, (x_offset + (where_at2 * bar_w), (800 - bar_h) / 2, max(1, bar_w - 1), bar_h))
        where_at2 += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(120)
    for idkvar in range(3):
        if heap_building:
            if where_at <= 0:
                heap_building = False
            current = where_at
            while 2 * current + 1 < how_many:
                if 2 * current + 2 < how_many:
                    largest = 2 * current + 1
                    if my_list[2 * current + 2] > my_list[largest]:
                        largest = 2 * current + 2
                    if my_list[largest] > my_list[current]:
                        swaps += 1
                        my_list[largest], my_list[current] = my_list[current], my_list[largest]
                        current = largest
                    else:
                        break
                elif 2 * current + 1 < how_many:
                    if my_list[2 * current + 1] > my_list[current]:
                        swaps += 1
                        my_list[2 * current + 1], my_list[current] = my_list[current], my_list[2 * current + 1]
                        current = 2 * current + 1
                    else:
                        break
            where_at -= 1
        else:
            my_list[0], my_list[heap_length - 1] = my_list[heap_length - 1], my_list[0]
            swaps += 1
            current2 = 0
            heap_length -= 1
            if heap_length>1:
                for z in range(math.ceil(math.log(heap_length + 1, 2)) - 1):
                    left = 2 * current2 + 1
                    right = 2 * current2 + 2
                    if left < heap_length and right < heap_length:
                        if my_list[left] > my_list[right]:
                            chosen = left
                        else:
                            chosen = right
                        if my_list[chosen] > my_list[current2]:
                            my_list[chosen], my_list[current2] = my_list[current2], my_list[chosen]
                            swaps += 1
                            current2 = chosen
                        else:
                            break
                    elif left < heap_length:
                        if my_list[left] > my_list[current2]:
                            my_list[left], my_list[current2] = my_list[current2], my_list[left]
                            swaps += 1
                            current2 = left
                        else:
                            break
                    else:
                        break
            else:
                running=False
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
