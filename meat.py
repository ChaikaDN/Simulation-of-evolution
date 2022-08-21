from object import Object
import random


class Meat(Object):
    def __init__(self, position):
        super().__init__(position, color=[200, 0, 0])
        self.age = 0
        self.max_age = random.randint(100, 150)
        self.is_alive = True

    def live(self, meat_list):
        self.age += 1
        if self.age >= self.max_age:
            meat_list.remove(self)
