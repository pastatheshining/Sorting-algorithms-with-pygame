import pygame
import sys
import random
import time
pygame.font.init()
pygame.init()
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 256
pointer=1
sorting=True
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
start_clock = time.perf_counter()
while running:
    screen.fill((0, 0, 0))
    where_at = 0
    for i in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        color.hsva = (colorvar % 360, 100, 100, 100)
        bar_h = (num / how_many) * 700
        pygame.draw.rect(screen, color, (x_offset + (where_at * bar_w), (800 - bar_h)/2,  max(1, bar_w - 1), bar_h))
        where_at += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(120)
    for idkvar in range(20):
        if sorting:
            if pointer>=how_many:
                sorting=False
                break
            if my_list[pointer-1]>my_list[pointer]:
                my_list[pointer]=my_list[pointer]+1
            else:
                pointer+=1
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit() 
