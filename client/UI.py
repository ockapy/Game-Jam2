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

class Event():
    NONE=pygame.event.custom_type()


class Label(pygame.sprite.Sprite):
    def __init__(self,pos,dim,color,group,cb_input=None,text="",fontsize=32,textcolor="black",texture=None,hidden=False) -> None:
        super().__init__(group)
        self.hidden=hidden

        if cb_input!=None:
            self.cb_input=cb_input[0]
            self.cb_input_arg=cb_input[1]

        self.text=text
        self.textcolor=textcolor
        self.pos=pos

        if texture !=None:
            self.texture = pygame.image.load(texture)
            self.texture = pygame.transform.scale(self.texture,(dim[0],dim[1]))
        else :
            self.texture=pygame.Surface(dim)
            self.texture.fill(color)

        self.rect=self.texture.get_rect()

        self.font=pygame.font.Font(None, fontsize)
        text_render=self.font.render(self.text,False,self.textcolor)
        self.image=self.texture.copy()
        self.image.blit(text_render,((self.rect.w-text_render.get_width() )/2,(self.rect.h-text_render.get_height() )/2))

        ws=pygame.display.get_window_size()
        self.rect.topleft=( (ws[0] *self.pos[0]/100 ) - self.rect.width/2,(ws[1] *self.pos[1]/100 ) - self.rect.height/2)

    def update(self,event) -> None:

        if self.cb_input!=None:
            if self.cb_input_arg!=None:
                self.text=str(self.cb_input(self.cb_input_arg))
            else:
                self.text=str(self.cb_input())
            

        text_render=self.font.render(self.text,False,self.textcolor)

        self.image=self.texture.copy()
        self.image.blit(text_render,((self.rect.w-text_render.get_width() )/2,(self.rect.h-text_render.get_height() )/2))

        ws=pygame.display.get_window_size()
        self.rect.topleft=( (ws[0] *self.pos[0]/100 ) - self.rect.width/2,(ws[1] *self.pos[1]/100 ) - self.rect.height/2)


class Button(Label):
    def __init__(self,pos,dim,color,group,callback,text="",fontsize=32,textcolor="black" ,texture=None ,disable=False) -> None:
        super().__init__(pos,dim,color,group,None,text,fontsize,textcolor,texture)
        if callback!=None:
            self.callback=callback[0]
            self.callback_arg=callback[1]

        self.disable=disable

    def enable(self,bool=True):
        self.disable = not bool

    def update(self,event) -> None: 

        #position
        ws=pygame.display.get_window_size()
        self.rect.topleft=( (ws[0] *self.pos[0]/100 ) - self.rect.width/2,(ws[1] *self.pos[1]/100 ) - self.rect.height/2)

        # if self.rect.collidepoint(pygame.mouse.get_pos()): # :over
        #     self.image=self.
        # else:
        #     self.image=self.texture

        if event.type == pygame.MOUSEBUTTONDOWN: #on click event
            if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.disable:
                if self.callback_arg!=None:
                    self.callback(self.callback_arg)
                else:
                    self.callback()

class Input(Button):
        
    def __init__(self,pos,dim,color,group,callback,text=None,fontsize=32 ,textcolor="grey",input_textcolor="black",texture=None,texture_alt=None,) -> None:
        super().__init__(pos,dim,color,group,None,text,fontsize,textcolor ,texture)

        self.focused=False
        self.input_text=""
        self.input_textcolor=input_textcolor
        self.callback=callback[0]

        if texture_alt !=None:
            self.texture_alt = pygame.image.load(texture_alt)
            self.texture_alt = pygame.transform.scale(self.texture_alt,(dim[0],dim[1]))
        else :
            self.texture_alt=pygame.Surface(dim)
            self.texture_alt.fill(color)

    
    def update(self, event) -> None:
        #super().update(events)

        #on click : set/unset focus
        if event.type == pygame.MOUSEBUTTONDOWN:
            if  self.rect.collidepoint(pygame.mouse.get_pos()):
                self.focused=True
                pygame.key.set_repeat(300,50)
            else:
                self.focused=False
                pygame.key.set_repeat(0)

            self.render_text()

        # on key pressed
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:

                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN :
                self.callback()
            else:   
                self.input_text += event.unicode

            self.render_text()
        
        ws=pygame.display.get_window_size()
        self.rect.topleft=( (ws[0] *self.pos[0]/100 ) - self.rect.width/2,(ws[1] *self.pos[1]/100 ) - self.rect.height/2)

    
    def render_text(self):
            if self.focused:  #select input texture
                self.image=self.texture_alt.copy()
            else:
                self.image=self.texture.copy()                         
            #render the text 
            text_render=self.font.render((self.input_text if len(self.input_text)!=0 or self.focused else self.text),False,self.input_textcolor if len(self.input_text)!=0  else self.textcolor)
            padding=(self.rect.h-text_render.get_height() )/2
            if text_render.get_width() > self.rect.w - 2*padding: #handle text overflow
                self.image.blit(text_render,(-text_render.get_width() + self.rect.w - padding,padding))
            else:
                self.image.blit(text_render,(padding,padding))


    def get_text(self):
        return self.input_text

class Audio_Manager():
    def __init__(self) -> None:
        self.sound_volume=1.0
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

    def get_sound_volume(self,rounded=False):
        if not rounded:
            return self.sound_volume
        return round(self.sound_volume*10)

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

    def get_music_volume(self,rounded=False):
        if not rounded:
            return self.music_volume
        return round( self.music_volume*10)
    
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
        pygame.event.post(pygame.event.Event(Event.NONE))
        self.handle_event()

    def quit_connect(self):
        self.menu=Menu.MAIN
        self.client.disconnect_server()

    def connect_to_serverip(self):
        self.client.connect_server( self.input["ADDRESS"].get_text())

    def start_game(self):
        self.menu=Menu.GAME
        self.client.start_game()

    #init objects to display on the spec. menu
    def init_main(self):
        Button((50,40),(150,40),"black",self.main_sprites,(self.set_menu,Menu.CONNECTION),"Play !",32,"yellow","./Assets/UI/button1.png")
        Button((50,50),(150,40),"black",self.main_sprites,(self.set_menu,Menu.SETTINGS),"Settings",32,"yellow","./Assets/UI/button1.png")

    def init_connection(self):
        Button((10,10),(150,40),"red",self.connection_sprites,(self.quit_connect,None),"back",texture="./Assets/UI/button1.png")
        #address input
        self.input["ADDRESS"] = Input((35,50),(260,40),"red",self.connection_sprites,(self.connect_to_serverip,None),"IP Address",texture="./Assets/UI/textinput-off1.png",texture_alt= "./Assets/UI/textinput-on1.png")
        Button((65,50),(150,40),"red",self.connection_sprites,(self.connect_to_serverip,None),"Connect",texture="./Assets/UI/button1.png")

        self.startbutton=Button((60,60),(150,40),"red",self.connection_sprites,(self.start_game,None),"Start !",texture="./Assets/UI/button1.png",disable=True)
      
    def init_settings(self):
        Button((10,10),(150,40),"red",self.settings_sprites,(self.set_menu,Menu.MAIN),"back",texture="./Assets/UI/button1.png")
        #music
        Button((40,30),(60,50),"red",self.settings_sprites,(self.audio_manager.decrease_music_volume,None),"-",texture="./Assets/UI/button1.png")
        Button((60,30),(60,50),"red",self.settings_sprites,(self.audio_manager.increase_music_volume,None),"+",texture="./Assets/UI/button1.png")
        Label((50,30),(50,50),"red",self.settings_sprites,(self.audio_manager.get_music_volume,True))
        #sound
        Button((40,40),(60,50),"red",self.settings_sprites,(self.audio_manager.decrease_sound_volume,None),"-",texture="./Assets/UI/button1.png")
        Button((60,40),(60,50),"red",self.settings_sprites,(self.audio_manager.increase_sound_volume,None),"+",texture="./Assets/UI/button1.png")
        Label((50,40),(50,50),"red",self.settings_sprites,(self.audio_manager.get_sound_volume,True))


    def __init__(self, client ) -> None:

        pygame.init()

        self.client=client #bidirectionnal association
        self.audio_manager=Audio_Manager()
        self.menu=Menu.MAIN #actual menu displayed

        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE )
        self.clock= pygame.time.Clock()


        #objects group by menu
        self.main_sprites = pygame.sprite.Group()
        self.connection_sprites = pygame.sprite.Group()
        self.settings_sprites = pygame.sprite.Group()
        self.input={}

        self.background=pygame.image.load("./Assets/UI/background1.png")

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
        self.main_sprites.draw(self.screen)

    def render_connection(self):
        self.connection_sprites.draw(self.screen)

        if self.client.get_state() == Client.ClientState.WAIT_CON:
            surface=pygame.Surface((150,40*4+4))
            surface.fill("grey")
            if self.client.is_connected():
                self.startbutton.enable(True)
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

            self.screen.blit(surface,(pygame.display.get_window_size()[0]*0.30,pygame.display.get_window_size()[1]*0.6))

    def render_settings(self):
        self.settings_sprites.draw(self.screen)     

    def render(self):
        # Rendu varié
        self.screen.fill("azure")
        self.screen.blit(pygame.transform.scale(self.background,pygame.display.get_window_size()),(0,0))

        match self.menu :
            case Menu.MAIN:
                self.render_main()
            case Menu.CONNECTION:
                self.render_connection()
            case Menu.SETTINGS:
                self.render_settings()
            case Menu.GAME:
                self.client.game.render(self.screen)
                pass

        pygame.display.flip()

        self.clock.tick(60) #max x loop per second

        