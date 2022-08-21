import random
from random import randint
from object import Object


def check_obj_type(obj=None):
    return 'Nothing' if obj is None else str(type(obj)).split('.')[1][:-2]


def add_coords(position1, position2, mod=None):
    return tuple(map(lambda x, y: x + y, position1, position2)) if mod is None else \
        tuple(map(lambda x, y: (x + y) % mod, position1, position2))


class Cell(Object):
    def __init__(self, pos, dna, color=None):
        """
        Гены 64:
        0..7 - сделать шаг выбрать сторону в зависимости от числа.
        8..15 - схватить.
        16..23 - посмотреть (бот остается на месте, а указатель команды переходит).
        24..31 - поворот 0-315 град.  - Зачем?
        32..61 - безусловный переход.
        62 - деление
        63 - фотосинтез
        """

        super().__init__(pos, color)
        self.health = randint(40, 60)
        self.dna = dna
        self.gene_pos = 0
        self.age = 0
        self.max_age = random.randint(120, 170)
        # self.generation = 1

        self.is_alive = True
        self.is_ready_to_divide = False

    def step(self, gene, distance):
        self.position = add_coords(self.position, Object.dirlist[gene % 8], mod=distance)
        self.gene_jump(1)

    def look(self, gene, *obj_lists):  # gene = 0..7
        pos = add_coords(self.position, self.dirlist[gene % 8])
        for obj_list in obj_lists:
            for obj in obj_list:
                if obj.position == pos:
                    return self.conditional_jump(check_obj_type(obj))
        return self.gene_jump(1)

    def kill(self, gene, cell_list):
        pos = add_coords(self.position, self.dirlist[gene % 8])
        for cell in cell_list:
            if cell.position == pos:
                cell.is_alive = False

    def eat(self):
        pass

    def photosynthesis(self, light_rate):
        self.health += light_rate

        self.color[0] -= 5 if self.color[0] >= 5 else 0
        self.color[1] += 5 if self.color[1] <= 120 else 0
        self.color[2] -= 5 if self.color[2] >= 5 else 0

        self.gene_jump(1)

    def gene_jump(self, step):
        self.gene_pos = (self.gene_pos + step) % len(self.dna)

    def conditional_jump(self, condition):
        match condition:
            case 'Nothing':  # не обязательно
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

    def divide(self, max_distance, cell_list, wall_list=None):
        if wall_list is None:
            wall_list = []
        self.health //= 2
        pos_list = list(filter(lambda x: 0 <= x[0] < max_distance and 0 <= x[1] < max_distance,
                               [add_coords(self.position, direction) for direction in self.dirlist]))
        child_dna = self.evolve() if not randint(0, 4) else self.dna

        for obj in cell_list + wall_list:
            if obj.position in pos_list:
                pos_list.remove(obj.position)
        if pos_list:
            cell_list.append(Cell(random.choice(pos_list), child_dna, color=self.color))
        else:
            self.is_alive = False
        self.gene_jump(1)

    def evolve(self):
        dna = self.dna[:]
        dna[randint(0, 63)] = randint(0, 63)
        return dna

    def live(self, distance, cell_list=None, meat_list=None, wall_list=None):
        self.age += 1
        if self.age >= self.max_age:
            self.is_alive = False
            return

        if self.health > 100:
            self.is_ready_to_divide = True
        elif self.health > 0:
            self.is_ready_to_divide = False
            gene = self.dna[self.gene_pos]
            match gene:
                case gene if 0 <= gene <= 7:
                    self.step(gene, distance)
                case gene if 8 <= gene <= 15:
                    self.kill(gene, cell_list)
                case gene if 16 <= gene <= 23:
                    self.look(gene, cell_list, meat_list, wall_list)
                case gene if 24 <= gene <= 62:
                    self.gene_jump(gene)
                case 63:
                    self.photosynthesis(random.choice((1, 2)))
                    pass
            self.health -= 1
        else:
            self.is_alive = False
