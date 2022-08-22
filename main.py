import random
from text_drawer import Text
from cell import Cell
from meat import Meat
import pygame as pg
import pygame.gfxdraw


class App:
    def __init__(self, pixel_size=30, pixel_count=32, panel_size=400):
        pg.init()
        self.FPS = 30
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
                           (x + (self.PIXEL_SIZE - size) / 2, y + (self.PIXEL_SIZE - size) / 2, size, size),
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
                    if event.key == pg.K_1:
                        self.FPS = 5
                    elif event.key == pg.K_2:
                        self.FPS = 15
                    elif event.key == pg.K_3:
                        self.FPS = 30
                    elif event.key == pg.K_4:
                        self.FPS = 60
                    elif event.key == pg.K_SPACE:
                        self.paused()

            self.draw_field()
            # for grass in grass_list:
            #     self.draw_obj(grass, self.PIXEL_SIZE/1.5)
            for meat in list(meat_list):
                self.draw_obj(meat, self.PIXEL_SIZE / 1.5)
                meat.live()
                if not meat.is_alive:
                    meat_list.remove(meat)

            for cell in list(cell_list):
                self.draw_obj(cell, self.PIXEL_SIZE - 2)

                tmp = cell.position
                cell.live(self.PIXEL_COUNT, cell_list, meat_list)
                cell.position = tmp if cell.check_collision(cell_list) else cell.position

                for food in meat_list:  # + grass_list + ...
                    if cell.is_collide(food):
                        cell.eat(food)

                if cell.is_ready_to_divide:
                    cell.divide(self.PIXEL_COUNT, cell_list)
                if not cell.is_alive:
                    meat_list.append(Meat(cell.position))
                    cell_list.remove(cell)

            messages = [Text(f'Cell count:  {len(cell_list)}', (self.WIDTH + 30, 15), 25)]
            if cell_list:
                messages.append(Text('Oldest cell genome:', (self.WIDTH + 30, 60), 25))
                pos_y = 95
                # for i, gene in enumerate(cell_list[0].dna):
                #     messages.append(Text(f'{gene} ', (self.WIDTH - 10 + 40 * (i % 8 + 1), pos_y + 35 * (i // 8)), 25))
                messages.append(Text(f'Max generation: {max(cell_list, key=lambda x: x.generation).generation}',
                                     (self.WIDTH + 30, 385), 25))

            for message in messages:
                message.draw(self.surface)
            pg.display.set_caption(f'FPS: {str(self.clock.get_fps())}')
            pg.display.flip()
            self.clock.tick(self.FPS)

    def paused(self):
        m = Text('Paused', (self.WIDTH + 300, 15), 25)
        while True:
            m.draw(self.surface)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return
            pg.display.flip()

if __name__ == '__main__':
    app = App()
    app.run()
