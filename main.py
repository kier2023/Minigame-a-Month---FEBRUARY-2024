import pygame
import sys
import random
import asyncio
import math
from Constants import *
from Functions import *
from Enemy import *
from Player import *

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

player = Player(5, 100, 50)
bullets = []
enemies = pygame.sprite.Group()
drops = []
wave_length = 5
last_wave = -10000
speed_boost_start = 0
player_score = 0
spawn_count = wave_length

# Game loop
async def main_loop():
    global wave_length, speed_boost_start, player_score, spawn_count

    await start_screen()

    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.05)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player.ammo > 0:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    shoot(player, mouse_x, mouse_y, True, BULLET_SIZE, 2, None, bullets)
                    player.ammo -= 1

        keys = pygame.key.get_pressed()
        player.update(keys)

        for drop in drops:
            drop["timer"] -= CLOCK.get_rawtime()  

            if drop["timer"] < FLASH_THRESHOLD:

                if drop["timer"] % (2 * FLASH_INTERVAL) < FLASH_INTERVAL: # Doesn't work so don't know why this is here....
                    SCREEN.blit(drop["img"], drop["rect"])

            if drop["timer"] <= 0:
                drops.remove(drop) 
            else:
                SCREEN.blit(drop["img"], drop["rect"]) 

        if player.xp >= XP_TO_PAUSE:
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            player.health = player.max_health
                            player.xp = 0
                            paused = False
                        elif event.key == pygame.K_2:
                            player.ammo = player.max_ammo
                            player.xp = 0
                            paused = False
                
                pause_options()
                pygame.display.flip()
                await asyncio.sleep(0)
                CLOCK.tick(FPS)
        
        if player.health <= 0:
            paused = True
            while paused:
                SCREEN.blit(RESTART, (0, 0))
                # I know how to pause the shooting... But I kinda don't.... So lets just leave this comment here so people know im A little bit of an idiot.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            player.health = player.max_health
                            player.ammo = player.max_ammo
                            player.xp = 0
                            spawn_count = wave_length = 5
                            enemies.empty()
                            bullets.clear()
                            drops.clear()
                            paused = False # Oh.... I see my issue, I think....? 
                            break # Maybe??
    
                pygame.display.flip()
                await asyncio.sleep(0)
                CLOCK.tick(FPS)
                continue 

        SCREEN.blit(BACKGROUND, (0, 0))

        if spawn_count > 1:
            while spawn_count > 1 and random.randint(0, 100) > 85:
                spawn_count -= 1
                side = random.choice(['left', 'right', 'top', 'bottom'])
                if side == 'left':
                    enemy_x = -ENEMY_SIZE
                    enemy_y = random.randint(0, HEIGHT - ENEMY_SIZE)
                elif side == 'right':
                    enemy_x = WIDTH
                    enemy_y = random.randint(0, HEIGHT - ENEMY_SIZE)
                elif side == 'top':
                    enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
                    enemy_y = -ENEMY_SIZE
                else:
                    enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
                    enemy_y = HEIGHT - ENEMY_SIZE

                new_enemy = Enemy(enemy_x, enemy_y, ENEMY_SIZE, 1) 

                while any(existing_enemy.rect.colliderect(new_enemy.rect) for existing_enemy in enemies):
                    if side == 'left':
                        new_enemy.rect.x = -ENEMY_SIZE
                        new_enemy.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
                    elif side == 'right':
                        new_enemy.rect.x = WIDTH
                        new_enemy.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
                    elif side == 'top':
                        new_enemy.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
                        new_enemy.rect.y = -ENEMY_SIZE
                    else:
                        new_enemy.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
                        new_enemy.rect.y = HEIGHT - ENEMY_SIZE
                
                enemies.add(new_enemy)

        for drop in drops:
            if player.rect.colliderect(drop["rect"]):
                if drop["type"] == "ammo" and player.ammo < player.max_ammo:
                    if player.ammo + 5 > player.max_ammo:
                        player.ammo = player.max_ammo 
                    else:
                        player.ammo += 5
                    drops.remove(drop)
                elif drop["type"] == "health" and player.health < player.max_health:
                    if player.health + 10 > player.max_health:
                        player.health = player.max_health
                    else:
                        player.health += 10  
                    drops.remove(drop) 
                elif drop["type"] == "speed":
                    player.vel = player.original_vel + 2
                    speed_boost_start = pygame.time.get_ticks()
                    drops.remove(drop)
                    
        for enemy in enemies:
            enemy.update(player.rect, bullets)
            SCREEN.blit(enemy.current_image, enemy.rect)

        if speed_boost_start > 0 and pygame.time.get_ticks() - speed_boost_start >= 5000:
            player.vel = player.original_vel
            speed_boost_start = 0

        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            bullet["rect"].x += bullet["rect"].width * bullet["vel_x"]
            bullet["rect"].y += bullet["rect"].height * bullet["vel_y"]

            bullet_marked_for_removal = False
            for enemy in enemies:
                if bullet["rect"].colliderect(enemy.rect) and bullet["player"]:
                    bullets_to_remove.append(bullet)
                    bullet_marked_for_removal = True
                    enemies_to_remove.append(enemy)
                    player.xp += 5
                    drop = handle_drops(enemy.rect)
                    drops.append(drop)
                    player_score += 5
                    break

            if bullet["rect"].colliderect(player.rect) and not bullet["player"]:
                bullets_to_remove.append(bullet)
                bullet_marked_for_removal = True
                player.health -= 10
                break

            if bullet_marked_for_removal:
                continue

        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        for drop in drops:
            SCREEN.blit(drop["img"], drop["rect"])

        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        for bullet in bullets:
            SCREEN.blit(bullet["img"], (int(bullet["rect"].x), int(bullet["rect"].y)))

        SCREEN.blit(BACKGROUND2, (0, 0))

        health_bar_width = int((player.health / player.max_health) * BAR_WIDTH)
        pygame.draw.rect(SCREEN, (150, 0, 0), (WIDTH // 2 - BAR_WIDTH // 2, 10, health_bar_width, BAR_HEIGHT))
        pygame.draw.rect(SCREEN, RED, (WIDTH // 2 - BAR_WIDTH // 2, 10, BAR_WIDTH, BAR_HEIGHT), 2)
        SCREEN.blit(HEALTH_IMG, (WIDTH // 2 + BAR_WIDTH // 2 + 10, 10))


        xp_bar_width = int((player.xp / 100) * BAR_WIDTH)  
        xp_bar_rect = pygame.Rect(WIDTH // 2 - BAR_WIDTH // 2, 40, xp_bar_width, BAR_HEIGHT)
        pygame.draw.rect(SCREEN, (0, 150, 0), xp_bar_rect)
        pygame.draw.rect(SCREEN, GREEN, (WIDTH // 2 - BAR_WIDTH // 2, 40, BAR_WIDTH, BAR_HEIGHT), 2)
        pygame.draw.line(SCREEN, GREEN, (xp_bar_rect.right, 40), (xp_bar_rect.right, 40 + BAR_HEIGHT), 2)
        SCREEN.blit(XP_IMG, (WIDTH // 2 + BAR_WIDTH // 2 + 10, 40))


        ammo_bar_width = int((player.ammo / player.max_ammo) * BAR_WIDTH)
        pygame.draw.rect(SCREEN, (0, 0, 150), (WIDTH // 2 - BAR_WIDTH // 2, 70, ammo_bar_width, BAR_HEIGHT))
        pygame.draw.rect(SCREEN, BLUE, (WIDTH // 2 - BAR_WIDTH // 2, 70, BAR_WIDTH, BAR_HEIGHT), 2)
        SCREEN.blit(AMO_IMG, (WIDTH // 2 + BAR_WIDTH // 2 + 10, 70))

        score_font = pygame.font.Font('Fonts/SPACE.ttf', 30)
        score_text = score_font.render(f'Score: {player_score}', True, WHITE)
        SCREEN.blit(score_text, (WIDTH - 250, HEIGHT - 50))
        SCREEN.blit(player.current_image, player.rect)

        if not enemies and spawn_count == 1:
            wave_length += 1
            spawn_count = wave_length

        pygame.display.flip()
        await asyncio.sleep(0)
        CLOCK.tick(FPS)

if __name__ == "__main__":
    asyncio.run(main_loop())