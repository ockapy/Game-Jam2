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
        self.velocity = 3

    def get_rect(self):
        return self.rect

    def get_velocity(self):
        return self.velocity

    def get_asset(self) -> pygame.Surface :
        return self.asset

    def get_position(self) -> tuple[int,int]: 
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x, y) -> None : 

        if x >= self.rect.x:
            self.set_direction("right")
        else:
            self.set_direction("left")

        self.rect.x = x
        self.rect.y = y
        self.animation_entity()

    def add_x(self, x):
        move = x*self.velocity           
        
        if move < 0:
            self.set_direction("left")
        else: 
            self.set_direction("right")

        self.rect.x += x * self.velocity
        self.animation_entity()

    def add_y(self, y):
        self.rect.y += y * self.velocity
        self.animation_entity()

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
      
    
    def render(self, screen):
        skin = pygame.transform.scale(self.skin, (self.skin.get_width() * 2, self.skin.get_height()*2))
        screen.blit(skin, self.get_position())


    def moveTo(self) : 
        if(self.direction=='right'):
            self.rect.x += self.velocity
        elif(self.direction=='left'):
            self.rect.x -= self.velocity
        self.animation_entity()

