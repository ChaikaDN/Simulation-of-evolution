from random import randint
from object import Object


class Cell(Object):
    def __init__(self, pos, dna):
        """
        гены 64:
        0..7 - сделать шаг выбрать сторону в зависимости от числа.
        8..15 - схватить.
        16..23 - посмотреть (бот остается на месте, а указатель команды переходит).
        24..31 - поворот 0-315 град.  - Зачем?
        32..62 - безусловный переход.
        63 - фотосинтез
        """

        super().__init__(pos)
        self.color = (0, 0, 0)
        self.health = randint(40, 60)
        self.dna = dna
        self.gene_pos = 0
        self.generation = 1

    def step(self, gene):
        self.position = tuple(sum(i) % 90 for i in zip(self.position, Object.dirlist[gene % 8]))  # % PIXEL_COUNT (90)
        self.gene_pos = (self.gene_pos + gene % 8) % len(self.dna)  # gene % 8 надо будет заменить на условный переход

    def gene_jump(self, gene):
        self.gene_pos = (self.gene_pos + gene) % len(self.dna)

    def divide(self, cell_list):  # нужен рефакторинг
        self.health //= 2
        self.gene_pos = (self.gene_pos + 1) % len(self.dna)
        pos_list = [tuple(sum(x) for x in zip(self.position, direction)) for direction in self.dirlist]

        for cell in cell_list:
            if self.is_neighbor(cell):
                pos_list.remove(cell.position)

        if pos_list:
            child = Cell(pos_list[0], self.evolve() if not randint(0, 4) else self.dna)
            child.color = (0, 0, (child.color[2] + 20) % 256)
            cell_list.append(child)
        else:
            self.health = 0

    def evolve(self):
        dna = self.dna[:]
        dna[randint(0, 63)] = randint(0, 63)
        return dna

    def live(self, cell_list):
        if self.health > 100:
            self.divide(cell_list)
        elif self.health > 0:
            gene = self.dna[self.gene_pos]
            match gene:
                case gene if 0 <= gene <= 7:
                    self.step(gene)
                case gene if 8 <= gene <= 15:
                    # cell.catch(gene)
                    pass
                case gene if 16 <= gene <= 23:
                    # cell.look(gene)
                    pass
                case gene if 24 <= gene <= 31:
                    # cell.rotate(gene)
                    pass
                case gene if 32 <= gene <= 62:
                    self.gene_jump(gene)
                case 63:
                    # cell.photosynthesis(gene)
                    pass
            self.health -= 1
        else:
            self.is_alive = False
