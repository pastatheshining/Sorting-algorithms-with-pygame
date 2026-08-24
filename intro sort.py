import pygame
import sys
import random
import time
import math
recursion_level = 1
pygame.font.init()
pygame.init()
rounds = 0
swaps = 0
current2 = 0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 2048
heap_length = how_many
my_list = []
for i in range(how_many):
    item = random.randint(1, how_many)
    while item in my_list:
        item = random.randint(1, how_many)
    my_list.append(item)
pointera = 0
pointerb = how_many - 1
color = pygame.Color(0, 0, 0)
clock = pygame.time.Clock()
delta_time = 0.1
running = True
total_w = 1300
bar_w = total_w / how_many
x_offset = (1440 - total_w) / 2
font_style = pygame.font.SysFont("Arial", 28)
def insertionsort_slice_generator(low, high):
    global swaps, pointera, pointerb
    for i in range(low + 1, high + 1):
        j = i
        while j > low and my_list[j] < my_list[j - 1]:
            pointera = j
            pointerb = j - 1
            my_list[j], my_list[j - 1] = my_list[j - 1], my_list[j]
            swaps += 1
            j -= 1
            yield
def heapsort_slice_generator(low, high):
    global swaps
    n = high - low + 1
    if n <= 1:
        return
    where_at = (n // 2) - 1
    while where_at >= 0:
        current = where_at
        while 2 * current + 1 < n:
            left = 2 * current + 1
            right = 2 * current + 2
            largest = current
            if my_list[low + left] > my_list[low + largest]:
                largest = left
            if right < n and my_list[low + right] > my_list[low + largest]:
                largest = right
            if largest == current:
                break
            my_list[low + current], my_list[low + largest] = my_list[low + largest], my_list[low + current]
            swaps += 1
            current = largest
            yield
        where_at -= 1
    h_len = n
    while h_len > 1:
        my_list[low], my_list[low + h_len - 1] = my_list[low + h_len - 1], my_list[low]
        swaps += 1
        current2 = 0
        h_len -= 1
        if h_len > 1:
            for z in range(math.ceil(math.log(h_len + 1, 2)) - 1):
                left = 2 * current2 + 1
                right = 2 * current2 + 2
                if left < h_len and right < h_len:
                    if my_list[low + left] > my_list[low + right]:
                        chosen = left
                    else:
                        chosen = right
                    if my_list[low + chosen] > my_list[low + current2]:
                        my_list[low + chosen], my_list[low + current2] = my_list[low + current2], my_list[low + chosen]
                        swaps += 1
                        current2 = chosen
                    else:
                        break
                elif left < h_len:
                    if my_list[low + left] > my_list[low + current2]:
                        my_list[low + left], my_list[low + current2] = my_list[low + current2], my_list[low + left]
                        swaps += 1
                        current2 = left
                    else:
                        break
                else:
                    break
def quicksort_generator(low, high):
    global pointera, pointerb, swaps, recursion_level
    if low >= high:
        return   
    if (high - low + 1) < 16:
        yield from insertionsort_slice_generator(low, high)
        return
    if recursion_level > 2 * math.log(how_many, 2):
        yield from heapsort_slice_generator(low, high)
        return
    mid_idx = (low + high) // 2
    pivot = my_list[mid_idx]
    pointera = low
    pointerb = high
    mova = True
    while pointera <= pointerb:
        if mova:
            if my_list[pointera] > pivot:
                mova = False
            else:
                pointera += 1
            yield
        else:
            if my_list[pointerb] < pivot:
                my_list[pointera], my_list[pointerb] = my_list[pointerb], my_list[pointera]
                swaps += 1
                mova = True
                pointerb -= 1
            else:
                pointerb -= 1
            yield       
    recursion_level += 1
    yield from quicksort_generator(low, pointerb)
    yield from quicksort_generator(pointera, high)
    recursion_level -= 1
sort_pipeline = quicksort_generator(0, how_many - 1)
start_clock = time.perf_counter()
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps} Recursion level: {recursion_level}", True, (255, 255, 255))
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
            running = False
    pygame.display.flip()
    clock.tick(120)
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
