from GameEngine.GameManager import *
from GameEngine.ColorLib import BLACK, WHITE
import pygame

class Text:
    def __init__(self, text, position, font_size=30,  color=BLACK):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.pos = position
        mainCamera.objects_on_scene.append(self)

    def _PrepForFrame(self):
        pass

    def draw(self):  # uses to write some text on screen
        pygame.draw.rect(mainScreen, WHITE, [self.pos.x, self.pos.y, self.font_size * len(self.text), self.font_size], 0)
        font_type = pygame.font.Font(self.font_size, 10)  # '18177.otf', "19319.ttf" you can use these :D
        text = font_type.render(self.text, True, self.color)
        mainScreen.blit(text, [self.pos.x, self.pos.y])