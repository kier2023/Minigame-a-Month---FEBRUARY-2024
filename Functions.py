import pygame
import random
import sys
import asyncio
from Constants import *

async def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        
        SCREEN.blit(BACKGROUND3, (0, 0))
        pygame.display.flip()
        await asyncio.sleep(0)
        CLOCK.tick(FPS)

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
    #SCREEN.blit(OPTIONS, (0, 0)) # IMAGINE THIS BEING IN ITS OWN FUNCTION (LOL!!!!!!)
    SCREEN.blit(AMMO_PACK, AMMO_PACK_RECT.topleft)
    SCREEN.blit(HEALTH_PACK, HEALTH_PACK_RECT.topleft)

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

def get_username():
    username = ""
    font = pygame.font.Font('Fonts/PixelifySans-VariableFont_wght.ttf', 50)
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    start_screen()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:
                        username += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if SIGN_IN_BTN_RECT.collidepoint(event.pos):
                    input_active = False
                    start_screen()                

        SCREEN.blit(USERNAME_SCREEN, (0, 0))

        # Display entered username underneath
        username_surface = font.render(username, True, BLACK)
        username_rect = username_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(username_surface, username_rect)
        SCREEN.blit(SIGN_IN_BTN, SIGN_IN_BTN_RECT.topleft)

        pygame.display.flip()
        CLOCK.tick(FPS)

    return username