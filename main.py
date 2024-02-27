import pygame
import sys
import random
import asyncio

WIDTH, HEIGHT = 800, 800
FPS = 60
PLAYER_VEL = 5
COOLDOWN = 30

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Space")

BACKGROUND = pygame.image.load('Images/background.png')
PLAYER_IMAGE = pygame.image.load('Images/pixel_ship_yellow.png')
ASTEROID_IMAGES = [pygame.image.load(f'Images/asteroid {i}.png') for i in range(1, 4)]
OXYGEN_IMAGES = [pygame.image.load(f'Images/o2 {i}.png') for i in range(1, 4)]

class Player:
    def __init__(self, x, y, o2=100):
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect(topleft=(x, y))
        self.o2 = o2

    def move(self, keys):
        self.rect.x += (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_VEL
        self.rect.y += (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_VEL
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = random.randint(1, 7)

    def move(self):
        self.rect.y += self.vel

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class AsteroidManager:
    def __init__(self):
        self.asteroid_list = pygame.sprite.Group()
        self.spawn_cooldown = 0

    def spawn_asteroid(self):
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-50, -10)
        asteroid_image = random.choice(ASTEROID_IMAGES)
        asteroid = Asteroid(x, y, asteroid_image)
        self.asteroid_list.add(asteroid)

    def move_asteroids(self):
        for asteroid in self.asteroid_list:
            asteroid.move()

    def draw_asteroids(self, surface):
        self.asteroid_list.draw(surface)

    def update(self, player):
        self.spawn_cooldown -= 1
        if self.spawn_cooldown <= 0:
            self.spawn_asteroid()
            self.spawn_cooldown = COOLDOWN

        self.move_asteroids()
        self.draw_asteroids(WIN)

        if pygame.sprite.spritecollide(player, self.asteroid_list, False):
            return True 
        return False

async def main():
    RUN = True
    LEVEL, LIVES = 0, 3

    player = Player(350, 650)

    CLOCK = pygame.time.Clock()
    asteroid_manager = AsteroidManager()

    while RUN:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        keys = pygame.key.get_pressed()
        player.move(keys)

        WIN.fill((0, 0, 0))
        WIN.blit(BACKGROUND, (0, 0))
        player.draw(WIN)

        if asteroid_manager.update(player):
            print("Game Over - Player collided with an asteroid")
            RUN = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())