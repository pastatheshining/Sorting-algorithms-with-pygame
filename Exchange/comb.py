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
pointer=0
rounds=0
swaps=0
old_swaps=0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 1024
gap_size=how_many
my_list = []
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
    screen.blit(text_surface, (30, 20))
    text_surface2 = font_style.render(f"Gap Size: {gap_size}", True, (255, 255, 255))
    screen.blit(text_surface2, (30, 60))
    where_at = 0
    is_sorted = my_list == sorted(my_list)
    for i in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at==pointer or where_at==pointer+gap_size:
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
    try:
        play_swap_sound(my_list[pointer],my_list[pointer+gap_size])
    except IndexError:
        print("Error")
    for idkvar in range(20):
        if pointer >= how_many-gap_size:
            if oldswaps=swaps:
                running=False
            pointer=0
            rounds+=1
            oldswaps=swaps
            gap_size=int(gap_size/1.3)
            if gap_size==0:
                gap_size=1
        elif my_list[pointer] > my_list[pointer+gap_size]:
            my_list[pointer], my_list[pointer+gap_size] = my_list[pointer+gap_size], my_list[pointer]
            pointer += 1
            swaps+=1
        else:
            pointer += 1
print(swaps)
print(time.perf_counter() - start_clock)
stream.close()
aud.terminate()
pygame.quit()
sys.exit() 