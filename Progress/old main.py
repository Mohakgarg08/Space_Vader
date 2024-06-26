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
MAX_WINS=3



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

def sign(num):
    if num< 0:
        return -1
    elif num> 0:
        return 1
    else: 
        return 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images/invaders.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0
        self.wins= 0 
    
    def win(self):
        self.wins+=1
        
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 300:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 595:
            self.rect.y += self.speed
            

class Powerups(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(50,50)):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def update(self):
        self.rect.x == 0
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(40, 30)):
        super().__init__()
        self.image = pygame.image.load('Images/EnemyShip.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        #self.image = pygame.Surface(size)
        #self.image.fill(RED)
        #self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x += self.speed
        return self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0
    

class Enemy_Wave():
    def __init__(self):
        self.enemies= []
        self.wavelost= False
        self.shoottime= 5
        self.speed= ENEMY_SPEED
        self.enemycount=0
        self.direction=1
        self.droptime=0

    def setenemycount(self, enemycount):
        self.enemycount=enemycount

    def addenemy(self, enemy):
        self.enemies.append(enemy)

    def removeenemy(self, enemy):
        self.enemies.remove(enemy)

    def update(self):
        self.droptime-=1
        self.speed= (ENEMY_SPEED+0.125*(self.enemycount-len(self.enemies)))*self.direction
        shoulddrop=False 
        for enemy in enemies:
            enemy.speed=self.speed
            if enemy.update():
                shoulddrop= True
        if shoulddrop and self.droptime<=0:
            self.droptime=10
            self.direction*=-1
            for enemy in enemies:
                enemy.rect.y+= ENEMY_DROP
                #enemy.speed=-enemy.speed
                if enemy.rect.y>=SCREEN_HEIGHT-50:
                    self.wavelost= True
        self.shoottime-=1
        if self.shoottime==0:
            self.shoottime=50
            return random.randint(0,len(self.enemies)-1)


class FinalBoss(pygame.sprite.Sprite):
    def __init__():
        pass
        


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,color, speed):
        super().__init__()
        self.image = pygame.image.load('Images/bullett.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        #self.image = pygame.Surface((5, 15))
        #self.image.fill(color)
        #self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
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
        self.image = pygame.image.load('Images/Logo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.bottom = 250


player = Player()
playergroup= pygame.sprite.Group(player)
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
score_texts = pygame.sprite.Group()
wave=Enemy_Wave()
logo=pygame.sprite.Group(Logo())





def create_enemies():
    wave.enemies.clear()
    wave.setenemycount(8*4)
    for i in range(8):
        for j in range(4):
            enemy = Enemy(100 + i * 80, 50 + j * 50)
            all_sprites.add(enemy)
            enemies.add(enemy)
            wave.addenemy(enemy)
            
            
create_enemies()

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        logo.draw(screen)

        #img = pygame.image.load('Images/Logo.png').convert_alpha()
        #pygame.transform.scale(img,(100, 1))
        #screen.blit(img, (0, 0))
        
        draw_text("Press ENTER to Start", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press C for Controls", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load("Sounds/SpaceInvadersmusic.wav")
                    pygame.mixer.music.set_volume(60)
                    pygame.mixer.music.play()
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

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = Bullet(player.rect.centerx, player.rect.top, BLUE, BULLET_SPEED)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pygame.mixer.music.load("Sounds/shoot.wav")
                    pygame.mixer.music.set_volume(40)
                    pygame.mixer.music.play()
            

        player.update(keys)
        #enemies.update()
        shootingenemy= wave.update()
        if shootingenemy != None:
            for enemy in enemies:
                if shootingenemy==0:
                    bullet = Bullet(enemy.rect.centerx, enemy.rect.top, RED, -BULLET_SPEED)
                    all_sprites.add(bullet)
                    enemybullets.add(bullet)
                    break
                shootingenemy-=1
        bullets.update()
        enemybullets.update()
        score_texts.update()


        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        if hits:
            for hit in hits.values():
                for enemy in hit:
                    player.score += 1
                    score_text = ScoreText(enemy.rect.centerx, enemy.rect.centery)
                    all_sprites.add(score_text)
                    score_texts.add(score_text)
                    wave.removeenemy(enemy)
                    pygame.mixer.music.load("Sounds/invaderkilled.wav")
                    pygame.mixer.music.set_volume(40)
                    pygame.mixer.music.play()

        
        hits = pygame.sprite.groupcollide(enemybullets, playergroup, True, False)
        if hits:
            player.lives-=1 
            player
            pygame.mixer.music.load("Sounds/explosion.wav")
            pygame.mixer.music.set_volume(40)
            pygame.mixer.music.play()
            if player.lives==0:
                draw_text("YOU LOST!", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.mixer.music.load("Sounds\You Lose Sound Effect.mp3")
                pygame.mixer.music.set_volume(60)
                pygame.mixer.music.play()
                pygame.display.flip()
                pygame.time.wait(2000)
                running= False

       # if player.score >= POINT_THRESHOLD:
        #    for enemy in enemies:
         #       enemy.kill()
          #  for i in range(8):
           #     for j in range(4):
            #        enemy = Enemy(100 + i * 80, 50 + j * 50, size=(60, 45))
             #       ENEMY_SPEED = 5
              #      all_sprites.add(enemy)
               #     enemies.add(enemy)

        if not enemies:
            draw_text("YOU WIN!", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            player.win()
            pygame.display.flip()
            pygame.time.wait(2000)
            if player.wins>=MAX_WINS:
                running = False
            else:
                create_enemies()
                for bullet in bullets:
                    bullet.kill()
        if wave.wavelost:
            draw_text("YOU LOST!", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.mixer.music.load("Sounds\You Lose Sound Effect.mp3")
            pygame.mixer.music.set_volume(100)
            pygame.mixer.music.play()
            pygame.display.flip()
            pygame.time.wait(2000)
            running= False

        #this just makes eeverything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(f"Score: {player.score}", 18, WHITE, SCREEN_WIDTH // 2, 10)
        draw_text(f"Lives: {player.lives}", 18, WHITE, SCREEN_WIDTH - 60, 10)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
    main()


# citing my work
    # https://www.pygame.org/docs/
