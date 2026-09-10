import pygame
import sys
import random
import time
import math
pygame.font.init()
pygame.init()
pointer=0
rounds=0
swaps=0
run_size=0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 365
minrun=how_many
insert=False
while minrun>32:
    minrun//=2
my_list=[]
aux=[]
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
font_style = pygame.font.SysFont("Arial", 28)
start_clock = time.perf_counter()
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 40))
    where_at = 0
    for i in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at==pointer:
            color.hsva = (0, 0, 100, 100)
        else:
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
        if pointer >= how_many - 1 and not insert:
            if not asc:
                run_start = (pointer // minrun) * minrun
                my_list[run_start:pointer+1] = reversed(my_list[run_start:pointer+1])
                swaps += 1
            insert = True
            break
        if pointer/minrun==pointer//minrun:
            if my_list[pointer]<my_list[pointer+1]:
                asc=True
            else:
                asc=False
            run_size=1
            pointer+=1
            if pointer//(minrun*2)==pointer/(minrun*2):
                merging=True
        elif not insert:
            if asc:
                if my_list[pointer]<=my_list[pointer+1]:
                    run_size+=1
                else:
                    insert=True
            else:
                if my_list[pointer]>=my_list[pointer+1]:
                    run_size+=1
                else:
                    run_start = (pointer // minrun) * minrun
                    my_list[run_start:pointer+1] = reversed(my_list[run_start:pointer+1])
                    swaps += 1
                    insert=True
            pointer+=1
        else:
            if pointer<how_many:
                if my_list[pointer-1]<my_list[pointer]:
                    pointer+=1
                    if pointer % minrun == 0:
                        insert = False
                else:
                    my_list[pointer-1], my_list[pointer] = my_list[pointer], my_list[pointer-1]
                    swaps+=1
                    run_start = (pointer // minrun) * minrun
                    if pointer > run_start + 1:
                        pointer-=1
                    else:
                        pointer+=1
            elif merging:
                continue
            else:
                running = False
                break
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
