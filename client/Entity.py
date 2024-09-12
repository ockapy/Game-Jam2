import pygame
from enum import Enum

class EntityState(Enum):
    WALK = 0
    FIGHT = 1

class Entity : 

    def __init__(self , asset, x, y, direction, assetCombat) -> None:
        self.asset = pygame.image.load(asset).convert_alpha()
        self.assetCombat = pygame.image.load(assetCombat).convert_alpha()
        self.skin = self.asset.subsurface(pygame.Rect(0,0,32,48))
        self.combat = self.assetCombat.subsurface(pygame.Rect(0,0,32,48))
        self.rect = pygame.Rect(0,0,20,30)
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.countSteps = 0
        self.countFrame = 0
        self.velocity = 3
        self.countCombat = 0
        self.etat = EntityState.WALK
        
    def get_rect(self):
        return self.rect

    def get_velocity(self):
        return self.velocity

    def get_asset(self) -> pygame.Surface :
        return self.asset

    def get_position(self,server_size) -> tuple[int,int]:        
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
            self.skin = self.asset.subsurface(pygame.Rect(32*(self.countSteps % 4),0,32,48))
        elif self.direction == "left" : 
            self.skin = pygame.transform.flip(self.asset.subsurface(pygame.Rect(32*(self.countSteps % 4),0,32,48)),180,0) 
        self.countFrame += 1 
        
        if (self.countFrame % 16 == 15) : self.countSteps +=1
    
    def animation_fight(self):
        print(self.countCombat)
        if self.direction == "right":
            self.skin = self.assetCombat.subsurface(pygame.Rect(32*(self.countCombat % 4),0,32,48))
        elif self.direction == "left" : 
            self.skin = pygame.transform.flip(self.assetCombat.subsurface(pygame.Rect(32*(self.countCombat % 4),0,32,48)),180,0) 
        
        if self.countFrame % 8 == 7 : self.countCombat += 1
        if self.countCombat % 4 == 3 : self.etat = EntityState.WALK
        
    
    def render(self, screen,server_size):

        scaleX = screen.get_width() / server_size[0]
        scaleY = screen.get_height() / server_size[1]


        skin = pygame.transform.scale(self.skin, (self.rect.w*scaleX,self.rect.h*scaleY))

        posX = self.rect.x * scaleX
        posY = self.rect.y * scaleY        

        screen.blit(skin, (posX,posY))

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(posX,posY,self.rect.w*scaleX,self.rect.h*scaleY), 1)


    def set_etat(self, etat): 
        if etat == 'fight' : self.etat = EntityState.FIGHT
        else :  self.etat = EntityState.WALK 

    def get_etat(self):
        return self.etat
    
    def is_fighting(self):
        return self.etat == EntityState.FIGHT


