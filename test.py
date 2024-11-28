import pygame
import random
import sys
import os
# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# main stuff
PLAYER_SPEED = 5 
ENEMY_SPEED = 1 
BULLET_SPEED = 7 
ENEMY_DROP = 30
POWERUP_SPAWN_INTERVAL = 5000  # this is in milliseconds if you want to change it
MAX_BULLETS = 3
MAX_WINS = 3
WAVE_1_ENEMIES = 30
WAVE_2_ENEMIES = 40
FINAL_WAVE = 15
ENEMY_SLOWDOWN_DISTANCE = 25
CUTSCENE_ENEMIES = 7
SHIELD_HEALTH = 35
FINAL_BOSS_HEALTH = 5  # Variable to experiment with final boss health

script_dir = os.path.dirname(os.path.abspath(__file__))

# Build paths to images and sounds
images_dir = os.path.join(script_dir, 'Images')
sounds_dir = os.path.join(script_dir, 'Sounds')

# Load images and sounds using dynamic paths
player_img = pygame.image.load(os.path.join(images_dir, 'Invader1.png')).convert_alpha()
enemy_img = pygame.image.load(os.path.join(images_dir, 'EnemyShip.png')).convert_alpha()
bullet_img = pygame.image.load(os.path.join(images_dir, 'bullett.png')).convert_alpha()
powerup_img = pygame.image.load(os.path.join(images_dir, 'Powerup.png')).convert_alpha()
enemy_bullet = pygame.image.load(os.path.join(images_dir, 'EnemyBullet.png')).convert_alpha()
background_img = pygame.image.load(os.path.join(images_dir, 'StarBackground.png')).convert_alpha()
logo_img = pygame.image.load(os.path.join(images_dir, 'Logo1.png')).convert_alpha()
Finalboss_img = pygame.image.load(os.path.join(images_dir, 'FinalBoss.png')).convert_alpha()
 
hyperdrive_sound = pygame.mixer.Sound(os.path.join(sounds_dir, 'HyperDrive.mp3'))
background_music = pygame.mixer.Sound(os.path.join(sounds_dir, 'SpaceInvadersmusic.mp3'))
finalboss_music = pygame.mixer.Sound(os.path.join(sounds_dir, 'finalbossmusic.mp3'))
lose_sound = pygame.mixer.Sound(os.path.join(sounds_dir, 'You Lose Sound Effect.mp3'))
explosion_sound = pygame.mixer.Sound(os.path.join(sounds_dir, 'Explosion.mp3'))
# Create a sprite group for the game logo
logo = pygame.sprite.Group()

# Health bar function
def draw_health_bar(x, y, current_health, max_health, color=RED):
    bar_length = 150  # Length of the health bar
    bar_height = 15   # Height of the health bar
    fill = (current_health / max_health) * bar_length  # Calculate the fill percentage
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)  # Outline rectangle
    fill_rect = pygame.Rect(x, y, fill, bar_height)  # Filled rectangle
    pygame.draw.rect(screen, color, fill_rect)  # Draw the fill
    pygame.draw.rect(screen, WHITE, outline_rect, 2)  # Draw the outline

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.lives = 15
        self.score = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Prevent going out of bounds
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, SCREEN_HEIGHT)

# Final Boss class
class Finalboss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.health = 50

# Star class for background animation in the menu
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 1
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)

# Function to draw text
def draw_text(text, size, color, x, y, font_name=None, center=False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Main menu screen with animated stars
def main_menu():
    stars = pygame.sprite.Group()
    for _ in range(100):
        star = Star(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        stars.add(star)
    # Load and scale the game logo image
    logo_image = pygame.transform.scale(logo_img, (400, 200))
    logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50))
    
    menu = True
    while menu:
        screen.fill(BLACK)
        stars.update()
        stars.draw(screen)
        screen.blit(logo_image, logo_rect)
        draw_text("Press ENTER to Start", 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, center=True)
        draw_text("Press C for Controls", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    start_game()
                if event.key == pygame.K_c:
                    show_controls()

# Show controls screen
def show_controls():
    controls = True
    while controls:
        screen.fill(BLACK)
        draw_text("Move: Arrow Keys or WASD", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        draw_text("Shoot: Space", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
        draw_text("Press ESC to go back", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2, center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    controls = False
                    main_menu()

# Main game function
def start_game():
    player = Player()
    finalBoss = Finalboss()

    all_sprites = pygame.sprite.Group(player)
    final_boss_group = pygame.sprite.Group(finalBoss)

    clock = pygame.time.Clock()

    running = True
    wave_num = 1
    final = False  # Final boss flag
    while running:
        clock.tick(60)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player
        player.update(keys)

        # Update other sprites (if any)
        all_sprites.update(keys)  # Other sprites will still be updated here

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw the player's health bar
        draw_health_bar(10, SCREEN_HEIGHT - 30, player.lives, 15, GREEN)

        # Draw the boss's health bar (only during the boss fight)
        if final:
            draw_health_bar(SCREEN_WIDTH // 2 - 75, 10, finalBoss.health, 50, RED)

        # Check if the final boss should appear
        if not final and player.lives > 0 and wave_num == 3:
            final = True
            draw_text("Final Boss Appears!", 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.flip()
            pygame.time.wait(2000)

        # Update the display
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main_menu()
