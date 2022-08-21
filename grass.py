from object import Object


class Grass(Object):
    def __init__(self, position):
        super().__init__(position, color=[0, 200, 0])
