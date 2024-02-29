import pygame
import sys
import random
import asyncio
import math

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
        
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.health -= 20
                drop = handle_drops(enemy.rect)
                drops.append(drop)
                enemy.kill()

        self.rect.x = max(0, min(self.rect.x, WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PLAYER_SIZE))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size, vel):
        super().__init__()
        self.images = {
            "still_forward": pygame.image.load('Assets/Enemies/Alien-stillForward.png'),
            "still_left": pygame.image.load('Assets/Enemies/Alien-stillLeft.png'),
            "still_right": pygame.image.load('Assets/Enemies/Alien-stillRight.png'),
            "still_up": pygame.image.load('Assets/Enemies/Alien-stillUp.png'),
            "walking_forward_1": pygame.image.load('Assets/Enemies/Alien-walkingForward1.png'),
            "walking_forward_2": pygame.image.load('Assets/Enemies/Alien-walkingForward2.png'),
            "walking_up_1": pygame.image.load('Assets/Enemies/Alien-walkingUp1.png'),
            "walking_up_2": pygame.image.load('Assets/Enemies/Alien-walkingUp2.png'),
            "walking_left_1": pygame.image.load('Assets/Enemies/Alien-walkingLeft1.png'),
            "walking_left_2": pygame.image.load('Assets/Enemies/Alien-walkingLeft2.png'),
            "walking_right_1": pygame.image.load('Assets/Enemies/Alien-walkingRight1.png'),
            "walking_right_2": pygame.image.load('Assets/Enemies/Alien-walkingRight2.png')} 
        
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

    def update(self, player_rect):
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
            shoot(self, player_rect.centerx + 5 - random.randint(0, 10), player_rect.centery + 5 - random.randint(0, 10), False, self.bullet_size, self.bullet_vel, self.bullet_img)

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

def shoot(me, x, y, is_player, size, vel, img):
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

# Constants
WIDTH, HEIGHT = 800, 800
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 10
FPS = 60
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BAR_WIDTH = 550
BAR_HEIGHT = 25
WAVE_DELAY = 5000
CURVED_BOX_COLOR = (59, 24, 29)
CURVED_BOX_RADIUS = 20
CURVED_BOX_PADDING = 20

pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

RESTART_FONT = pygame.font.Font('Fonts/SpaceMono-Regular.ttf', 40)
RESTART_TEXT = RESTART_FONT.render("GAME OVER! Press R to restart", True, WHITE)

AMO_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/Ammo crate.png'), (40, 40))
HEALTH_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/health.png'), (30, 30))
XP_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/xp.png'), (30, 30))
SPEED_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/speed.png'), (30, 30))

DROP_DURATION = 5000  
FLASH_THRESHOLD = 1500 
FLASH_INTERVAL = 200  

XP_TO_PAUSE = 100

BACKGROUND = pygame.image.load('Assets/backgrounds/Background 1.png')
BACKGROUND2 = pygame.image.load('Assets/backgrounds/Background 2.png')
BACKGROUND3 = pygame.image.load('Assets/backgrounds/bg.png')
RESTART = pygame.image.load('Assets/backgrounds/restart.png')
OPTIONS = pygame.image.load('Assets/backgrounds/options.png')

RED_BULLET_IMG = pygame.transform.scale(pygame.image.load('Assets/lasers/1.png'), (30, 30))
GREEN_BULLET_IMG = pygame.transform.scale(pygame.image.load('Assets/lasers/2.png'), (30, 30))

BULLET_SOUND = pygame.mixer.Sound('Music/efx/space-laser-38082.wav')
BULLET_SOUND.set_volume(0.2)
pygame.mixer.music.load('Music/bg-music/arthur-vyncke-a-few-jumps-away.wav')

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Space")
CLOCK = pygame.time.Clock()

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
                    shoot(player, mouse_x, mouse_y, True, BULLET_SIZE, 2, None)
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
            enemy.update(player.rect)
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