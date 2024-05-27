import pygame
import random

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 7
ENEMY_DROP = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAX_BULLETS = 3
MAX_WINS = 2


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")


PLAYER_IMAGE = pygame.image.load('Images/invaders.png').convert_alpha()
ENEMY_IMAGE = pygame.image.load('Images/EnemyShip.png').convert_alpha()
BULLET_IMAGE = pygame.image.load('Images/bullett.png').convert_alpha()
LOGO_IMAGE = pygame.image.load('Images/Logo.png').convert_alpha()

def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_IMAGE, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0
        self.wins = 0
        self.powered_up = False
        self.powerup_time = 0

    def win(self):
        self.wins += 1

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
                bullet = Bullet(self.rect.centerx + offset, self.rect.top, BLUE, BULLET_SPEED)
                all_sprites.add(bullet)
                bullets.add(bullet)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top, BLUE, BULLET_SPEED)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            player.powered_up = True
            player.powerup_time = pygame.time.get_ticks() + 5000
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(50, 30)):
        super().__init__()
        self.image = pygame.transform.scale(ENEMY_IMAGE, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += ENEMY_DROP
        if self.rect.top >= SCREEN_HEIGHT:
            player.score -= 1
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed):
        super().__init__()
        self.image = pygame.transform.scale(BULLET_IMAGE, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

class ScoreText(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.image = self.font.render("+1", True, WHITE)
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

class Logo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(LOGO_IMAGE, (400, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.bottom = 250

player = Player()
playergroup = pygame.sprite.Group(player)
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
score_texts = pygame.sprite.Group()
logo = pygame.sprite.Group(Logo())

def create_enemies(wave_number):
    for i in range(8):
        for j in range(4):
            enemy = Enemy(100 + i * 80, 50 + j * 50)
            all_sprites.add(enemy)
            enemies.add(enemy)

def spawn_powerup():
    x = random.randint(0, SCREEN_WIDTH - 20)
    y = random.randint(300, SCREEN_HEIGHT - 50)
    powerup = Powerup(x, y)
    all_sprites.add(powerup)
    powerups.add(powerup)

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def countdown():
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        text = font.render(str(i), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)
    screen.fill(BLACK)
    text = font.render("GO!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)

def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        logo.draw(screen)
        draw_text("Press ENTER to Start", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press C for Controls", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    countdown()
                    menu = False
                if event.key == pygame.K_c:
                    show_controls()

def show_controls():
    controls = True
    while controls:
        screen.fill(BLACK)
        draw_text("CONTROLS", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text("Move: Arrow Keys", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Shoot: Space Bar", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        draw_text("Press ESC to go back", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    controls = False

def win_screen():
    screen.fill(BLACK)
    draw_text("You Win!", 74, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    running = True
    clock = pygame.time.Clock()
    wave = 1
    create_enemies(wave)

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
                    pygame.mixer.music.set_volume(40)
                    pygame.mixer.music.play()

        player.update(keys)
        bullets.update()
        enemies.update()
        powerups.update()
        score_texts.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        if hits:
            for hit in hits.values():
                for enemy in hit:
                    player.score += 1
                    score_text = ScoreText(enemy.rect.centerx, enemy.rect.centery)
                    all_sprites.add(score_text)
                    score_texts.add(score_text)
                    pygame.mixer.music.load("Sounds/invaderkilled.wav")
                    pygame.mixer.music.set_volume(40)
                    pygame.mixer.music.play()

        if player.wins >= MAX_WINS:
            win_screen()
            running = False

        if len(enemies) == 0:
            player.win()
            if player.wins < MAX_WINS:
                wave += 1
                create_enemies(wave)
                spawn_powerup()

        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(f"Lives: {player.lives}", 18, WHITE, 50, 10)
        draw_text(f"Score: {player.score}", 18, WHITE, SCREEN_WIDTH // 2, 10)
        draw_text(f"Wins: {player.wins}", 18, WHITE, SCREEN_WIDTH - 50, 10)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
    main()
