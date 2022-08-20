class Object:
    dirlist = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self, position):
        self.position = position
        self.is_alive = True
        # self.direction = Object.dirlist[0]

    # def check_neighbor_type(self, obj):  # возвращает тип объекта по соседству относительно position или None
    #     return obj.objtype if self.is_neighbor(obj) else None
    #
    def is_neighbor(self, obj):
        return tuple(x - y for x, y in zip(self.position, obj.position)) in self.dirlist
    #
    # def check_collision(self, obj):  # возвращает True / False
    #     return self.position == obj.position

    def check_near_position(self, objs):
        neighbors = []
        for obj in objs:
            for direction in self.dirlist:
                if tuple(sum(i) for i in zip(self.position, direction)) == obj.position:
                    neighbors.append(obj)
                    if len(neighbors) == 8:  # проверить
                        return neighbors
        return neighbors
