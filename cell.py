import random
from functools import reduce
from object import Object, check_obj_type, add_coords


class Cell(Object):
    def __init__(self, pos, dna, color=None):
        """
        Гены 64:
        0..7 - сделать шаг выбрать сторону в зависимости от числа.
        8..15 - схватить.
        16..23 - посмотреть (бот остается на месте, а указатель команды переходит).
        24..61 - безусловный переход.
        62 - деление
        63 - фотосинтез
        """

        super().__init__(pos, color)
        self.health = random.randint(40, 60)
        self.dna = dna
        self.gene_pos = 0
        self.age = 0
        self.max_age = random.randint(120, 170)
        self.generation = 1

        self.is_alive = True
        self.is_ready_to_divide = False

    def step(self, gene, distance):
        self.position = add_coords(self.position, Object.dirlist[gene % 8], mod=distance)
        self.gene_jump(1)

    def look(self, gene, *obj_lists):
        pos = add_coords(self.position, self.dirlist[gene % 8])
        for obj in reduce(lambda x, y: x + y, obj_lists):
            if obj.position == pos:
                return self.conditional_jump(check_obj_type(obj))
        return self.gene_jump(1)

    def kill(self, gene, cell_list):
        pos = add_coords(self.position, self.dirlist[gene % 8])
        for cell in cell_list:
            difference = [gene for gene in self.dna if gene not in cell.dna]
            if cell.position == pos and len(difference) >= 2:
                cell.is_alive = False
        self.gene_jump(1)

    def eat(self, obj):
        self.health += int(obj.health)
        obj.is_alive = False

    def photosynthesis(self, light_rate):
        self.health += light_rate

        self.color[0] -= 5 if self.color[0] >= 5 else 0
        self.color[1] += light_rate * 2 if self.color[1] <= 120 else 0
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

        for obj in cell_list + wall_list:
            if obj.position in pos_list:
                pos_list.remove(obj.position)
        if pos_list:
            child = Cell(random.choice(pos_list), self.dna, color=[x//2 for x in self.color])
            child.health = self.health
            if not random.randint(0, 4):
                child.dna = self.evolve()
            else:
                child.generation = self.generation + 1
            cell_list.append(child)
        else:
            self.is_alive = False
        self.gene_jump(1)

    def evolve(self):
        dna = self.dna[:]
        dna[random.randint(0, 63)] = random.randint(0, 63)

        return dna

    def live(self, distance, cell_list=None, meat_list=None):
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
                    self.look(gene, cell_list, meat_list)
                case gene if 24 <= gene <= 62:
                    self.gene_jump(gene)
                case 63:
                    y = self.position[1]
                    match y:
                        case y if 32 >= y >= 25:
                            self.photosynthesis(2)
                        case y if 24 >= y >= 20:
                            self.photosynthesis(1.5)
                        case y if 19 >= y >= 10:
                            self.photosynthesis(1)

            self.health -= 1
        else:
            self.is_alive = False
