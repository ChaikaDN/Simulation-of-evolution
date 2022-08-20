import random
from random import randint
from object import Object


def check_obj_type(obj=None):
    obj_type = str(type(obj)).split('.')[1][:-2] if obj is not None else 'Nothing'
    return obj_type


class Cell(Object):
    def __init__(self, pos, dna):
        """
        Гены 64:
        0..7 - сделать шаг выбрать сторону в зависимости от числа.
        8..15 - схватить.
        16..23 - посмотреть (бот остается на месте, а указатель команды переходит).
        24..31 - поворот 0-315 град.  - Зачем?
        32..62 - безусловный переход.
        63 - фотосинтез
        """

        super().__init__(pos)
        self.color = [0, 0, 0]
        self.health = randint(40, 60)
        self.dna = dna
        self.gene_pos = 0
        self.generation = 1  # пригодится потом
        self.age = 0

        self.is_alive = True
        self.is_ready_to_divide = False

    def step(self, gene):
        self.position = tuple(sum(i) % 90 for i in zip(self.position, Object.dirlist[gene % 8]))  # % PIXEL_COUNT (90)
        # self.gene_jump(gene % 8)  # gene % 8 надо будет заменить на условный переход
        self.conditional_jump(check_obj_type())

    def look(self, gene, *obj_lists):  # gene = 0..7
        pos = tuple(sum(x) for x in zip(self.position, self.dirlist[gene]))
        for obj_list in obj_lists:
            for obj in obj_list:
                if obj.position == pos:
                    return self.conditional_jump(check_obj_type(obj))
        return self.conditional_jump(check_obj_type())

    def kill(self, gene, cell_list):
        pos = tuple(sum(x) for x in zip(self.position, self.dirlist[gene]))
        for cell in cell_list:
            if cell.position == pos:
                cell.is_alive = False

    def photosynthesis(self, light_rate):
        self.health += light_rate
        self.color[0] -= 5 if self.color[0] >= 5 else 0
        self.color[1] -= 5 if self.color[1] >= 5 else 0
        self.color[2] += 5 if self.color[2] <= 250 else 0
        self.gene_jump(1)

    def gene_jump(self, step):
        self.gene_pos = (self.gene_pos + step) % len(self.dna)

    def conditional_jump(self, condition):
        match condition:
            case 'Nothing':
                self.gene_jump(1)
            case 'Cell':
                self.gene_jump(2)
            case 'Grass':
                self.gene_jump(3)
            case 'Meat':
                self.gene_jump(4)
            case 'Wall':
                print('wall')
                self.gene_jump(5)

    def divide(self, *obj_lists):  # нужен рефакторинг, obj_lists = cells, walls
        self.health //= 2

        pos_list = [tuple(sum(x) for x in zip(self.position, direction)) for direction in self.dirlist]

        for obj_list in obj_lists:
            for obj in obj_list:
                if self.is_neighbor(obj):
                    pos_list.remove(obj.position)

        if pos_list:
            child = Cell(random.choice(pos_list), self.evolve() if not randint(0, 4) else self.dna)
            child.color = self.color
            return child
        else:
            self.is_alive = False

        self.gene_jump(1)

    def evolve(self):
        dna = self.dna[:]
        dna[randint(0, 63)] = randint(0, 63)
        return dna

    def live(self, *obj_lists):
        self.age += 1
        if self.age >= 128:
            self.is_alive = False
            return

        if self.health > 100:
            self.is_ready_to_divide = True
        elif self.health > 0:
            self.is_ready_to_divide = False
            gene = self.dna[self.gene_pos]
            match gene:
                case gene if 0 <= gene <= 7:
                    self.step(gene)
                case gene if 8 <= gene <= 15:
                    self.kill(gene % 8, obj_lists[0])
                case gene if 16 <= gene <= 23:
                    self.look(gene % 8, *obj_lists)
                case gene if 24 <= gene <= 31:
                    # cell.rotate(gene)
                    pass
                case gene if 32 <= gene <= 62:
                    self.gene_jump(gene)
                case 63:
                    self.photosynthesis(random.choice((1, 2)))
                    pass
            self.health -= 1
        else:
            self.is_alive = False
