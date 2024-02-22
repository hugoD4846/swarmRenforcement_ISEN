import pygame

class Entity():
    ENTITY_SIZE = 20
    def __init__(self, entity_id : int, x : int , y : int, color: str) -> None:
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.color = color

    def render(self, game):
        # Draw pie segment
        pygame.draw.circle(game.window, self.color, (self.x, self.y), self.ENTITY_SIZE)
