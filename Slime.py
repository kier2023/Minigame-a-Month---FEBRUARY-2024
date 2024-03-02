import pygame
from Functions import *

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, size, vel, drops, initial_health=3):
        super().__init__()
        self.images = {
            "slime_still": pygame.image.load('Assets/Enemies/slime/slime-idle-1.png'),
            "slime_move_right_1": pygame.image.load('Assets/Enemies/slime/slime-move_right_1.png'),
            "slime_move_right_2": pygame.image.load('Assets/Enemies/slime/slime-move_right_2.png'),
            "slime_move_left_1": pygame.image.load('Assets/Enemies/slime/slime-move-left_1.png'),
            "slime_move_left_2": pygame.image.load('Assets/Enemies/slime/slime-move_left_2.png')}
        self.current_image = self.images["slime_still"] 
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (x, y)
        self.size = size
        self.vel = 2 
        self.spawn_time = pygame.time.get_ticks()
        self.acc = 0.03
        self.health = initial_health
        self.drops = drops

    def update(self, player_rect):
        if self.spawn_time + 4000 <= pygame.time.get_ticks():
            self.vel += self.acc
            self.acc *= 0.98
        if self.rect.x < player_rect.centerx:
            self.rect.x += self.vel
            self.current_image = self.images["slime_move_right_1"]
        elif self.rect.x > player_rect.centerx:
            self.rect.x -= self.vel
            self.current_image = self.images["slime_move_left_1"]

        if self.rect.y < player_rect.centery:
            self.rect.y += self.vel
            self.current_image = self.images["slime_still"]
        elif self.rect.y > player_rect.centery:
            self.rect.y -= self.vel
            self.current_image = self.images["slime_still"]
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            drop = handle_drops(self.rect)
            self.drops.append(drop)