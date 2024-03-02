import pygame
import math
from Constants import *
from Enemy import *
from Functions import *

class Player(pygame.sprite.Sprite):
    def __init__(self, vel, max_health, max_ammo):
        super().__init__()
        self.images = {
            "still_forward": pygame.image.load('Assets/Astronaut/Player_stillForward.png'),
            "still_left": pygame.image.load('Assets/Astronaut/Player_stillLeft.png'),
            "still_right": pygame.image.load('Assets/Astronaut/Player_stillRight.png'),
            "still_up": pygame.image.load('Assets/Astronaut/Player_stillUp.png'),
            "walking_forward_1": pygame.image.load('Assets/Astronaut/Player_walkingForward_1.png'),
            "walking_forward_2": pygame.image.load('Assets/Astronaut/Player_walkingForward_2.png'),
            "walking_up_1": pygame.image.load('Assets/Astronaut/Player_walkingUp_1.png'),
            "walking_up_2": pygame.image.load('Assets/Astronaut/Player_walkingUp_2.png'),
            "walking_left_1": pygame.image.load('Assets/Astronaut/Player_walkingLeft_1.png'),
            "walking_left_2": pygame.image.load('Assets/Astronaut/Player_walkingLeft_2.png'),
            "walking_right_1": pygame.image.load('Assets/Astronaut/Player_walkingRight_1.png'),
            "walking_right_2": pygame.image.load('Assets/Astronaut/Player_walkingRight_2.png')}
        
        self.current_image = self.images["still_forward"]
        self.rect = self.current_image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel = vel
        self.xp = 0
        self.health = max_health
        self.ammo = max_ammo
        self.max_health = max_health
        self.max_ammo = max_ammo
        self.original_vel = vel 
        self.enemies = pygame.sprite.Group()
        self.drops = []

    def update(self, keys):
        move_up = keys[pygame.K_w]
        move_down = keys[pygame.K_s]
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]

        # Boople said to use polar co-ordinates and im going to be systemically sick, and I am dumb.
        if move_up and not move_down:
            self.current_image = self.images["walking_up_1"]
            if move_left or move_right:
                self.rect.y -= math.sqrt(math.pow(self.vel,2) // 2)
            else:
                self.rect.y -= self.vel

        if move_down and not move_up:
            self.current_image = self.images["walking_forward_1"]   
            if move_left or move_right:
                self.rect.y += math.sqrt(math.pow(self.vel,2) // 2)
            else:
                self.rect.y += self.vel

        if move_left and not move_right:
            self.current_image = self.images["walking_left_1"]
            if move_up or move_down:
                self.rect.x -= math.sqrt(math.pow(self.vel,2) // 2)
            else:
                self.rect.x -= self.vel

        if move_right and not move_left:
            self.current_image = self.images["walking_right_1"]
            if move_up or move_down:
                self.rect.x += math.sqrt(math.pow(self.vel,2) // 2)
            else:
                self.rect.x += self.vel

        if not any([move_up, move_down, move_left, move_right]):
            self.current_image = self.images["still_forward"]

    #WHY THE FUCK ARE YOU NOT BEING CALLED?! #Get boople.
        print("cunt")
        for enemy in self.enemies:
            print(f"Player: ({self.rect.x}, {self.rect.y}), Enemy: ({enemy.rect.x}, {enemy.rect.y})")
            if self.rect.colliderect(enemy.rect):
                print("Collision Detected!")
                self.health -= 20
                drop = handle_drops(enemy.rect)
                self.drops.append(drop)
                enemy.kill()

        self.rect.x = max(0, min(self.rect.x, WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PLAYER_SIZE))