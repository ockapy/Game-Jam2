import pygame


class Vfx() :

    def __init__(self, asset, x, y, direction) -> None:
        self.asset = pygame.image.load(asset).convert_alpha()
        self.wind = self.asset.subsurface(pygame.Rect(0,0,48,31))
        self.rect = self.wind.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

        self.countFrame = 0
        self.countWind = 0

    def annimation_wind(self):
        if self.direction == "right":
            self.skin = self.asset.subsurface(pygame.Rect(48*(self.countWind % 4),0,48,31))
            self.rect.x += 10
        elif self.direction == "left" : 
            self.skin = pygame.transform.flip(self.asset.subsurface(pygame.Rect(32*(self.countWind % 4),0,48,31)),180,0) 
            self.rect.x -= 10
        self.countFrame += 1 
        if (self.countFrame % 16 == 15) : self.countWind +=1

    def render(self, screen, server_size) : 
        scaleX = screen.get_width() / server_size[0]
        scaleY = screen.get_height() / server_size[1]

        wind = pygame.transform.scale(self.wind, (self.rect.w *scaleX,self.rect.h*scaleY))

        posX = self.rect.x * scaleX
        posY = self.rect.y * scaleY        

        screen.blit(wind, (posX,posY))

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(posX,posY,self.rect.w*scaleX,self.rect.h*scaleY), 1)

