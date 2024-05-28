import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# settings man
PLAYER_SPEED = 5
ENEMY_SPEED = 1
BULLET_SPEED = 7
ENEMY_DROP = 30
POWERUP_SPAWN_INTERVAL = 5000  # milliseconds
MAX_BULLETS = 3
MAX_WINS = 3
WAVE_1_ENEMIES = 30
WAVE_2_ENEMIES = 40
ENEMY_SLOWDOWN_DISTANCE = 25 
CUTSCENE_ENEMIES = 7  


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")


player_img = pygame.image.load('Images/invaders.png').convert_alpha()
enemy_img = pygame.image.load('Images/EnemyShip.png').convert_alpha()
bullet_img = pygame.image.load('Images/bullett.png').convert_alpha()
powerup_img = pygame.image.load('Images/Powerup.png').convert_alpha()
enemy_bullet = pygame.image.load('Images/EnemyBullet.png').convert_alpha()
background_img = pygame.image.load('Images/StarBackground.png').convert_alpha()
logo_img = pygame.image.load('Images\Logo1.png').convert_alpha()
hyperdrive_sound = pygame.mixer.Sound('Sounds/HyperDrive.mp3')
background_music = pygame.mixer.Sound('Sounds/SpaceInvadersmusic.mp3')
lose_sound=pygame.mixer.Sound('Sounds\You Lose Sound Effect.mp3')



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
    pygame.time.wait(500)
    draw_text("GO!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.fill(BLACK)
    pygame.display.flip()

def cinematic_intro():
    draw_text("So it begins...", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    pygame.display.flip()
    pygame.time.wait(1000)
    pygame.mixer.Sound.play(hyperdrive_sound)
    pygame.mixer.music.set_volume(0.01)
    pygame.time.wait(2000)
    screen.fill(BLACK)
    pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0
        self.wins = 0
        self.powered_up = False
        self.powerup_time = 0

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
            self.kill()

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

class EnemyWave:
    def __init__(self):
        self.enemies = []
        self.shoottime=10

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def update(self):
        self.shoottime-=1
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
        if self.shoottime==0:
            shooter= self.enemies[random.randint(0,len(self.enemies)-1)]
            self.shoottime=10
            return Bullet(shooter.rect.centerx, shooter.rect.y, enemy_bullet, BULLET_SPEED)

player = Player()
player_group = pygame.sprite.Group(player)
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
score_texts = pygame.sprite.Group()
enemy_wave = EnemyWave()
logo = pygame.sprite.Group()
enemybullets= pygame.sprite.Group()

def create_enemies(wave_num):
    enemy_wave.enemies.clear()
    num_enemies = WAVE_1_ENEMIES if wave_num == 1 else WAVE_2_ENEMIES
    positions = set()
    for i in range(num_enemies):
        size = random.choice([(50, 30), (75, 45), (125, 75)])
        points = size[0] // 10
        x, y = random.randint(0, SCREEN_WIDTH - size[0]), random.randint(-1500, -50)
        while any(abs(x - pos[0]) < size[0] and abs(y - pos[1]) < size[1] for pos in positions):
            x, y = random.randint(0, SCREEN_WIDTH - size[0]), random.randint(-1500, -50)
        positions.add((x, y))
        fast = True if i < CUTSCENE_ENEMIES else False
        enemy = Enemy(x, y, size, points, fast)
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
    menu = True
    logo_image = pygame.transform.scale(logo_img, (400, 200))
    logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3-50))
    while menu:
        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))
        screen.blit(logo_image, logo_rect)
        draw_text("Press ENTER to Start", 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+30, center=True)
        draw_text("Press C for Controls", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    tv_off_effect()
                    cinematic_intro()
                    hyperdrive_effect()
                    pygame.mixer.Sound.play(background_music)
                    pygame.mixer.music.set_volume(0.7)
                if event.key == pygame.K_c:
                    show_controls()

def show_controls():
    controls = True
    while controls:
        screen.fill(BLACK)
        draw_text("CONTROLS", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        draw_text("Move: Arrow Keys", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        draw_text("Shoot: Space Bar", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, center=True)
        draw_text("Press ESC to go back", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    controls = False

def main():
    running = True
    clock = pygame.time.Clock()
    spawn_time = pygame.time.get_ticks()
    wave_num = 1
    create_enemies(wave_num)
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    player.shoot()
                    pygame.mixer.music.load("Sounds/shoot.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()

        player.update(keys)
        bullets.update()
        powerups.update()
        score_texts.update()
        

        if pygame.time.get_ticks() - spawn_time > POWERUP_SPAWN_INTERVAL:
            spawn_powerup()
            spawn_time = pygame.time.get_ticks()

        bullet= enemy_wave.update()
        if bullet != None:
            all_sprites.add(bullet)
            enemybullets.add(bullet)
        bullets.update()
        enemybullets.update()
        score_texts.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits.values():
            for enemy in hit:
                player.score += enemy.points
                score_text = ScoreText(enemy.rect.centerx, enemy.rect.centery,enemy)
                all_sprites.add(score_text)
                score_texts.add(score_text)
                enemy_wave.remove_enemy(enemy)
                pygame.mixer.music.load("Sounds/invaderkilled.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()

        hits = pygame.sprite.groupcollide(enemybullets, player_group, True, False)
        if hits:
            player.lives-=1 
            player
            pygame.mixer.music.load("Sounds/explosion.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            if player.lives==0:
                draw_text("YOU LOST!", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.mixer.music.load("Sounds\You Lose Sound Effect.mp3")
                pygame.mixer.music.set_volume(20)
                pygame.mixer.music.play()
                pygame.display.flip()
                pygame.time.wait(2000)
                running= False

        if not enemies:
            draw_text("WAVE COMPLETE!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.flip()
            pygame.time.wait(2000)
            wave_num += 1
            if wave_num > 2:
                draw_text("YOU WIN!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            else:
                create_enemies(wave_num)
                for bullet in bullets:
                    bullet.kill()

        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(f"Score: {player.score}", 24, WHITE, SCREEN_WIDTH // 2, 10)
        draw_text(f"Lives: {player.lives}", 24, WHITE, SCREEN_WIDTH - 60, 10)
        draw_text(f"Wave: {wave_num}", 24, WHITE, 40, 10)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
    main()
