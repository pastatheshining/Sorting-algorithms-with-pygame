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
pointer = 1
oldpointer = 1
inserts = 0
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 256
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
    # pygame necessities and sorting visuals. do not change
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Total inserts: {inserts}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 40))
    where_at = 0
    for i in range(how_many):
        num = my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at == oldpointer or where_at == pointer:
            color.hsva = (0, 0, 100, 100)
        else:
            color.hsva = (colorvar % 360, 100, 100, 100)
        bar_h = (num / how_many) * 700
        pygame.draw.rect(screen, color, (x_offset + (where_at * bar_w), (800 - bar_h) / 2, max(1, bar_w - 1), bar_h))
        where_at += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if my_list == sorted(my_list):
        running = False

    pygame.display.flip()
    clock.tick(120)
    try:
        play_swap_sound(my_list[pointer],my_list[oldpointer])
    except IndexError:
        print("Error")
    for idkvar in range(20):
        if oldpointer < how_many:
            if pointer > 0 and my_list[pointer-1] > my_list[oldpointer]:
                pointer -= 1
            else:
                if pointer < oldpointer:
                    my_list.insert(pointer, my_list[oldpointer])
                    my_list.pop(oldpointer+1)
                    inserts += 1
                oldpointer += 1
                pointer = oldpointer
        else:
            break
print(inserts)
print(time.perf_counter() - start_clock)
stream.close()
aud.terminate()
pygame.quit()
sys.exit()
