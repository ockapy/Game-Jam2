import pygame
import time

class Player:
    GRAVITY = pygame.Vector2(0, 1200)
    JUMP_FORCE = pygame.Vector2(0, -30000)
    GROUND_ACCEL = 1400
    MAX_VELOCITY = 175
    FRICTION = 200

    ATTACK_DELAY = 0.5 #seconde
    def __init__(self, server) -> None:
        self.collide_box = pygame.Rect(400, 400, 32, 64)
        self.position = pygame.Vector2(400, 400)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.current_action = []

        self.other_force = []
        self.direction = pygame.Vector2(0, 0)

        self.attack_rect = pygame.Rect(0, 0, 50, 50)

        self.server = server

        self.__prev_tick_jump = False
        self.__last_attack_time = time.time()

    def set_action(self, action: dict):
        self.current_action = action

    def __reset_action(self):
        self.current_action = []
    
    def push(self, force: pygame.Vector2):
        self.other_force.append(force)

    def update(self, delta_time: float):
        self.collide_box.topleft = self.position.xy

        has_jumped = 0
        movement_direction = pygame.Vector2(0, 0)
        if pygame.K_d in self.current_action or pygame.K_RIGHT in self.current_action:
            #print("MOVE RIGHT")
            movement_direction.x = 1
        if pygame.K_q in self.current_action or pygame.K_LEFT in self.current_action:
            #print("MOVE LEFT")
            movement_direction.x = -1
        if pygame.K_z in self.current_action or pygame.K_UP in self.current_action:
            #print("JUMP")
            if not self.__prev_tick_jump:
                has_jumped = 1
            self.__prev_tick_jump = True
        elif len(self.current_action) == 0:
            self.__prev_tick_jump = self.__prev_tick_jump
        else:
            self.__prev_tick_jump = False

        if pygame.K_j in self.current_action:
            if time.time() - self.__last_attack_time >= Player.ATTACK_DELAY:
                if self.velocity.magnitude() != 0:
                    self.direction = self.velocity.normalize()
                else:
                    self.direction = pygame.Vector2(0, 0)
                
                # déplacement de la box de collision devant le joueur
                # la velocité marche a l'envers du sens pensé (vel > 0 vers la gauche et inversement)
                if self.velocity.x < 0:
                    self.attack_rect.left = self.collide_box.right
                elif self.velocity.x > 0:
                    self.attack_rect.right = self.collide_box.left
                else:
                    self.attack_rect.right = self.position.x
                self.attack_rect.y = self.collide_box.y

                for e in self.server.entities.values():
                    if e is not self and self.attack_rect.colliderect(e.collide_box):
                        e.push(-self.direction * 10_000 + pygame.Vector2(0, -1) * 50_000)

                self.__last_attack_time = time.time()
            
        if (pygame.K_q not in self.current_action) and (pygame.K_d not in self.current_action):
            if self.velocity.x > 0:
                self.velocity.x -= 7
                if self.velocity.x < 0:
                    self.velocity.x = 0

            elif self.velocity.x < 0:
                self.velocity.x += 7
                if self.velocity.x > 0:
                    self.velocity.x = 0


        # Methode de l'integration de verlet https://www.compadre.org/PICUP/resources/Numerical-Integration/
        sum_of_force = (Player.GRAVITY) \
            + (Player.JUMP_FORCE * has_jumped) \
            + (Player.GROUND_ACCEL * movement_direction) \
            + sum(self.other_force, pygame.Vector2(0, 0))

        average_velocity = self.velocity + self.acceleration * delta_time / 2.0

        self.position += average_velocity * delta_time
        self.acceleration = sum_of_force
        self.velocity = average_velocity + self.acceleration * delta_time / 2.0

        if self.velocity.x >= Player.MAX_VELOCITY:
            self.velocity.x = Player.MAX_VELOCITY

        elif self.velocity.x < -Player.MAX_VELOCITY:
            self.velocity.x = -Player.MAX_VELOCITY
        
        # Collision
        if self.position.y >= 500:
            self.position.y = 500
            self.velocity.y = 0
        
        #print("acc: ", self.acceleration, "\tvel", self.velocity)
        
        self.__reset_action()
        self.other_force = []
        
    
    def serialize(self) -> dict:
        return {"pos": [self.position.x, self.position.y]}