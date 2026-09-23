import pygame
import sys
import random
import time
from math import sin, pi
import pyaudio 
my_rate=48000
pit=500
length=0.01
volume=0.6
aud=pyaudio.PyAudio()
stream=aud.open(format=pyaudio.paInt16, channels=1, rate=my_rate, output=True,)
pygame.font.init()
pygame.init()
rounds=0
swaps=0
old_swaps=0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 1024
pointera=0
pointerb=how_many-1
my_list=[]
def play_swap_sound(val1, val2):
    bytes_audio = bytearray()
    total_samples = int(my_rate * length)
    fade_samples = int(total_samples * 0.25)
    for n in range(total_samples):
        point = sin(2 * pi * (((val1 / how_many) * 500) + 150) * (n / my_rate))
        if n > total_samples - fade_samples:
            point *= ((total_samples - n) / fade_samples)
        vol_int = int(point * 32767 * volume)
        bytes_audio.extend(vol_int.to_bytes(2, byteorder="little", signed=True))
    stream.write(bytes(bytes_audio))
    bytes_audio2 = bytearray()
    for n in range(total_samples):
        point = sin(2 * pi * (((val2 / how_many) * 500) + 150) * (n / my_rate))
        if n > total_samples - fade_samples:
            point *= ((total_samples - n) / fade_samples)
        vol_int = int(point * 32767 * volume)
        bytes_audio2.extend(vol_int.to_bytes(2, byteorder="little", signed=True))
    stream.write(bytes(bytes_audio2))
for i in range(how_many):
    item=random.randint(1,how_many)
    while item in my_list:
        item=random.randint(1,how_many)
    my_list.append(item)
color = pygame.Color(0, 0, 0)
clock = pygame.time.Clock()
delta_time = 0.1
running = True
sorting=True
total_w = 1300
bar_w = total_w / how_many
x_offset = (1440 - total_w) / 2
font_style = pygame.font.SysFont("Arial", 28)
start_clock = time.perf_counter()
def circle(low,high):
    global swaps, my_list, pointera, pointerb, step_counter
    if low >= high:
        return
    pointera=low
    pointerb=high
    while pointera < pointerb:
        if my_list[pointera]>my_list[pointerb]:
            my_list[pointera],my_list[pointerb]=my_list[pointerb],my_list[pointera]
            yield
            swaps+=1
        pointera+=1
        pointerb-=1
    yield
    yield from circle(low,(low+high)//2)
    yield from circle(((low+high)//2)+1,high)
sort_pipeline = circle(0, how_many - 1)
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total Swaps: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 40))
    where_at = 0
    for i in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at==pointera or where_at==pointerb:
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
        if sorting:
            try:
                next(sort_pipeline)
            except StopIteration:
                if old_swaps==swaps:
                    running=False
                    break
                old_swaps=swaps
                sort_pipeline = circle(0, how_many - 1)
    for i in range(len(my_list)-1):
        if my_list[i]>my_list[i+1]:
            break
    play_swap_sound(my_list[pointera],my_list[pointerb])
print(swaps)
print(time.perf_counter() - start_clock)
pygame.quit()
sys.exit()
