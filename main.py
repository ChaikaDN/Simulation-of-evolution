import random
# from grass import Grass
from cell import Cell
from meat import Meat
import pygame as pg
import pygame.gfxdraw


class App:
    def __init__(self, pixel_size=15, pixel_count=64, panel_size=400):
        pg.init()
        self.PIXEL_SIZE = pixel_size
        self.PIXEL_COUNT = pixel_count
        self.PANEL_SIZE = panel_size
        self.FIELD_RES = self.WIDTH, self.HEIGHT = self.PIXEL_SIZE * self.PIXEL_COUNT, self.PIXEL_SIZE * self.PIXEL_COUNT
        self.RES = self.WIDTH + self.PANEL_SIZE, self.HEIGHT
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

    def draw_field(self):
        self.surface.fill('grey')
        pygame.gfxdraw.box(self.surface, (self.WIDTH, 0, self.PANEL_SIZE, self.HEIGHT), (128, 128, 128))

    def draw_obj(self, obj, size):
        self.draw_pixel(obj.position[0] * self.PIXEL_SIZE, obj.position[1] * self.PIXEL_SIZE, size, obj.color)

    def draw_pixel(self, x, y, size, color=(0, 0, 0)):
        pygame.gfxdraw.box(self.surface,
                           (x+(self.PIXEL_SIZE-size)/2, y+(self.PIXEL_SIZE-size)/2, size, size),
                           color)

    def run(self):
        # grass_list = [Grass((random.randint(0, self.PIXEL_COUNT-1),
        #                      random.randint(0, self.PIXEL_COUNT-1))) for _ in range(64)]
        grass_list = []
        cell_list = [Cell((random.randint(0, self.PIXEL_COUNT - 1),
                           random.randint(0, self.PIXEL_COUNT - 1)),
                          [63 for _ in range(64)]) for _ in range(64)]
        meat_list = []

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        pass

            self.draw_field()

            for grass in grass_list:
                self.draw_obj(grass, self.PIXEL_SIZE/1.5)
            for meat in list(meat_list):
                self.draw_obj(meat, self.PIXEL_SIZE/1.5)
                meat.live(meat_list)

            for cell in list(cell_list):

                for c in list(cell_list):  # костыль!
                    if c.position == cell.position and c is not cell:
                        c.is_alive = False
                self.draw_obj(cell, self.PIXEL_SIZE-2)

                tmp = cell.position
                cell.live(self.PIXEL_COUNT, cell_list, grass_list, meat_list)
                cell.position = tmp if cell.check_collision(cell_list) else cell.position

                collided_grass = cell.check_collision(grass_list)
                collided_meat = cell.check_collision(meat_list)

                if collided_grass:
                    cell.health += 50

                    cell.color[0] -= 5 if cell.color[0] >= 5 else 0
                    cell.color[1] -= 5 if cell.color[1] >= 5 else 0
                    cell.color[2] += 5 if cell.color[2] <= 150 else 0

                    grass_list.remove(collided_grass)

                if collided_meat:
                    cell.health += 70

                    cell.color[0] += 5 if cell.color[0] <= 150 else 0
                    cell.color[1] -= 5 if cell.color[1] >= 5 else 0
                    cell.color[2] -= 5 if cell.color[2] >= 5 else 0

                    meat_list.remove(collided_meat)

                if cell.is_ready_to_divide:
                    cell.divide(self.PIXEL_COUNT, cell_list)

                if not cell.is_alive:
                    meat_list.append(Meat(cell.position))
                    cell_list.remove(cell)

            pg.display.set_caption(f'{len(cell_list)} | {str(self.clock.get_fps())}')
            pg.display.flip()
            self.clock.tick(30)


if __name__ == '__main__':
    app = App()
    app.run()
