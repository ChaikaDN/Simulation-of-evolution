from random import randint
from object import Object


class Cell(Object):
    def __init__(self, pos, dna):
        super().__init__(pos)
        self.color = (0, 0, 0)
        """
        гены 64:
        0..7 - сделать шаг выбрать сторону в зависимости от числа.
        8..15 - схватить.
        16..23 - посмотреть (бот остается на месте, а указатель команды переходит).
        24..31 - поворот 0-315 град.  - Зачем?
        32..62 - безусловный переход.
        63 - фотосинтез
        """
        self.health = randint(40, 60)
        self.dna = dna
        # self.dna = [randint(0, 63) for _ in range(64)]
        self.gene_pos = 0
        self.generation = 1

    def step(self, gene):
        self.position = tuple(sum(i) % 90 for i in zip(self.position, Object.dirlist[gene % 8]))  # % PIXEL_COUNT (90)
        self.gene_pos = (self.gene_pos + gene % 8) % len(self.dna)  # gene % 8 надо будет заменить на условный переход
    #
    # def catch(self, gene):
    #     self.gene_pos = (self.gene_pos + gene % 8) % len(self.dna)
    #     # print(f'схватил на {gene % 8}')
    #
    # def photosynthesis(self, gene):
    #     self.gene_pos = (self.gene_pos + 1) % len(self.dna)
    #     # print(f'фотосинтез {gene}')
    #
    # def look(self, gene):
    #     self.gene_pos = (self.gene_pos + 1) % len(self.dna)
    #     # print(f'посмотрел на {gene % 8}')

    # def rotate(self, gene):  # бесполезный метод?
    #     self.direction = Object.dirlist[gene % 8]
    #     self.gene_pos = (self.gene_pos + gene % 8) % len(self.dna)
    #     # print(f'повернулся на {gene % 8}')

    def gene_jump(self, gene):
        self.gene_pos = (self.gene_pos + gene) % len(self.dna)  # условный переход

    def divide(self, cell_list):  # проверять свободно ли место для деления, если нет, то клетка умирает
        self.health //= 2
        self.gene_pos = (self.gene_pos + 1) % len(self.dna)

        pos_list = [tuple(sum(x) for x in zip(self.position, direction)) for direction in self.dirlist]
        for cell in cell_list:
            if self.is_neighbor(cell):
                x = cell.position
                pos_list.remove(cell.position)
        if pos_list:
            child = Cell(pos_list[0], self.evolve() if not randint(0, 4) else self.dna)
            child.color = (0, 0, (child.color[2] + 20) % 256)
            print('!!!')
            cell_list.append(child)
        else:
            self.health = 0

    def evolve(self):
        dna = self.dna[:]
        dna[randint(0, 63)] = randint(0, 63)
        print('***')
        return dna
