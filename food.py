import pygame
pygame.init()

# Food class
class Food:
    def __init__(self, x_food, y_food):
        self.x_food = x_food
        self.y_food = y_food

    def draw_food(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), (self.x_food, self.y_food), 5)