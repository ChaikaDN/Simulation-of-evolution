from object import Object
import random


class Meat(Object):
    def __init__(self, position):
        super().__init__(position, color=[200, 0, 0])
        self.health = random.randint(40, 60)
        self.is_alive = True

    def live(self):
        self.health -= 0.2
        if self.health <= 0:
            self.is_alive = False
