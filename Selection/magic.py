import random
import time
aux_array=[]
the_list=[]
how_many=100
skip=[True]*how_many
start_clock = time.perf_counter()
for i in range(how_many):
    item=random.randint(1,how_many)
    while item in the_list:
        item=random.randint(1,how_many)
    the_list.append(item)
def lowest (my_list):
    smallest=None
    smallesti=0
    i=0
    for i in range(len(my_list)):
        if skip[i]==True and (smallest is None or my_list[i]<smallest):
            smallest= my_list[i]
            smallesti=i
    return f"Smallest is: {smallest}. Position of smallest is: {smallesti}"
def lowest_fr_py (my_list):
    smallest=None
    smallesti=0
    i=0
    for i in range(len(my_list)):
        if skip[i]==True and (smallest is None or my_list[i]<smallest):
            smallest=my_list[i]
            smallesti=i
    return smallesti
for g in range(len(the_list)):
    lowesttwo=lowest_fr_py(the_list)
    aux_array.append(the_list[lowesttwo])
    skip[lowesttwo]=False
the_list=aux_array.copy()
aux_array.clear()
print(time.perf_counter() - start_clock)
