import pygame
import sys
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, vel):
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

        # Boundary checks
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
            "walking_right_2": pygame.image.load('Assets/Enemies/Alien-walkingRight2.png')
        }
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

# Constants
WIDTH, HEIGHT = 800, 800
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 10
FPS = 60
GREEN = (0, 255, 0)

BACKGROUND = pygame.image.load('Assets/backgrounds/Background 1.png')

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Space")
CLOCK = pygame.time.Clock()

player = Player(3)
bullets = []
enemies = pygame.sprite.Group()
enemies = []
wave_length = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse_x - player.rect.centerx, mouse_y - player.rect.centery).normalize()
            bullet_velocity = direction * 2  
            bullet_vel_x, bullet_vel_y = bullet_velocity.x, bullet_velocity.y
            bullets.append({
                "rect": pygame.Rect(player.rect.centerx - BULLET_SIZE // 2, player.rect.centery - BULLET_SIZE // 2, BULLET_SIZE, BULLET_SIZE),
                "vel_x": bullet_vel_x,
                "vel_y": bullet_vel_y})

    keys = pygame.key.get_pressed()
    player.update(keys)

    SCREEN.blit(BACKGROUND, (0, 0))

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
                break 

        if bullet_marked_for_removal:
            break 

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    for bullet in bullets:
        pygame.draw.circle(SCREEN, GREEN, (int(bullet["rect"].x), int(bullet["rect"].y)), BULLET_SIZE // 2)

    SCREEN.blit(player.current_image, player.rect)

    if not enemies:
        wave_length += 2

    pygame.display.flip()
    CLOCK.tick(FPS)
