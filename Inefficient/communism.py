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
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many = 511
if how_many%2==0:
    sys.exit("Oops this list will never be sorted")
find=True
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
def lowest (a_list):
    i=0
    smallest=i
    for i in range(len(a_list)):
        if a_list[i]<a_list[smallest]:
            smallest=i
    return smallest
def highest (a_list):
    i=0
    biggest=i
    for i in range(len(a_list)):
        if a_list[i]>a_list[biggest]:
            biggest=i
    return biggest
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
small,big=lowest(my_list),highest(my_list)
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
    if small==big:
        running=False
    pygame.display.flip()
    clock.tick(120)
    try:
        play_swap_sound(my_list[small],my_list[big])
    except IndexError:
        print("Error")
    for _ in range(20):
        small,big=lowest(my_list),highest(my_list)
        my_list[small]+=1
        my_list[big]-=1
print(time.perf_counter() - start_clock)
stream.close()
aud.terminate()
pygame.quit()
sys.exit() 
