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
        self.visibility = False

    def get_w(self):
        return self.rect.w

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self) -> str: 
        return self.direction

    def set_visibility(self, bool):
        self.visibility = bool

    def is_show(self):
        return self.visibility

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.annimation_wind()

    def add_x(self, x):
        self.rect.x += x

    def add_y(self, y):
        self.rect.y += y


    def annimation_wind(self):
        if self.direction == "right":
            self.wind = self.asset.subsurface(pygame.Rect(48*(self.countWind % 4),0,48,31))
        elif self.direction == "left" : 
            self.wind = pygame.transform.flip(self.asset.subsurface(pygame.Rect(48*(self.countWind % 4),0,48,31)),180,0) 
        self.countFrame += 1 
        if (self.countFrame % 16 == 15) : self.countWind +=1
        if self.countWind % 4 == 3 : 
            self.visibility == False
            self.countFrame = 0
            self.countWind = 0

    def render(self, screen, server_size) : 
        scaleX = screen.get_width() / server_size[0]
        scaleY = screen.get_height() / server_size[1]

        wind = pygame.transform.scale(self.wind, (self.rect.w *scaleX,self.rect.h*scaleY))

        posX = self.rect.x * scaleX
        posY = self.rect.y * scaleY        

        screen.blit(wind, (posX,posY))


