import pygame
import sys
import random
import asyncio
from Constants import *
from Functions import *
from Enemy import *
from Player import *
from Slime import *

'''
 Function to deplay the start screen before the main game loop begins. 
 Game loop starts when the user clicks anywhere on the screen.
 Player can also quit/exit the game by clicking the close applicatioin button.
'''
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
slimes = pygame.sprite.Group()
drops = []
wave_length = 5
last_wave = -10000
speed_boost_start = 0
player_score = 0
spawn_count = wave_length

# Main game loop is an ansycrhronus functions as I used pygbag to generate a web.zip file. 

async def main_loop():
    global wave_length, speed_boost_start, player_score, spawn_count, bullets

    username = get_username()
    print({username})
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

                    '''
                    Calls the shoot function to create a bullet. 
                    Doing so decrements the players overall ammo by 1.
                    Shoot direction is defined by where the mouse was clicked on the screen.
                    '''
                    shoot(player, mouse_x, mouse_y, True, BULLET_SIZE, 2, None, bullets)
                    player.ammo -= 1

        keys = pygame.key.get_pressed()
        player.update(keys)

        '''
        Updates timers for enemy drops and applies a flash effect for the drops before the timer expiers.
        The flash effect is not working, and is not important enough to fix right now. 
        '''
        for drop in drops:
            drop["timer"] -= CLOCK.get_rawtime()  

            if drop["timer"] < FLASH_THRESHOLD:

                if drop["timer"] % (2 * FLASH_INTERVAL) < FLASH_INTERVAL:
                    SCREEN.blit(drop["img"], drop["rect"])

            if drop["timer"] <= 0:
                drops.remove(drop) 
            else:
                SCREEN.blit(drop["img"], drop["rect"]) 

        '''
        Only in-game pause feature. 
        Players can only access the pause screen if they have enough XP (100xp),
        I am going to create a key press to bring up the pause menu.
        For now, the pause menu acts like a level up menu, displaying bonus options for the player to select.
        Each bonus option resets the values back to max. 
        '''
        if player.xp >= XP_TO_PAUSE:
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()                  
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if AMMO_PACK_RECT.collidepoint(event.pos):
                            player.ammo = player.max_ammo
                            player.xp = 0
                            paused = False
                        elif HEALTH_PACK_RECT.collidepoint(event.pos):
                            player.health = player.max_health
                            player.xp = 0
                            paused = False
                
                pause_options()
                pygame.display.flip()
                await asyncio.sleep(0)
                CLOCK.tick(FPS)
        
        '''
        Game over screen is triggered when the players health is less than or equal to 0. 
        The game can be restarted by pressing the R key, or players can quit the game. 
        On restart, health, ammo, xp, enemies, bullets and drops are all reset/cleared. 
        '''
        if player.health <= 0:
            paused = True
            while paused:
                SCREEN.blit(RESTART, (0, 0))
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
                            paused = False 
                            break
    
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

                if random.choice([True, False]):
                    new_enemy = Enemy(enemy_x, enemy_y, ENEMY_SIZE, 1) 
                else:
                    new_enemy = Slime(enemy_x, enemy_y, ENEMY_SIZE, 1, drops) 

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
                
                if isinstance(new_enemy, Enemy):
                    enemies.add(new_enemy)
                elif isinstance(new_enemy, Slime):
                    slimes.add(new_enemy)

        '''
        Checks for player v enemy collision. 
        Upon collision, players health is reduced by 20, 
        Enemy then drops a bonus, and is killed from the screen.
        '''
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player.health -= 20
                player.xp += 10
                drop = handle_drops(enemy.rect)
                drops.append(drop)
                enemy.kill()

        for slime in slimes:
            if player.rect.colliderect(slime.rect):
                player.health -= 0.5

        '''
        Checks for collisions between player and drops, and applies the corrosponding perks.
        Currently in the process of adding more of these to my v1.1.0 branch.
        Drop type ammo increases the players ammo on drop pickup by 5
        Drop type health increases the players health on drop pickup by 10
        Drop type speed increases the players velocity on drop pick up by 2. This drop type has a duration effect of 5 seconds.
        '''
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
        
        for slime in slimes:
            slime.update(player.rect)
            SCREEN.blit(slime.current_image, slime.rect)

        if speed_boost_start > 0 and pygame.time.get_ticks() - speed_boost_start >= 5000:
            player.vel = player.original_vel
            speed_boost_start = 0

        bullets_to_remove = []
        enemies_to_remove = []

        '''
        Update bullet positions anc checks for collisions with enemies or players.
        If a players bullet hits an enemy, the player gaines 5 xp points, and a score of 5. 
        Players score is incremented by 5 when an enemy is killed. 
        If an enemy bullet collides with the player, the players health is reduced by 10.
        Enemies and bullets are also removed when a) they collide, or b) they go off screen.
        '''
        for bullet in bullets:
            bullet["rect"].x += bullet["rect"].width * bullet["vel_x"]
            bullet["rect"].y += bullet["rect"].height * bullet["vel_y"]

            bullet_marked_for_removal = False
            for slime in slimes:
                if bullet["rect"].colliderect(slime.rect) and bullet["player"]:
                    bullets_to_remove.append(bullet)
                    bullet_marked_for_removal = True
                    slime.take_damage()
                    player.xp += 5
                    player_score += 5
                    break

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

        bullets = [bullet for bullet in bullets if bullet not in bullets_to_remove]

        for bullet in bullets:
            SCREEN.blit(bullet["img"], (int(bullet["rect"].x), int(bullet["rect"].y)))

        SCREEN.blit(BACKGROUND2, (0, 0))

        '''
        Health, XP and Ammo bars are positioned at the top center of the screen.
        These health bars decrease/increase depending on drop pick ups, enemy kills, or player collision with bullets and enemies. 
        '''
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