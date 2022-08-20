from cell import Cell
from life_manager import live
import random
import time

"""
https://www.youtube.com/watch?v=SfEZSyvbj2w&list=PLnmlxA5EUR3F4BrpqTl0koT5Cx5aXjBIA

cells = [Cell([random.randint(0, 63) for _ in range(64)]) for _ in range(8)]

with open('start.txt', 'w') as file:
    for cell in cells:
        print(*cell.dna, file=file)

for _ in range(5):
    for cell in list(cells):  # list создал копию списка, исзодный список можно редактировать
        for i in range(8):
            dna = cell.dna
            if i == 7:  # каждый восьмой мутирует
                dna[random.randint(0, 63)] = random.randint(0, 63)
            cells.append(Cell(cell.dna))

    while Cell.count > 8:
        for cell in cells:
            live(cell)
            if not cell.is_alive:
                cells.remove(cell)  # не уменьшается count попробовать del
        # time.sleep(0.1)

with open('end.txt', 'w') as file:
    for cell in cells:
        print(*cell.dna, file=file)
"""