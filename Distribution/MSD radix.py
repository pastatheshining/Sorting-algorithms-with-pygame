import pygame
import sys
import random
import time
import math
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
screen = pygame.display.set_mode((1440, 800))
start_time = pygame.time.get_ticks()
how_many=2048
my_list=[]
def play_swap_sound(val1):
    bytes_audio = bytearray()
    total_samples = int(my_rate * length)
    fade_samples = int(total_samples * 0.25)
    for n in range(total_samples):
        point = math.sin(2 * math.pi * (((val1 / how_many) * 500) + 150) * (n / my_rate))
        if n > total_samples - fade_samples:
            point *= ((total_samples - n) / fade_samples)
        vol_int = int(point * 32767 * volume)
        bytes_audio.extend(vol_int.to_bytes(2, byteorder="little", signed=True))
    stream.write(bytes(bytes_audio))
for i in range(how_many):
    item=random.randint(0,how_many-1)
    while item in my_list:
        item=random.randint(0,how_many-1)
    my_list.append(item)
color = pygame.Color(0, 0, 0)
state_stack = []
start = 0
end = how_many
bucketing=True
buck0=[]
buck1=[]
buck2=[]
buck3=[]
i=0
def bucket(a_list):
    global swaps, bucketing, buck0, buck1, buck2, buck3, i, place_value, running, start, end  
    if bucketing:
        digit = (a_list[i] // place_value) % 4
        if digit==0:
            buck0.append(a_list[i])
        elif digit==1:
            buck1.append(a_list[i])
        elif digit==2:
            buck2.append(a_list[i])
        elif digit==3:
            buck3.append(a_list[i])
        i+=1
        if i>=end:
            bucketing=False
            i=start
    else:
        if i<start + len(buck0):
            a_list[i]=buck0[i-start]
        elif i<start + len(buck0)+len(buck1):
            a_list[i]=buck1[i-start-len(buck0)]
        elif i<start + len(buck0)+len(buck1)+len(buck2):
            a_list[i]=buck2[i-start-(len(buck0)+len(buck1))]
        else:
            a_list[i]=buck3[i-start-(len(buck0)+len(buck1)+len(buck2))]
        swaps += 1
        i+=1
        if i>=end:
            next_pv = place_value // 4
            if next_pv >= 1:
                b0_len = len(buck0)
                b1_len = len(buck1)
                b2_len = len(buck2)
                b3_len = len(buck3)    
                if end > start + b0_len + b1_len + b2_len:
                    state_stack.append((end, start + b0_len + b1_len + b2_len, next_pv))
                if start + b0_len + b1_len + b2_len > start + b0_len + b1_len:
                    state_stack.append((start + b0_len + b1_len + b2_len, start + b0_len + b1_len, next_pv))
                if start + b0_len + b1_len > start + b0_len:
                    state_stack.append((start + b0_len + b1_len, start + b0_len, next_pv))
                if start + b0_len > start:
                    state_stack.append((start + b0_len, start, next_pv))      
            if len(state_stack) > 0:
                end, start, place_value = state_stack.pop()
                buck0.clear()
                buck1.clear()
                buck2.clear()
                buck3.clear()
                bucketing = True
                i = start
            else:
                running = False         
clock = pygame.time.Clock()
delta_time = 0.1
running = True
total_w = 1300
bar_w = total_w / how_many
x_offset = (1440 - total_w) / 2
font_style = pygame.font.SysFont("Arial", 28)
start_clock = time.perf_counter()
bits=math.ceil(math.log(how_many,4))-1
low=0
high=how_many-1
place_value=4**bits
while running:
    screen.fill((0, 0, 0))
    text_surface = font_style.render(f"Writes to array: {swaps}", True, (255, 255, 255))
    screen.blit(text_surface, (50, 40))
    where_at = 0
    box_counts=[0,0,0,0]
    for j in range(how_many):
        num=my_list[where_at]
        colorvar = (360 * (num - 1)) / (how_many - 1)
        if where_at==i:
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
        bucket(my_list)
    try:
        play_swap_sound(my_list[i])
    except IndexError:
        print("Error")
print(swaps)
print(time.perf_counter() - start_clock)
stream.close()
aud.terminate()
pygame.quit()
sys.exit()
