import pygame
import sys
import random
import time
pygame.font.init()
pygame.init()
pointer=0
rounds=0
swaps=0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
# You can now change this to higher numbers (e.g., 20 or 50)!
how_many = 256
length=how_many
my_list=[]
for i in range(how_many):
    item=random.randint(1,how_many)
    while item in my_list:
            item=random.randint(1,how_many)
    my_list.append(item)
color = pygame.Color(0, 0, 0)
clock = pygame.time.Clock()
delta_time = 0.1
running = True
total_w = 1300
bar_w = total_w / how_many
x_offset = (1440 - total_w) / 2
oddeven=0
font_style = pygame.font.SysFont("Arial", 28)
start_clock = time.perf_counter()
# RECURSIVE STOOGE SORT GENERATOR
def stooge_sort(alist, l, h):
    global swaps

    # Base case
    if l >= h:
        return
    # If first element is smaller than last, swap them
    if alist[l] > alist[h]:
        alist[l], alist[h] = alist[h], alist[l]
        swaps += 1
        yield alist  # Yield here to show the swap visually
    # If there are more than 2 elements in the current subarray
    if h - l + 1 > 2:
        t = (h - l + 1) // 3
        # Recursively sort initial 2/3 elements
        yield from stooge_sort(alist, l, h - t)
        # Recursively sort last 2/3 elements
        yield from stooge_sort(alist, l + t, h)
        # Recursively sort initial 2/3 elements again
        yield from stooge_sort(alist, l, h - t)
# Initialize the recursive generator tracking indices 0 to length-1
stooge_generator = stooge_sort(my_list, 0, how_many - 1)
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 40))
    where_at = 0
    for i in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / max(1, (how_many - 1))
        color.hsva = (colorvar % 360, 100, 100, 100)
        bar_h = (num / how_many) * 700
        pygame.draw.rect(screen, color, (x_offset + (where_at * bar_w), (800 - bar_h)/2,  max(1, bar_w - 1), bar_h))
        where_at += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if my_list == sorted(my_list):
        running = False
    pygame.display.flip()
    clock.tick(120) 
    for idkvar in range(20):
        try:
            next(stooge_generator)
        except StopIteration:
            pass
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
