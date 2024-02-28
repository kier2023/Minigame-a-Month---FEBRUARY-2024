import pygame
import sys
import random

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

AMO_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/ammo crate.png'), (30, 30))
HEALTH_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/health.png'), (30, 30))
XP_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/xp.png'), (30, 30))

DROP_DURATION = 2000  
FLASH_THRESHOLD = 1500 
FLASH_INTERVAL = 200  

XP_TO_PAUSE = 100

BACKGROUND = pygame.image.load('Assets/backgrounds/Background 1.png')

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

    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.vel
            self.current_image = self.images["walking_up_1"]
        elif keys[pygame.K_s]:
            self.rect.y += self.vel
            self.current_image = self.images["walking_forward_1"]
        elif keys[pygame.K_a]:
            self.rect.x -= self.vel
            self.current_image = self.images["walking_left_1"]
        elif keys[pygame.K_d]:
            self.rect.x += self.vel
            self.current_image = self.images["walking_right_1"]
        else:
            self.current_image = self.images["still_forward"]

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

    def update(self, player_rect):
        if self.rect.x < player_rect.centerx:
            self.rect.x += self.vel
            self.current_image = self.images["walking_right_1"]
        elif self.rect.x > player_rect.centerx:
            self.rect.x -= self.vel
            self.current_image = self.images["walking_left_1"]

        if self.rect.y < player_rect.centery:
            self.rect.y += self.vel
            self.current_image = self.images["walking_down_1"]
        elif self.rect.y > player_rect.centery:
            self.rect.y -= self.vel
            self.current_image = self.images["walking_up_1"]

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Space")
CLOCK = pygame.time.Clock()

player = Player(3, 100, 50)
bullets = []
enemies = pygame.sprite.Group()
enemies = []
drops = []
wave_length = 5

def handle_drops(enemy_rect):
    drop_type = random.choice(["ammo", "health", "xp"])
    drop_rect = pygame.Rect(enemy_rect.centerx, enemy_rect.centery, 30, 30)

    if drop_type == "ammo":
        drop_img = AMO_IMG
    elif drop_type == "health":
        drop_img = HEALTH_IMG
    else:
        drop_img = XP_IMG

    drop_timer = DROP_DURATION 
    return {"type": drop_type, "rect": drop_rect, "img": drop_img, "timer": drop_timer}

def pause_options():
    option_font = pygame.font.Font('Fonts/SPACE.ttf', 30) # Might be to big???????????????????
    
    health_text = option_font.render("Press 1 for health", True, WHITE)
    SCREEN.blit(health_text, (WIDTH // 2 - health_text.get_width() // 2, HEIGHT // 2 - 50))

    ammo_text = option_font.render("Press 2 for Ammo", True, WHITE)
    SCREEN.blit(ammo_text, (WIDTH // 2 - ammo_text.get_width() // 2, HEIGHT // 2 + 50))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player.ammo > 0: 
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = pygame.Vector2(mouse_x - player.rect.centerx, mouse_y - player.rect.centery).normalize()
                bullet_velocity = direction * 2  
                bullet_vel_x, bullet_vel_y = bullet_velocity.x, bullet_velocity.y
                bullets.append({
                    "rect": pygame.Rect(player.rect.centerx - BULLET_SIZE // 2, player.rect.centery - BULLET_SIZE // 2, BULLET_SIZE, BULLET_SIZE),
                    "vel_x": bullet_vel_x,
                    "vel_y": bullet_vel_y})
                player.ammo -= 1 

    for drop in drops.copy():
        drop["timer"] -= CLOCK.get_rawtime()  

        if drop["timer"] < FLASH_THRESHOLD:

            if drop["timer"] % (2 * FLASH_INTERVAL) < FLASH_INTERVAL:
                SCREEN.blit(drop["img"], drop["rect"])

        if drop["timer"] <= 0:
            drops.remove(drop) 
        else:
            SCREEN.blit(drop["img"], drop["rect"]) 

    keys = pygame.key.get_pressed()
    player.update(keys)

    if player.xp >= XP_TO_PAUSE:
        pygame.time.delay(1000) # = 1 second I think?
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
            CLOCK.tick(FPS)

    SCREEN.blit(BACKGROUND, (0, 0))

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

    if not enemies:
        for _ in range(wave_length):
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

            enemies.append(new_enemy)

    for drop in drops.copy():
        if player.rect.colliderect(drop["rect"]):
            if drop["type"] == "ammo" and player.ammo < player.max_ammo:
                player.ammo += 1
                drops.remove(drop)  
            elif drop["type"] == "health" and player.health < player.max_health:
                player.health += 10  
                drops.remove(drop) 
            elif drop["type"] == "xp":
                player.xp += 10  
                drops.remove(drop)  

    for enemy in enemies:
        if enemy.rect.x < player.rect.centerx:
            enemy.rect.x += 1
        elif enemy.rect.x > player.rect.centerx:
            enemy.rect.x -= 1

        if enemy.rect.y < player.rect.centery:
            enemy.rect.y += 1
        elif enemy.rect.y > player.rect.centery:
            enemy.rect.y -= 1

        SCREEN.blit(enemy.current_image, enemy.rect)
    
    bullets_to_remove = []

    for bullet in bullets:
        bullet["rect"].x += bullet["rect"].width * bullet["vel_x"]
        bullet["rect"].y += bullet["rect"].height * bullet["vel_y"]

        bullet_marked_for_removal = False
        for enemy in enemies.copy():
            if bullet["rect"].colliderect(enemy):
                bullets_to_remove.append(bullet)
                bullet_marked_for_removal = True
                enemies.remove(enemy)
                drop = handle_drops(enemy.rect)
                drops.append(drop)
                break 

        if bullet_marked_for_removal:
            break 

    for drop in drops:
        SCREEN.blit(drop["img"], drop["rect"])

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    for bullet in bullets:
        pygame.draw.circle(SCREEN, GREEN, (int(bullet["rect"].x), int(bullet["rect"].y)), BULLET_SIZE // 2)

    SCREEN.blit(player.current_image, player.rect)

    if not enemies:
        wave_length += 2

    pygame.display.flip()
    CLOCK.tick(FPS)
