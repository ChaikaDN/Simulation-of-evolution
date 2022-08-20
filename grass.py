from object import Object


class Grass(Object):
    def __init__(self, position):
        super().__init__(position)
        self.color = (0, 128, 0)
