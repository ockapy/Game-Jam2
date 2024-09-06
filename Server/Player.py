import pygame

class Player:
    def __init__(self) -> None:
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.current_action = []

    def set_action(self, action: dict):
        self.current_action = action

    def update(self):
        for keycode in self.current_action:
            if keycode == pygame.K_d:
                print("lets go input reçu")
        
    
    def serialize(self) -> dict:
        return {"pos": [self.position.x, self.position.y]}