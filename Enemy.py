import pygame
import random
from Functions import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size, vel):
        super().__init__()
        self.images = {
            "still_forward": pygame.image.load('Assets/Enemies/Alien/Alien-stillForward.png'),
            "still_left": pygame.image.load('Assets/Enemies/Alien/Alien-stillLeft.png'),
            "still_right": pygame.image.load('Assets/Enemies/Alien/Alien-stillRight.png'),
            "still_up": pygame.image.load('Assets/Enemies/Alien/Alien-stillUp.png'),
            "walking_forward_1": pygame.image.load('Assets/Enemies/Alien/Alien-walkingForward1.png'),
            "walking_forward_2": pygame.image.load('Assets/Enemies/Alien/Alien-walkingForward2.png'),
            "walking_up_1": pygame.image.load('Assets/Enemies/Alien/Alien-walkingUp1.png'),
            "walking_up_2": pygame.image.load('Assets/Enemies/Alien/Alien-walkingUp2.png'),
            "walking_left_1": pygame.image.load('Assets/Enemies/Alien/Alien-walkingLeft1.png'),
            "walking_left_2": pygame.image.load('Assets/Enemies/Alien/Alien-walkingLeft2.png'),
            "walking_right_1": pygame.image.load('Assets/Enemies/Alien/Alien-walkingRight1.png'),
            "walking_right_2": pygame.image.load('Assets/Enemies/Alien/Alien-walkingRight2.png')} 
        
        self.current_image = self.images["still_forward"]
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (x, y)
        self.size = size
        self.vel = vel
        self.shoot_cooldown = random.randint(1000, 5000)
        self.last_shot = random.randint(0, 500) + pygame.time.get_ticks()
        self.bullet_size = 10
        self.bullet_vel = 0.5
        self.bullet_img = None
        self.spawn_time = pygame.time.get_ticks()
        self.acc = 0.03

    def update(self, player_rect, bullets):
        if self.spawn_time + 4000 <= pygame.time.get_ticks():
            self.vel += self.acc
            self.acc *= 0.98
        if self.rect.x < player_rect.centerx:
            self.rect.x += self.vel
            self.current_image = self.images["walking_right_1"]
        elif self.rect.x > player_rect.centerx:
            self.rect.x -= self.vel
            self.current_image = self.images["walking_left_1"]

        if self.rect.y < player_rect.centery:
            self.rect.y += self.vel
            self.current_image = self.images["walking_forward_1"]
        elif self.rect.y > player_rect.centery:
            self.rect.y -= self.vel
            self.current_image = self.images["walking_up_1"]

        if self.last_shot + self.shoot_cooldown <= pygame.time.get_ticks():
            self.last_shot = random.randint(0, 500) + pygame.time.get_ticks()
            shoot(self, player_rect.centerx + 5 - random.randint(0, 10), player_rect.centery + 5 - random.randint(0, 10), False, self.bullet_size, self.bullet_vel, self.bullet_img, bullets)