from .entity import Entity

TARGET_COLOR = "#2ecc71"

class Target(Entity):
    def __init__(self, entity_id: int, x: int, y: int) -> None:
        super().__init__(entity_id, x, y, TARGET_COLOR)
        self.health = 100

    def render(self, game):
        super().render(game)
        life_text = game.font.render(str(self.health), False, (0, 0, 0))
        game.window.blit(life_text, (0,0))
