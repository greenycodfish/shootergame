from pygame import *
from random import randint

#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        super().__init__() #sprite.Sprite.__init__(self)
 
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#child class for player
class Player(GameSprite):
    #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-15)
        bullets.add(bullet)

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            missed = missed + 1

class Obstacle (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            

score = 0
missed = 0
goal = 10
max_lost = 3
lives = 3
life_colour = (0,0,0)

font.init()
displayText = font.Font(None, 36)

endText = font.Font(None, 80)
WIN = endText.render("You win!", True, (235,52,116))
LOSE = endText.render("You lose!", True, (250,250,50))

#we need the following images
img_bg = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ducks.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

#window properties
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter game")
background = transform.scale(image.load(img_bg), (win_width, win_width))

#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 12)
bullets = sprite.Group()

UFOs = sprite.Group()
for i in range(1,6):
    ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    UFOs.add(ufo)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Obstacle(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)

#background music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg") #sound effect for bullet

#game loop
game = True #exit with "close window"
finish = False #end with win/lose
FPS = 60
clock = time.Clock()

while game:
    #exit when "close window" is clicked
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    #end the game when win/lose
    if not finish:
        #update the background
        window.blit(background, (0,0))

        #update the Player
        bullets.update()
        ship.update()
        ship.reset()

        UFOs.update()
        UFOs.draw(window)
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        collides = sprite.groupcollide(UFOs, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            UFOs.add(ufo)

        if sprite.spritecollide(ship, UFOs, False) or sprite.spritecollide(ship, asteroids, False):
            lives -= 1

        if missed >= max_lost or lives == 0:
            finish = True
            window.blit(LOSE, (200,200))

        if score >= goal:
            finish = True
            window.blit(WIN, (200,200))
        
        if lives == 3:
            life_colour = (173,255,47)
        if lives == 2:
            life_colour = (255,255,0)
        if lives == 1:
            life_colour = (255,0,0)

        LIVES = displayText.render(str(lives) + "lives", 1, life_colour)
        window.blit(LIVES, (600,10))

        SCORE = displayText.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(SCORE, (10,10))

        MISSED = displayText.render("Missed: " + str(missed), 1, (255,255,255))
        window.blit(MISSED, (10,40))
        #update the window
        display.update()
        clock.tick(FPS)

    else:
        finish = False
        score = 0
        missed = 0
        for b in bullets:
            b.kill()
        for e in UFOs:
            e.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(1,6):
            ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            UFOs.add(ufo)

        for i in range(1,3):
            asteroid = Obstacle(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            asteroids.add(asteroid)

    time.delay(0)