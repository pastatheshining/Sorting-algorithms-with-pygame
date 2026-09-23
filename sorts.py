import pygame
import sys
import random
import time
pygame.font.init()
pygame.init()
pointer=1
swaps=0
screen = pygame.display.set_mode((1440, 850))
start_time = pygame.time.get_ticks()
how_many = 256
scrolly=0
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
pick_algo=True
while running:
    #pygame necessities and sorting visuals. do not change
    screen.fill((0, 0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    if not pick_algo:
        text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
        screen.blit(text_surface, (50, 40))
        where_at = 0
        for i in range(how_many):
            num=my_list[where_at]
            colorvar = (360 * (num - 1)) / (how_many - 1)
            if where_at==pointer or where_at==pointer+1:
                color.hsva = (0, 0, 100, 100)
            else:
                color.hsva = (colorvar % 360, 100, 100, 100)
            bar_h = (num / how_many) * 800
            pygame.draw.rect(screen, color, (x_offset + (where_at * bar_w), (850 - bar_h)-30,  max(1, bar_w - 1), bar_h))
            where_at += 1
    else:
        text_surface = font_style.render("Pick algorithm:", True, (255, 255, 255))
        screen.blit(text_surface, (630, 50))
        list_mask_rect=pygame.Rect(600,150,400,400)
        algorithms = [
            "Bubble", "Odd-even", "Comb", "Gnome", "Quick L/L", "Quick L/R", "Earthbound", "Circle",
            "Shell", "Selection", "Heap", 
            "Merge", 
            "LSD radix", "MSD radix", 
            "Intro",
            "Bogo", "Stooge"
        ]
        screen.set_clip(list_mask_rect)
        mouse_pos = pygame.mouse.get_pos()
        for algorithm in range(len(algorithms)):
            algo_text=font_style.render(algorithms[algorithm], True, (255,255,255))
            algo_text_rect = pygame.Rect(610,(algorithm*25)+150+scrolly,algo_text.get_width(),algo_text.get_height())
            screen.blit(algo_text,(610,(algorithm*25)+150+scrolly))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for algorithm in range(len(algorithms)):
                        algo_text_rect = pygame.Rect(610,(algorithm * 25) + 150 + scrolly, algo_text.get_width(), algo_text.get_height())
                        if algo_text_rect.collidepoint(event.pos):
                            print(algorithms[algorithm])
                            pick_algo = False
                            break

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                scrolly+=event.y*3
                if scrolly<-56:
                    scrolly=-56
                elif scrolly>0:
                    scrolly=0
        screen.set_clip(None)
    if my_list == sorted(my_list):
        running=False
    pygame.display.flip()
    clock.tick(120)
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit() 

