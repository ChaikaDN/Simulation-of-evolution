def check_obj_type(obj=None):
    return 'Nothing' if obj is None else str(type(obj)).split('.')[1][:-2]


def add_coords(position1, position2, mod=None):
    return tuple(map(lambda x, y: x + y, position1, position2)) if mod is None else \
        tuple(map(lambda x, y: (x + y) % mod, position1, position2))


class Object:
    dirlist = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self, position, color=None):
        if color is None:
            color = [0, 0, 0]
        self.color = color
        self.position = position

    def is_neighbor(self, obj):
        return add_coords(self.position, -obj.position) in self.dirlist

    def check_near_position(self, obj_list):
        pass

    def check_collision(self, obj_list):
        for obj in obj_list:
            if self.is_collide(obj):
                return obj

    def is_collide(self, obj):
        return self.position == obj.position and self is not obj