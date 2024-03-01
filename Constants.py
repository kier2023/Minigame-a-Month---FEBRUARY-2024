
import pygame

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
BAR_WIDTH = 450
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

AMO_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/Ammo crate.png'), (30, 30))
HEALTH_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/health.png'), (30, 30))
XP_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/xp.png'), (30, 30))
SPEED_IMG = pygame.transform.scale(pygame.image.load('Assets/bonuses/speed.png'), (30, 30))

AMMO_PACK = pygame.transform.scale(pygame.image.load('Assets/bonuses/Ammo Pack.png'), (200, 200))
AMMO_PACK_RECT = AMMO_PACK.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 ))
HEALTH_PACK = pygame.transform.scale(pygame.image.load('Assets/bonuses/Health Pack.png'), (200, 200))
HEALTH_PACK_RECT = HEALTH_PACK.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2))

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