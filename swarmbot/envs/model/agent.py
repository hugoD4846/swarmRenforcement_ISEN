import math
import random
import pygame
from .entity import Entity

AGENT_VISION_COLOR = "#6b592b"
AGENT_VISION_COLOR_SUCCESS = "#f1c40f"
AGENT_COLOR = "#e74c3c"

class Agent(Entity):
    AGENT_VISION_SIZE = 100
    AGENT_VISION_ANGLE = 60
    AGENT_VISION_COLOR = "#6b592b"
    AGENT_VISION_COLOR_SUCCESS = "#f1c40f"

    def __init__(self, entity_id: int, x: int, y: int) -> None:
        super().__init__(entity_id, x, y, AGENT_COLOR)
        self.angle = random.randint(0, 360)
        self.know_target_position = False
        self.is_out_of_bound = False

    def move(self, v_angle, speed):
        self.angle = ((self.angle + v_angle) + 360) % 360.0
        vx = math.cos(self.angle * (math.pi / 180)) * speed
        vy = math.sin(self.angle * (math.pi / 180)) * speed
        self.x += vx
        self.y += vy

    def render_vision(self, game):
        p = [(self.x, self.y)]

        # Get points on arc
        for n in range(int(self.angle - self.AGENT_VISION_ANGLE / 2),int(self.angle + self.AGENT_VISION_ANGLE - self.AGENT_VISION_ANGLE / 2)):
            x = self.x + int(self.AGENT_VISION_SIZE*math.cos(n*math.pi/180))
            y = self.y + int(self.AGENT_VISION_SIZE*math.sin(n*math.pi/180))
            p.append((x, y))
        p.append((self.x, self.y))

        if len(p) > 2:
            agent_vision_flag = False
            for entity in game.entities:
                if entity.entity_id is self.entity_id:
                    continue
                agent_vision_flag = self.is_in_vision(entity)
                if agent_vision_flag is True:
                    break
            target_vision_flag = self.is_in_vision(game.target)
            ray_color = AGENT_VISION_COLOR_SUCCESS if agent_vision_flag or target_vision_flag else AGENT_VISION_COLOR
            pygame.draw.polygon(game.window, ray_color, p)

    def render(self, game):
        self.render_vision(game)
        super().render(game)

    def attack(self, game):
        if self.is_in_vision(game.target):
            game.target.health -= 1

    def get_dist_with_entity(self, entity : Entity):
        return ((self.x - entity.x)**2+(self.y - entity.y)**2)**.5

    def get_angle_with_entity(self, entity : Entity):
        return  180 + math.atan2((self.y - entity.y),(self.x - entity.x)) * (180/math.pi)

    def is_in_vision(self, entity : Entity):
        if self.get_dist_with_entity(entity) < self.AGENT_VISION_SIZE + super().ENTITY_SIZE:
            colision_angle = self.get_angle_with_entity(entity)
            low_colision_angle = colision_angle - 360
            high_colision_angle = colision_angle + 360
            return (
                (self.angle - self.AGENT_VISION_ANGLE/2) <= colision_angle <= (self.angle + self.AGENT_VISION_ANGLE/2)
                or
                (self.angle - self.AGENT_VISION_ANGLE/2) <= low_colision_angle <= (self.angle + self.AGENT_VISION_ANGLE/2)
                or
                (self.angle - self.AGENT_VISION_ANGLE/2) <= high_colision_angle<= (self.angle + self.AGENT_VISION_ANGLE/2)
            )
        return False
