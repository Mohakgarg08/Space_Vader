import pygame
import random
import sys

pygame.init()

# This is the setting the screen height and width
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# settings
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

# This is the colors for the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#This is setting the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Vaders")


# saving the images and the audios in a variable.
player_img = pygame.image.load('Images/Invader1.png').convert_alpha()
enemy_img = pygame.image.load('Images/EnemyShip.png').convert_alpha()
bullet_img = pygame.image.load('Images/bullett.png').convert_alpha()
powerup_img = pygame.image.load('Images/Powerup.png').convert_alpha()
enemy_bullet = pygame.image.load('Images/EnemyBullet.png').convert_alpha()
background_img = pygame.image.load('Images/StarBackground.png').convert_alpha()
logo_img = pygame.image.load('Images/Logo1.png').convert_alpha()
Finalboss_img = pygame.image.load('Images/FinalBoss.png').convert_alpha()
hyperdrive_sound = pygame.mixer.Sound('Sounds/HyperDrive.mp3')
background_music = pygame.mixer.Sound('Sounds/SpaceInvadersmusic.mp3')
finalboss_music = pygame.mixer.Sound('Sounds/finalbossmusic.mp3')
lose_sound = pygame.mixer.Sound('Sounds/You Lose Sound Effect.mp3')
explosion_sound = pygame.mixer.Sound('Sounds/Explosion.mp3')  # Placeholder for explosion sound


def draw_text(text, size, color, x, y, font_name=None, center=False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def hyperdrive_effect():
    for _ in range(20):
        screen.fill(BLACK)
        for enemy in enemies:
            enemy.rect.y += 20
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.wait(50)
    for enemy in enemies:
        enemy.speed = ENEMY_SPEED

def tv_off_effect():
    for i in range(10, 0, -1):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT // 2 - i * 10, SCREEN_WIDTH, i * 20))
        pygame.display.flip()
        pygame.time.wait(100)
    screen.fill(BLACK)
    pygame.display.flip()
    pygame.time.wait(700)
    draw_text("GO!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    pygame.display.flip()
    pygame.time.wait(2100)
    screen.fill(BLACK)
    pygame.display.flip()

def cinematic_intro():
    draw_text("So it begins...", 44, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 , center=True)
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    pygame.display.flip()
    pygame.time.wait(1500)
    pygame.mixer.Sound.play(hyperdrive_sound)
    pygame.mixer.music.set_volume(0.01)
    pygame.time.wait(2000)
    screen.fill(BLACK)
    pygame.display.flip()

def boss_cinematic_entry():
    for i in range(10):
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 50))
        pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        draw_text("I have found you.", 44, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        pygame.display.flip()
        pygame.time.wait(300)
    pygame.time.wait(2000)
    draw_text("You now have shields when you get power-ups, press F to save yourself.", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
    pygame.display.flip()
    pygame.time.wait(3000)

# This is the player class where all the characteristics of the player are.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (80, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 15
        self.score = 0
        self.wins = 0
        self.powered_up = False
        self.powerup_time = 0
        self.shielded = False
        self.shield_health = SHIELD_HEALTH
        self.hasshield=False

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 300:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 595:
            self.rect.y += self.speed
        if self.powered_up and pygame.time.get_ticks() > self.powerup_time:
            self.powered_up = False
        if keys[pygame.K_f] and self.hasshield and final:
            self.activate_shield()
            self.hasshield=False


    def shoot(self):
        if self.powered_up:
            for offset in [-15, 0, 15]:
                bullet = Bullet(self.rect.centerx + offset, self.rect.top, bullet_img, -BULLET_SPEED)
                all_sprites.add(bullet)
                bullets.add(bullet)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top, bullet_img, -BULLET_SPEED)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def activate_shield(self):
        self.shielded = True
        self.shield_health=SHIELD_HEALTH


    def deactivate_shield(self):
        self.shielded = False

    def draw_shield(self):
        if self.shielded:
            pygame.draw.ellipse(screen, BLUE, self.rect.inflate(30, 30), 2)
            draw_text(f"Shield: {self.shield_health}", 18, WHITE, self.rect.centerx, self.rect.top - 20)

# This is the Enemy class where all the characteristics of the enemy are.
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size, points, fast=True):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.points = points
        self.fast = fast

    def update(self):
        if self.fast and self.rect.y > ENEMY_SLOWDOWN_DISTANCE:
            self.fast = False
        if self.fast:
            self.rect.y += 5
        else:
            self.rect.y += self.speed

# This is the Finalboss class where all the characteristics of the Final boss are.
class Finalboss(Enemy):
    def __init__(self):
        super().__init__(250, -100, (150, 140), 15, fast=False)
        self.image = pygame.transform.scale(Finalboss_img, (200, 190))
        self.rect = self.image.get_rect(centerx=SCREEN_WIDTH // 2)
        self.points = 15
        self.bosshits = 0
        self.health = FINAL_BOSS_HEALTH
        self.shoot_timer = pygame.time.get_ticks()
        self.speed=0.5

    def update(self):
        super().update()
        self.draw_health_bar()
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer > 5000:
            self.shoot()
            self.shoot_timer = current_time

    def shoot(self):
        for offset in [-20, 20]:
            bullet = Bullet(self.rect.centerx + offset, self.rect.bottom - 10, enemy_bullet, BULLET_SPEED)
            all_sprites.add(bullet)
            enemybullets.add(bullet)

    def draw_health_bar(self):
        bar_length = 100
        bar_height = 10
        fill = (self.health / FINAL_BOSS_HEALTH) * bar_length
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_length, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, RED, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 2)

# This is the Bullet class where all the characteristics of the bullet are.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img, speed):
        super().__init__()
        self.image = pygame.transform.scale(img, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(powerup_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            player.powered_up = True
            player.powerup_time = pygame.time.get_ticks() + 5000
            player.hasshield = final
            self.kill()

# This is the Scoretext class where all the characteristics of the score are.
class ScoreText(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.image = self.font.render(f"+{enemy.points}", True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alpha = 255

    def update(self):
        self.alpha -= 5
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)
            self.rect.y -= 1
# # This is the Enemywave class where all the characteristics of the enemywave are.
class EnemyWave:
    def __init__(self):
        self.enemies = []
        self.shoottime = 10

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def update(self):
        self.shoottime -= 1
        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.bottom >= SCREEN_HEIGHT:
                player.score -= 10
                if player.score < 0:
                    draw_text("YOU LOST!", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
                    pygame.mixer.music.load("Sounds/You Lose Sound Effect.mp3")
                    pygame.mixer.music.set_volume(40)
                    pygame.mixer.music.play()
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()
                enemy.kill()
                self.remove_enemy(enemy)
        if self.shoottime == 0 and len(self.enemies)>0 :
            shooter = self.enemies[random.randint(0, len(self.enemies) - 1)]
            self.shoottime = 10
            return Bullet(shooter.rect.centerx, shooter.rect.y, enemy_bullet, BULLET_SPEED)


# Create a player object
player = Player()

# Create a sprite group for the player
player_group = pygame.sprite.Group(player)

# Create a sprite group for all game sprites (including the player)
all_sprites = pygame.sprite.Group(player)

# Create empty sprite groups for enemies, bullets, powerups, and score texts
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
score_texts = pygame.sprite.Group()

# Initialize an enemy wave
enemy_wave = EnemyWave()

# Create a sprite group for the game logo
logo = pygame.sprite.Group()

# Create a sprite group for enemy bullets
enemybullets = pygame.sprite.Group()

# Initialize the final boss
finalBoss = Finalboss()
final_boss = pygame.sprite.Group(finalBoss)


def create_enemies(wave_num):
    # Clear the existing enemy wave
    enemy_wave.enemies.clear()
    num_enemies = WAVE_1_ENEMIES
    # Determine the number of enemies based on the wave number
    if wave_num == 1:
        num_enemies = WAVE_1_ENEMIES
    elif wave_num == 2:
        num_enemies = WAVE_2_ENEMIES
    else:
        num_enemies = FINAL_WAVE  # The final wave has a specific number of enemies
    # Keep track of enemy positions to avoid overlap
    positions = set()
    # Create the specified number of enemies
    for i in range(num_enemies):
        # Choose a random enemy size
        size = random.choice([(50, 30), (75, 45), (125, 75)])
        points = size[0] // 10
        x, y = random.randint(0, SCREEN_WIDTH - size[0]), random.randint(-1500, -50)
         # Ensure enemies don't overlap
        while any(abs(x - pos[0]) < size[0] and abs(y - pos[1]) < size[1] for pos in positions):
            x, y = random.randint(0, SCREEN_WIDTH - size[0]), random.randint(-1500, -50)
        positions.add((x, y))
        # Create an enemy object
        fast = True if i < CUTSCENE_ENEMIES else False
        enemy = Enemy(x, y, size, points, fast)
        # Add the enemy to sprite groups
        all_sprites.add(enemy)
        enemies.add(enemy)
        enemy_wave.add_enemy(enemy)



def spawn_powerup():
    x = random.randint(0, SCREEN_WIDTH - 20)
    y = random.randint(300, SCREEN_HEIGHT - 50)
    powerup = Powerup(x, y)
    all_sprites.add(powerup)
    powerups.add(powerup)

def main_menu():
     # Initialize the menu state
    menu = True
    
    # Load and scale the game logo image
    logo_image = pygame.transform.scale(logo_img, (400, 200))
    logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50))
    
    # Main menu loop
    while menu:
        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))
        screen.blit(logo_image, logo_rect)
        # Display menu options
        draw_text("Press ENTER to Start", 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, center=True)
        draw_text("Press C for Controls", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
        
        # Update the display
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Start the game and play effects
                    menu = False
                    tv_off_effect()
                    cinematic_intro()
                    hyperdrive_effect()
                    pygame.mixer.Sound.play(background_music)
                    pygame.mixer.music.set_volume(0.9)
                if event.key == pygame.K_c:
                    # Show controls screen
                    show_controls()

def show_controls():
    # Initialize the controls state
    controls = True
    # Main loop for displaying controls
    while controls:
       
        # Clear the screen
        screen.fill(BLACK)
       
        # Display the title "CONTROLS"
        draw_text("CONTROLS", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        
        # Display control instructions
        draw_text("Move: Arrow Keys", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        draw_text("Shoot: Space Bar", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, center=True)
        draw_text("Press ESC to go back", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
        
        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Exit the controls screen
                    controls = False

final = False

def main():
    global final # Indicates whether the final boss battle is active

    running = True
    clock = pygame.time.Clock()
    spawn_time = pygame.time.get_ticks()
    wave_num = 3
    create_enemies(wave_num) # Initialize enemies for the first wave
    while running:
        clock.tick(60) # Limit frame rate to 60 
        keys = pygame.key.get_pressed() # Get the state of keyboard keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Exit the game if the window is closed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                     # Shoot bullets when the Space Bar is pressed
                    player.shoot()
                    pygame.mixer.music.load("Sounds/shoot.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
        
        # Update player, bullets, powerups, and score texts
        player.update(keys)
        bullets.update()
        powerups.update()
        score_texts.update()

        # Spawn powerups 
        if pygame.time.get_ticks() - spawn_time > POWERUP_SPAWN_INTERVAL:
            spawn_powerup()
            spawn_time = pygame.time.get_ticks()

        # Update enemy wave and handle enemy bullets
        bullet = enemy_wave.update()
        if bullet is not None:
            all_sprites.add(bullet)
            enemybullets.add(bullet)
        bullets.update()
        enemybullets.update()
        score_texts.update()

        # Handle collisions between enemy bullets and player
        hits = pygame.sprite.groupcollide(enemybullets, player_group, True, False)
        for hit in hits:
            if not player.shielded:
                player.lives -= 1
                pygame.mixer.music.load("Sounds/explosion.wav")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                if player.lives == 0:
                    draw_text("YOU LOST!", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    pygame.mixer.music.load("Sounds/You Lose Sound Effect.mp3")
                    pygame.mixer.music.set_volume(20)
                    pygame.mixer.music.play()
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running = False
            # Handle player shield collisions with enemy bullets
            else: #player.shielded and pygame.sprite.spritecollide(player, enemybullets, True):
                player.shield_health -= 1
                if player.shield_health <= 0:
                    player.deactivate_shield()
                

        # Check if the final boss battle is active
        if not final:
            # Handle collisions between player bullets and enemies
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for hit in hits.values():
                for enemy in hit:
                    player.score += enemy.points
                    score_text = ScoreText(enemy.rect.centerx, enemy.rect.centery, enemy)
                    all_sprites.add(score_text)
                    score_texts.add(score_text)
                    enemy_wave.remove_enemy(enemy)
                    pygame.mixer.music.load("Sounds/invaderkilled.wav")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play()
            
            # Check if all enemies are defeated in the final wave
            if not enemies and wave_num == 3:
                # Activate the final boss battle
                boss_cinematic_entry()
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(finalboss_music)
                enemy_wave.add_enemy(finalBoss)
                enemies.add(finalBoss)
                all_sprites.add(finalBoss)
                
                final = True

        else:
            # Check for collisions between player bullets and enemies
            hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
            #print(hits)
            if len(hits)>0:
                print(hits)
                # Reduce the health of the final boss
                finalBoss.health -= 1
                finalBoss.draw_health_bar()
                if finalBoss.health <= 0:
                    # Play explosion sound and remove the final boss
                    pygame.mixer.Sound.play(explosion_sound)
                    enemy_wave.remove_enemy(finalBoss)
                    enemies.remove(finalBoss)
                    tv_off_effect()
                    
                    # Display win message
                    draw_text("YOU DID IT.. YOU SAVED THE UNIVERSE!", 58, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    
                    # Prompt user to play again
                    draw_text("However, there are more universes in need of saving,", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
                    draw_text("Do you want to play again? Y/N", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.4, center=True)
                    pygame.display.flip()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_y:
                                    main_menu()
                                    main()
                                if event.key == pygame.K_n:
                                    pygame.quit()
                                    sys.exit()
        if finalBoss.rect.bottom>410:
            draw_text("YOU LOST!", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.mixer.music.load("Sounds/You Lose Sound Effect.mp3")
            pygame.mixer.music.set_volume(20)
            pygame.mixer.music.play()
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        if not enemies and not final:
            # Display "WAVE COMPLETE!" message
            draw_text("WAVE COMPLETE!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.flip()
            pygame.time.wait(2000)
            wave_num += 1
            if wave_num > 3:
                # If all waves are completed, display "YOU WIN!" message
                draw_text("YOU WIN!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            else:
                # Create enemies for the next wave and remove existing bullets
                create_enemies(wave_num)
                for bullet in bullets:
                    bullet.kill()
        # Refresh the screen and display relevant information
        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        if player.shielded:
            player.draw_shield()
        draw_text(f"Score: {player.score}", 24, WHITE, SCREEN_WIDTH // 2, 10)
        draw_text(f"Lives: {player.lives}", 24, WHITE, SCREEN_WIDTH - 60, 10)
        if wave_num <= 3:
            draw_text(f"Wave: {wave_num}", 24, WHITE, 40, 10)
        else:
            draw_text("LAST!", 24, WHITE, 40, 10)
        pygame.display.flip()
# exit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
    main()
