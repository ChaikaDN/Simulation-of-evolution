import pygame


class Text:
    def __init__(self, message, position, font_size):
        self.font_size = font_size
        self.position = position
        self.font = pygame.font.SysFont('Impact', self.font_size)
        self.text = self.font.render(message, True, (0, 0, 0))
        self.background_rect = self.text.get_rect()
        # self.position_center = [x1 - x2 for x1, x2 in zip(self.position, self.background_rect.center)]
        self.background_rect.center = self.position


    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), self.background_rect)
        screen.blit(self.text, self.position)

