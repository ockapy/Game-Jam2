import pygame

class Entity : 

    def __init__(self , asset, x, y, direction) -> None:
        self.asset = pygame.image.load(asset).convert_alpha()
        self.skin = self.asset.subsurface(pygame.Rect(0,0,16,32))
        self.rect = self.skin.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.countSteps = 0
        self.countFrame = 0

    def get_asset(self) -> pygame.Surface :
        return self.asset

    def get_position(self) -> tuple[int,int]: 
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x, y) -> None : 
        self.rect.x = x
        self.rect.y = y

    def set_direction(self, direction) -> None : 
        self.direction = direction

    def get_direction(self) -> str: 
        return self.direction
    
    def animation_entity(self) -> None : 
        if self.direction == "right":
            self.skin = self.asset.subsurface(pygame.Rect(16*(self.countSteps % 4),0,16,32))
        elif self.direction == "left" : 
            self.skin = pygame.transform.flip(self.asset.subsurface(pygame.Rect(16*(self.countSteps % 4),0,16,32)),180,0) 
        self.countFrame += 1 
        if (self.countFrame % 16 == 15) : self.countSteps +=1

    def update(self):
        self.set_direction("left")
        self.animation_entity()
    
    def render(self, screen):
        skin = pygame.transform.scale(self.skin, (self.skin.get_width() * 2, self.skin.get_height()*2))
        screen.blit(skin, self.get_position())

        
