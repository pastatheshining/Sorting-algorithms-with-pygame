import pygame
import sys
import random
import math
import time
pygame.font.init()
pygame.init()
pointer=0
swaps=0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 2048
move=0
gap_size=int(how_many/2.3)
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
font_style = pygame.font.SysFont("Arial", 28)
start_clock = time.perf_counter()
while running:
    #pygame necessities and sorting visuals. do not change
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (30, 20))
    text_surface2 = font_style.render(f"Gap Size: {gap_size}", True, (255, 255, 255))
    screen.blit(text_surface2, (30, 60))
    where_at = 0
    for i in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at==pointer or where_at==pointer+gap_size:
            color.hsva = (0, 0, 100, 100)
        else:
            color.hsva = (colorvar % 360, 100, 100, 100)
        bar_h = (num / how_many) * 700
        pygame.draw.rect(screen, color, (x_offset + (where_at * bar_w), (800 - bar_h)/2, max(1, bar_w - 1), bar_h))
        where_at += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if gap_size==0:
        running = False
    pygame.display.flip()
    clock.tick(120)
    #sorting algorithm. change it
    for idkvar in range(20):
        if pointer+gap_size>=how_many:
            pointer=0
            if gap_size==1:
                gap_size=0
            gap_size=math.ceil(gap_size/2.3)
            
            move=0
        else:
            if my_list[pointer]<=my_list[pointer+gap_size]:
                if move > 0:
                    pointer += move
                    move = 0
                else:
                    pointer+=1
            else:
                my_list[pointer], my_list[pointer + gap_size] = my_list[pointer + gap_size], my_list[pointer]
                swaps+=1
                if pointer>0:
                    if pointer>=gap_size:
                       pointer-=gap_size
                       move+=gap_size
                    else:
                        if move > 0:
                            pointer += move
                            move = 0
                        else:
                            pointer+=1
                else:
                    if move>0:
                        pointer+=move
                        move=0
                    else:
                         pointer+=1
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit() 