from enum import Enum
import pygame

import Client

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

class Menu(Enum):
    MAIN=0
    CONNECTION=1
    GAME=2
    SETTINGS=3

class Button(pygame.sprite.Sprite):
    def __init__(self,pos,dim,color,callback,group,text=None,textcolor="black" ,texture=None) -> None:
        super().__init__(group)
        if callback!=None:
                self.callback=callback[0]
                self.callback_arg=callback[1]
        
        self.text=text
        self.textcolor=textcolor

        if texture !=None:
            self.texture=pygame.image.load(texture)
        else :
            self.texture=pygame.Surface(dim)
            self.texture.fill(color)

        self.image=self.texture.copy()
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]

        font=pygame.font.Font(None, 32)
        text_render=font.render(self.text,False,self.textcolor)
        self.image.blit(text_render,((self.rect.w-text_render.get_width() )/2,(self.rect.h-text_render.get_height() )/2))


    def update(self,event) -> None:  #on click event

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.callback_arg!=None:
                    self.callback(self.callback_arg)
                else:
                    self.callback()

class Input(Button):
        
    def __init__(self,pos,dim,color,group,text=None ,textcolor="grey",input_textcolor="black",texture=None) -> None:
        self.focused=False
        self.input_text=""
        self.input_textcolor=input_textcolor
        print(len(self.input_text))

        super().__init__(pos,dim,color,None,group,text,textcolor ,texture)
    
    def update(self, event) -> None:
        #super().update(events)
        
        #on click : set/unset focus
        if event.type == pygame.MOUSEBUTTONDOWN:
            if  self.rect.collidepoint(pygame.mouse.get_pos()):
                self.focused=True
            else:
                self.focused=False
        # on key pressed
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:   
                self.input_text += event.unicode
    
            font=pygame.font.Font(None, 32) # font option (todo : set global setting)
            text_render=font.render((self.input_text if len(self.input_text)!=0  else self.text),False,self.input_textcolor if len(self.input_text)!=0  else self.textcolor)

            self.image=self.texture.copy()

            padding=(self.rect.h-text_render.get_height() )/2

            if text_render.get_width() > self.rect.w - 2*padding: #handle text overflow
                self.image.blit(text_render,(-text_render.get_width() + self.rect.w - padding,padding))
            else:
                self.image.blit(text_render,(padding,padding))

    def get_text(self):
        return self.input_text

class Audio_Manager():
    def __init__(self) -> None:
        self.ch_volume=1.0
        self.music_volume=1.0
        self.mute=False

        # self.sounds_list=Client.loader.loadCsv('./sounds/list.txt')
        # self.music_list=Client.loader.loadCsv('./music/list.txt')
        # self.sounds =dict()
        # for i in range(len(KEY_SET)):  # charge les sons
        # try:
        #     self.sounds[KEY_SET[i] ] = pygame.mixer.Sound('./sounds/' + self.sounds_list[0][i])
        # except:
        #     pass

    def get_sound_volume(self):
        return self.sound_volume

    def set_sound_volume(self,volume):
        if volume >=0 and volume<=1:
            self.sound_volume=volume
            pygame.mixer.music.set_volume(self.music_volume)

    def increase_sound_volume(self):
        self.set_sound_volume(self.sound_volume+0.1)

    def decrease_sound_volume(self):
        self.set_sound_volume(self.sound_volume-0.1)

    def play_sound(self,id):
        pass

    def stop_sound(self,id):    
        pass

    def get_music_volume(self):
        return self.music_volume
    
    def set_music_volume(self,volume):
        if volume >=0 and volume<=1:
            self.music_volume=volume
            pygame.mixer.music.set_volume(self.music_volume)

    def increase_music_volume(self):
        self.set_music_volume(self.music_volume+0.1)

    def decrease_music_volume(self):
        self.set_music_volume(self.music_volume-0.1)

    def play_music(self,id):
        pass

    def play_random_music(self):
        pass

    def proto_play_music(self,src="./Assets/Audios/Musics/Vivaldi_4Seasons_ Spring.mp3"):

        pygame.mixer.music.load(src)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(self.music_volume)
        pass

    def stop_music(self,id):
        pass
    
    def queue_music(self,id):
        pass

class UI():

    def set_menu(self, menu):
        self.menu=menu

    def quit_connect(self):
        self.menu=Menu.MAIN
        self.client.disconnect_server()

    def connect_to_serverip(self):
        self.client.connect_server( self.input["ADDRESS"].get_text())

    #init objects to display on the spec. menu
    def init_main(self):
        Button((SCREEN_WIDTH/3,SCREEN_HEIGHT/2),(150,40),"black",(self.set_menu,Menu.CONNECTION),self.main_sprites,"play !","yellow")
        Button((SCREEN_WIDTH/3,SCREEN_HEIGHT/1.5),(150,40),"black",(self.set_menu,Menu.SETTINGS),self.main_sprites,"SETTINGS","yellow")


    def init_connection(self):
        Button((SCREEN_WIDTH/8,SCREEN_HEIGHT/8),(150,40),"red",(self.quit_connect,None),self.connection_sprites,"back")
        #address input
        self.input["ADDRESS"] = Input((SCREEN_WIDTH/3,SCREEN_HEIGHT/3),(200,40),"red",self.connection_sprites,"IP Address")
        Button((SCREEN_WIDTH*2/3,SCREEN_HEIGHT/3),(150,40),"red",(self.connect_to_serverip,None),self.connection_sprites,"Connect")
      
    def init_settings(self):
        Button((SCREEN_WIDTH/8,SCREEN_HEIGHT/8),(150,40),"red",(self.set_menu,Menu.MAIN),self.settings_sprites,"back")
        #music
        Button((SCREEN_WIDTH/6,SCREEN_HEIGHT/3),(50,50),"red",(self.audio_manager.decrease_music_volume,None),self.settings_sprites,"- m")
        Button((SCREEN_WIDTH/3,SCREEN_HEIGHT/3),(50,50),"red",(self.audio_manager.increase_music_volume,None),self.settings_sprites,"+ m")
        #sound
        Button((SCREEN_WIDTH/6,SCREEN_HEIGHT/2),(50,50),"red",(self.audio_manager.decrease_sound_volume,None),self.settings_sprites,"- m")
        Button((SCREEN_WIDTH/3,SCREEN_HEIGHT/2),(50,50),"red",(self.audio_manager.increase_sound_volume,None),self.settings_sprites,"+ m")
      

    def __init__(self, client ) -> None:

        pygame.init()

        self.client=client #bidirectionnal association
        self.audio_manager=Audio_Manager()
        self.menu=Menu.MAIN #actual menu displayed

        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
        self.clock= pygame.time.Clock()

        #objects group by menu
        self.main_sprites = pygame.sprite.Group()
        self.connection_sprites = pygame.sprite.Group()
        self.settings_sprites = pygame.sprite.Group()
        self.input={}

        self.init_main()
        self.init_connection()
        self.init_settings()

        #self.audio_manager.proto_play_music()


    def handle_event(self) -> bool :
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            match self.menu :
                case Menu.MAIN:
                    self.main_sprites.update(event)
                case Menu.CONNECTION:
                    self.connection_sprites.update(event)
                case Menu.SETTINGS:
                    self.settings_sprites.update(event)
                case Menu.GAME:
                    pass
                    
        return True

    def render_main(self):
        self.screen.fill("green")
        self.main_sprites.draw(self.screen)

    def render_connection(self):
        self.screen.fill("blue")
        self.connection_sprites.draw(self.screen)

        if self.client.get_state() == Client.ClientState.WAIT_CON:
            surface=pygame.Surface((150,40*4+4))
            surface.fill("grey")
            if self.client.is_connected():
            #display the player list  !PROTOTYPE!

                #players = self.client.getplayers()
                players= ["joueur 1 ", "joueur 2","joueur 3"]  #line for test purpose only

                y=0
                for player in players:
                    srfce=pygame.Surface((150,40))
                    srfce.fill("white")
                    font=pygame.font.Font(None, 25) # font option (todo : set global setting)

                    text=font.render(player,False,"black")
                    
                    srfce.blit(text,((srfce.get_height()-text.get_height())/2,(srfce.get_height()-text.get_height())/2))
                    
                    surface.blit(srfce,(0,y))
                    y+=40

            else:
                font=pygame.font.Font(None, 40) # font option (todo : set global setting)

                if (pygame.time.get_ticks()%1000 < 250 ):
                    text=font.render("/",False,"black")
                elif (pygame.time.get_ticks()%1000 < 500):
                    text=font.render("-",False,"black")
                elif (pygame.time.get_ticks()%1000 < 750):
                    text=font.render("\\",False,"black")
                else:
                    text=font.render("|",False,"black")

                surface.blit(text,((surface.get_width()-text.get_width())/2,(surface.get_height()-text.get_height())/2))

            self.screen.blit(surface,(SCREEN_WIDTH*0.4,SCREEN_HEIGHT*0.5))

    def render_settings(self):
        self.screen.fill("blue")
        self.settings_sprites.draw(self.screen)     

        music_volume_surface=pygame.Surface((50,50))
        music_volume_surface.fill("grey")
        
        font=pygame.font.Font(None, 25) # font option (todo : set global setting)
        music_volume_text=font.render(str(round(self.audio_manager.music_volume*10)),False,"black")
        music_volume_surface.blit(music_volume_text,((music_volume_surface.get_width()-music_volume_text.get_width())/2,(music_volume_surface.get_height()-music_volume_text.get_height())/2))
        self.screen.blit(music_volume_surface,(SCREEN_WIDTH/4,SCREEN_HEIGHT/3))

    def render(self):
        match self.menu :
            case Menu.MAIN:
                self.render_main()
            case Menu.CONNECTION:
                self.render_connection()
            case Menu.SETTINGS:
                self.render_settings()
            case Menu.GAME:
                    
                pass

        pygame.display.flip()

        self.clock.tick(20) #max x loop per second

        