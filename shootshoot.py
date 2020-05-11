# Plese install pygame first!

# 'python3 -m pip install -U pygame --user'

# Get link 'https://www.pygame.org/wiki/GettingStarted'

import pygame
import os
import random
from os import path


#Geometry
WIDTH = 500
HEIGHT = 600 
FPS = 30 #Frame Rate Per Second

#Color
bgcolor = (225, 245, 241)
white = (255, 255, 255)
blue = (18, 69, 199)
sea = (159, 192, 245)
black = (0, 0, 0)
green = (0, 255, 0)



#Initialize pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shoot Shoot')
clock = pygame.time.Clock()

#Ceate
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

print('game Folder')
print(game_folder)

#insert sound
bulletSound = pygame.mixer.Sound('sound\8bit_gunloop_explosion.wav')
# boomSound = pygame.mixer.Sound('sound\8bit_bomb_explosion.wav')

# music = pygame.mixer.music.load('sound\Action1 - Encounter With The Witches.ogg')
# pygame.mixer.music.play(-1)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newenemy(): 
    em = Enemy()
    all_sprites.add(em)
    enemy.add(em)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

class Submarine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sub_img = os.path.join(img_folder,'submarine.png')

        self.image = pygame.image.load(sub_img).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100



    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10 

        if keystate[pygame.K_UP]:
            self.speedy = -10

        if keystate[pygame.K_DOWN]:
            self.speedy = 10 

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        em_img = os.path.join(img_folder,'enemy2.png')

        self.image = pygame.image.load(em_img).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

    

class Bullet(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bul_img = os.path.join(img_folder,'bullet.png')
        
    
        self.image = pygame.image.load(bul_img).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
    

# Load game graphic
background =  pygame.image.load(os.path.join(img_folder,'seaFull.jpg')).convert()
background_rect = background.get_rect()

# sprite is a player
all_sprites = pygame.sprite.Group()

#Add Submarine
submarine = Submarine()
all_sprites.add(submarine)        

enemy = pygame.sprite.Group()

bullets = pygame.sprite.Group()

for i in range(10):
    newenemy()

score = 0

#Game loop
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        #Check for closing
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                submarine.shoot()
                # bulletSound.play()
                

    all_sprites.update()


    #check hits enemy
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    
    if hits:
        score += 20
        # boomSound.play()
        newenemy()
        print(hits)

    hits = pygame.sprite.spritecollide(submarine, enemy, True)
    if hits:
        submarine.shield -= 20
        newenemy()
        if submarine.shield <=0:
            running = False

    # Draw / render
    screen.fill(sea)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 15)
    draw_shield_bar(screen, 5, 5, submarine.shield)

    pygame.display.flip()

pygame.quit()

