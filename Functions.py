import pygame
import random
from Constants import *

def handle_drops(enemy_rect):
    drop_type = random.choice(["ammo", "health", "speed"])
    drop_rect = pygame.Rect(enemy_rect.centerx, enemy_rect.centery, 30, 30)

    if drop_type == "ammo":
        drop_img = AMO_IMG
    elif drop_type == "speed":
        drop_img = SPEED_IMG
    else:
        drop_img = HEALTH_IMG

    drop_timer = DROP_DURATION 
    return {"type": drop_type, "rect": drop_rect, "img": drop_img, "timer": drop_timer}

def pause_options():    
    SCREEN.blit(OPTIONS, (0, 0)) # IMAGINE THIS BEING IN ITS OWN FUNCTION (LOL!!!!!!)

def shoot(me, x, y, is_player, size, vel, img, bullets):
    direction = pygame.Vector2(x - me.rect.centerx, y - me.rect.centery).normalize()
    bullet_velocity = direction * vel  
    bullet_vel_x, bullet_vel_y = bullet_velocity.x, bullet_velocity.y
    bullets.append({
        "rect": pygame.Rect(me.rect.centerx - size // 2, me.rect.centery - size // 2, size, size),
        "vel_x": bullet_vel_x,
        "vel_y": bullet_vel_y,
        "player": is_player,
        "img": RED_BULLET_IMG if is_player else GREEN_BULLET_IMG})

    BULLET_SOUND.play()
