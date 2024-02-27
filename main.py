import pygame, sys
import asyncio
import random

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Space")

#images!!! 

#backgrounds:
MENU = pygame.image.load('Assets/backgrounds/bg.png')
BACKGROUND1 = pygame.image.load('Assets/backgrounds/Background 1.png')
BACKGROUND2 = pygame.image.load('Assets/backgrounds/Background 2.png')
BACKGROUND3 = pygame.image.load('Assets/backgrounds/Background 3.png')

#Enemy Alien - Forgot to edit to transparent when editing the sprite frames, so I did it in python, which is why this part looks messy lol:
ALIEN_STILL_FORWARD = pygame.image.load('Assets/Enemies/Alien-stillForward.png')
ALIEN_STILL_FORWARD = ALIEN_STILL_FORWARD.convert_alpha()
ALIEN_STILL_FORWARD.set_colorkey((0, 0, 0))

ALIEN_STILL_UP = pygame.image.load('Assets/Enemies/Alien-stillUp.png')
ALIEN_STILL_UP = ALIEN_STILL_UP.convert_alpha()
ALIEN_STILL_UP.set_colorkey((0, 0, 0))

ALIEN_STILL_LEFT = pygame.image.load('Assets/Enemies/Alien-stillLeft.png')
ALIEN_STILL_LEFT = ALIEN_STILL_LEFT.convert_alpha()
ALIEN_STILL_LEFT.set_colorkey((0, 0, 0))

ALIEN_STILL_RIGHT = pygame.image.load('Assets/Enemies/Alien-stillRight.png')
ALIEN_STILL_RIGHT = ALIEN_STILL_RIGHT.convert_alpha()
ALIEN_STILL_RIGHT.set_colorkey((0, 0, 0))

ALIEN_WALKING_FORWARD_1 = pygame.image.load('Assets/Enemies/Alien-walkingForward1.png')
ALIEN_WALKING_FORWARD_1 = ALIEN_WALKING_FORWARD_1.convert_alpha()
ALIEN_WALKING_FORWARD_1.set_colorkey((0, 0, 0))

ALIEN_WALKING_FORWARD_2 = pygame.image.load('Assets/Enemies/Alien-walkingForward2.png')
ALIEN_WALKING_FORWARD_2 = ALIEN_WALKING_FORWARD_2.convert_alpha()
ALIEN_WALKING_FORWARD_2.set_colorkey((0, 0, 0))

ALIEN_WALKING_UP_1 = pygame.image.load('Assets/Enemies/Alien-walkingUp1.png')
ALIEN_WALKING_UP_1 = ALIEN_WALKING_UP_1.convert_alpha()
ALIEN_WALKING_UP_1.set_colorkey((0, 0, 0))

ALIEN_WALKING_UP_2 = pygame.image.load('Assets/Enemies/Alien-walkingUp2.png')
ALIEN_WALKING_UP_2 = ALIEN_WALKING_UP_2.convert_alpha()
ALIEN_WALKING_UP_2.set_colorkey((0, 0, 0))

ALIEN_WALKING_LEFT_1 = pygame.image.load('Assets/Enemies/Alien-walkingLeft1.png')
ALIEN_WALKING_LEFT_1 = ALIEN_WALKING_LEFT_1.convert_alpha()
ALIEN_WALKING_LEFT_1.set_colorkey((0, 0, 0))

ALIEN_WALKING_LEFT_2 = pygame.image.load('Assets/Enemies/Alien-walkingLeft2.png')
ALIEN_WALKING_LEFT_2 = ALIEN_WALKING_LEFT_2.convert_alpha()
ALIEN_WALKING_LEFT_2.set_colorkey((0, 0, 0))

ALIEN_WALKING_RIGHT_1 = pygame.image.load('Assets/Enemies/Alien-walkingRight1.png')
ALIEN_WALKING_RIGHT_1 = ALIEN_WALKING_RIGHT_1.convert_alpha()
ALIEN_WALKING_RIGHT_1.set_colorkey((0, 0, 0))

ALIEN_WALKING_RIGHT_2 = pygame.image.load('Assets/Enemies/Alien-walkingRight2.png')
ALIEN_WALKING_RIGHT_2 = ALIEN_WALKING_RIGHT_2.convert_alpha()
ALIEN_WALKING_RIGHT_2.set_colorkey((0, 0, 0))

# Player - This time I made the background transparent lol.... I HATE MY LIFE.
PLAYER_STILL_FORWARD = pygame.image.load('Assets/Astronaut/Player_stillForward.png')
PLAYER_STILL_LEFT = pygame.image.load('Assets/Astronaut/Player_stillLeft.png')
PLAYER_STILL_RIGHT = pygame.image.load('Assets/Astronaut/Player_stillRight.png')
PLAYER_STILL_UP = pygame.image.load('Assets/Astronaut/Player_stillUp.png')

PLAYER_WALKING_FORWARD_1 = pygame.image.load('Assets/Astronaut/Player_walkingForward_1.png')
PLAYER_WALKING_FORWARD_2 = pygame.image.load('Assets/Astronaut/Player_walkingForward_2.png')

PLAYER_WALKING_UP_1 = pygame.image.load('Assets/Astronaut/Player_walkingUp_1.png')
PLAYER_WALKING_UP_2 = pygame.image.load('Assets/Astronaut/Player_walkingUp_2.png')

PLAYER_WALKING_LEFT_1 = pygame.image.load('Assets/Astronaut/Player_walkingLeft_1.png')
PLAYER_WALKING_LEFT_2 = pygame.image.load('Assets/Astronaut/Player_walkingLeft_2.png')

PLAYER_WALKING_RIGHT_1 = pygame.image.load('Assets/Astronaut/Player_walkingRight_1.png')
PLAYER_WALKING_RIGHT_2 = pygame.image.load('Assets/Astronaut/Player_walkingRight_2.png')

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3
        self.images_forward = [ALIEN_WALKING_FORWARD_1, ALIEN_STILL_FORWARD, ALIEN_WALKING_FORWARD_2]
        self.images_up = [ALIEN_WALKING_UP_1, ALIEN_STILL_UP, ALIEN_WALKING_UP_2]
        self.images_left = [ALIEN_WALKING_LEFT_1, ALIEN_STILL_LEFT, ALIEN_WALKING_LEFT_2]
        self.images_right = [ALIEN_WALKING_RIGHT_1, ALIEN_STILL_RIGHT, ALIEN_WALKING_RIGHT_2]
        self.current_images = self.images_forward
        self.walk_count = 0
        self.direction_timer = random.randint(30, 90)
    
    def move(self):
        if self.direction_timer == 0:
            direction = random.randint(0, 3)

            if direction == 0:
                self.current_images = self.images_forward
            elif direction == 1:
                self.current_images = self.images_up
            elif direction == 2:
                self.current_images = self.images_left
            elif direction == 3:
                self.current_images = self.images_right
            
            self.direction_timer = random.randint(30, 90)

        else:
            new_x = self.x
            new_y = self.y

            if self.current_images is self.images_forward:
                new_y += self.vel
            
            elif self.current_images is self.images_up:
                new_y -= self.vel
            
            elif self.current_images is self.images_left:
                new_x -= self.vel
            
            elif self.current_images is self.images_right:
                new_x += self.vel
            
            if 0 <= new_x <= WIDTH - self.current_images[0].get_width() and 0 <= new_y <= HEIGHT - self.current_images[0].get_height():
                self.x = new_x
                self.y = new_y
            else:
                if self.current_images is self.images_forward:
                    self.current_images = self.images_up
                elif self.current_images is self.images_up:
                    self.current_images = self.images_forward
                elif self.current_images is self.images_left:
                    self.current_images = self.images_right
                elif self.current_images is self.images_right:
                    self.current_images = self.images_left
            
            self.direction_timer -= 1
            
        self.walk_count = (self.walk_count + 1) % (len(self.current_images) * 3)

    def draw(self):
        index = self.walk_count // 3
        WIN.blit(self.current_images[index], (self.x, self.y))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3
        self.images_forward = [PLAYER_WALKING_FORWARD_1, PLAYER_STILL_FORWARD, PLAYER_WALKING_FORWARD_2]
        self.images_up = [PLAYER_WALKING_UP_1, PLAYER_STILL_UP, PLAYER_WALKING_UP_2]
        self.images_left = [PLAYER_WALKING_LEFT_1, PLAYER_STILL_LEFT, PLAYER_WALKING_LEFT_2]
        self.images_right = [PLAYER_WALKING_RIGHT_1, PLAYER_STILL_RIGHT, PLAYER_WALKING_RIGHT_2]
        self.current_images = self.images_forward
        self.walk_count = 0
    
    def move(self, keys):
        x_movement = 0
        y_movement = 0

        if keys[pygame.K_a] and self.x > self.vel:
            x_movement -= self.vel
            self.current_images = self.images_left
        elif keys[pygame.K_d] and self.x < WIDTH - self.vel - self.current_images[0].get_width():
            x_movement += self.vel
            self.current_images = self.images_right

        if keys[pygame.K_w] and self.y > self.vel:
            y_movement -= self.vel
            self.current_images = self.images_up
        elif keys[pygame.K_s] and self.y < HEIGHT - self.vel - self.current_images[0].get_height():
            y_movement += self.vel
            self.current_images = self.images_forward
        
        else:
            if self.current_images == self.images_left:
                self.current_images = [PLAYER_STILL_LEFT]
            elif self.current_images == self.images_right:
                self.current_images = [PLAYER_STILL_RIGHT]
            elif self.current_images == self.images_up:
                self.current_images = [PLAYER_STILL_UP]
            elif self.current_images == self.images_forward:
                self.current_images = [PLAYER_STILL_FORWARD]

        self.x += x_movement
        self.y += y_movement
    
        self.walk_count = (self.walk_count + 1) % (len(self.current_images) * 3)
    
    def draw(self, win):
        index = self.walk_count // 3
        win.blit(self.current_images[index], (self.x, self.y))

#Game loop:
pygame.font.init()

async def main():
    run = True
    FPS = 60
    LEVEL, LIVES = 0, 5
    MAIN_FONT = pygame.font.Font('Fonts/SPACE.ttf', 30)
    ENEMIES = []
    WAVE_LEN = 8
    LOST = False
    PLAYER = Player(WIDTH // 2, HEIGHT // 2)
    CLOCK = pygame.time.Clock()

    while not run:
        CLOCK.tick(FPS)
        menu_scaled = pygame.transform.scale(MENU, (WIDTH, HEIGHT))
        WIN.blit(menu_scaled, (0, 0))


        #Click to start message:
        start_message = MAIN_FONT.render('Click to Start!', True, (255, 255, 255))
        WIN.blit(start_message, (WIDTH // 2 - start_message.get_width() // 2, HEIGHT // 2 - start_message.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        await asyncio.sleep(0)
    
    for _ in range(WAVE_LEN):
        alien = Alien(random.randint(0, WIDTH - ALIEN_STILL_FORWARD.get_width()), random.randint(0, HEIGHT - ALIEN_STILL_FORWARD.get_height()))
        ENEMIES.append(alien)

    while run:
        CLOCK.tick(FPS)
        WIN.blit(BACKGROUND1, (0, 0))

        keys = pygame.key.get_pressed()
        PLAYER.move(keys)
        PLAYER.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
        
        for enemy in ENEMIES:
            enemy.move()
            enemy.draw()

        pygame.display.update()
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())