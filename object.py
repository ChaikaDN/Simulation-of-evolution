class Object:
    dirlist = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self, position):
        self.position = position
        self.is_alive = True
        # self.direction = Object.dirlist[0]

    def is_neighbor(self, obj):
        return tuple(x - y for x, y in zip(self.position, obj.position)) in self.dirlist

    def check_near_position(self, obj_list):
        neighbors = []
        for obj in obj_list:
            if self.is_neighbor(obj):
                neighbors.append(obj)
        return neighbors

    def check_collision(self, obj_list):
        for obj in obj_list:
            if self.is_collide(obj):
                return obj

    def is_collide(self, obj):
        return self.position == obj.position and self is not obj  # проверить второе условие
