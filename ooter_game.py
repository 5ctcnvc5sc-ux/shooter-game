from pygame import *
from random import randint
import time as tm
init()
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, filename, width, height, x, y, step = 5):
        super().__init__()
        self.image = image.load(filename)
        self.rect = Rect(x, y, width, height)
        self.image = transform.scale(self.image, (width, height))
        self.x = x
        self.y = y
        self.step = step
        self.start_x = x
        self.start_y = y

    def draw(self):
        self.rect.x = self.x
        self.rect.y = self.y
        window.blit(self.image, (self.x, self.y))

class Player(GameSprite):
    bullets = sprite.Group()
    start_time = 0
    cooldown = 0.25
    fireable = False
    shot_ufos = 0
    missed_ufos = 0
    lives = 3

    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.x < window_size[0] - self.rect.width: self.x += self.step 
        if keys[K_a] and self.x > 0: self.x -= self.step 
        mouse_buttons = mouse.get_pressed()
        if mouse_buttons[0]:
            self.fire()

    def fire(self):
        if self.fireable:
            laser_gunshot.play()
            self.fireable = False
            self.start_time = tm.time()
            centerx = self.rect.centerx
            centery = self.rect.centery
            bullet= Bullet('bullet.png', 5, 20, centerx, centery - 10, 5)
            self.bullets.add(bullet) 

class Bullet(GameSprite):
    def update(self):
        self.y = self.y - self.step
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y < 0:
            self.kill()

class Ufo(GameSprite):
    def update(self):
        self.y = self.y + self.step
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y > window_size[1]:
            rocket.missed_ufos += 1
            missed_ufos.set_number(rocket.missed_ufos)
            self.kill()
            ufo = Ufo('ufo.png', 80, 80, randint(0, 620), randint(-160, -80), 2)
            ufos.add(ufo)

class Asteroid(GameSprite):
    def update(self):
        self.y = self.y + self.step
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y > window_size[1]:
            self.kill()
            asteroid_size = randint (40, 80)
            asteroid = Asteroid('asteroid.png', asteroid_size, asteroid_size,
                                     randint(0, 620), randint(-160, -80), 2)
            asteroids.add(asteroid)

class Label:
    def __init__(self, text, color, x, y, size):
        self.font = font.SysFont('verdana', size)
        self.label = self.font.render(text, True, color)
        self.text = text
        self.color = color
        self.coords = (x, y)

    def draw(self):
        window.blit(self.label, self.coords)

    def set_number(self, number):
        self.label = self.font.render(f'{self.text}: {number}', True, self.color)

#play background music
mixer.music.load('space.ogg')
mixer.music.set_volume(0.15)
mixer.music.play()

#add new background music for win / lose


metal_hit = mixer.Sound('metal_hit.mp3')
laser_gunshot = mixer.Sound('laser_gunshot.mp3')
stone_thud = mixer.Sound('stone_thud.mp3')

window = display.set_mode((700, 500))
clock = time.Clock() #timer
window_size = window.get_size()

background = image.load('galaxy.jpg') 
background = transform.scale(background, window_size)

rocket = Player('rocket.png', 70, 70, 350, 400)

missed_ufos = Label('Missed Ufos', (193, 189, 219), 10, 10, 20)
shot_ufos = Label('Shot Ufos', (193, 189, 219), 30, 40, 20)
rocket_lives = Label('Lives', (237, 136, 116), 30, 70, 20)
winner_text = Label('You saved planet Earth!', (255, 255, 255), 120, 220, 30)
loser_text = Label('Aliens captured planet Earth!!', (255, 0, 0), 120, 220, 30)

missed_ufos.set_number(0)
shot_ufos.set_number(0)
rocket_lives.set_number(rocket.lives)

ufos = sprite.Group()
for _ in range(5):
    ufo = Ufo('ufo.png', 80, 80, randint(0, 620), randint(-160, -80), 2)
    ufos.add(ufo)

asteroids = sprite.Group()
for _ in range(2):
    asteroid_size = randint(40, 80)
    asteroid = Asteroid('asteroid.png', asteroid_size, asteroid_size,
                                     randint(0, 620), randint(-160, -80), 2)
    asteroids.add(asteroid)

player_rocket = sprite.Group()
player_rocket.add(rocket)

'''ufo =  [Enemy('ufo.png', 70, 70, 750, 310, 5, 650, 950, ),
        Enemy('ufo.png', 70, 70, 1180, 310, 5, 50, 930, )d

                ]'''

game_on = True
game_result = False
while game_on:
    for game_event in event.get():
        #k_q meaning the key q on your keyboard
        if game_event.type == QUIT:
            game_on = False
        if game_event.type == KEYDOWN:
            if game_event.key == K_ESCAPE:
                game_on = False

    if not game_result:
        current_time = tm.time()
        if rocket.fireable == False and current_time - rocket.start_time > rocket.cooldown:
            rocket.fireable = True

        number = sprite.groupcollide(rocket.bullets, ufos, True, True)
        for x in number:
            metal_hit.play()
            rocket.shot_ufos += 1
            shot_ufos.set_number(rocket.shot_ufos)
            ufo = Ufo('ufo.png', 80, 80, randint(0, 620), randint(-160, -80), 2)
            ufos.add(ufo)

        number = sprite.groupcollide(ufos, player_rocket, True, False)
        for x in number:
            metal_hit.play()
            rocket.lives -= 1
            rocket_lives.set_number(rocket.lives)
            ufo = Ufo('ufo.png', 80, 80, randint(0, 620), randint(-620, -80), 2)
            ufos.add(ufo)

        number = sprite.groupcollide(asteroids, player_rocket, True, False)
        for x in number:
            stone_thud.play()
            rocket.lives -= 1
            rocket_lives.set_number(rocket.lives)
            asteroid_size = randint(40, 80)
            asteroid = Asteroid('asteroid.png', asteroid_size, asteroid_size,
                                     randint(0, 620), randint(-160, -80), 2)
            asteroids.add(asteroid)

        number = sprite.groupcollide(asteroids, rocket.bullets, False, True)

            
        rocket.update()
        rocket.bullets.update()
        ufos.update()
        asteroids.update()


    window.fill((0, 0, 255))
    window.blit(background, (0, 0))
            
    rocket.draw()
    
    rocket.bullets.draw(window)
    ufos.draw(window)

    asteroids.draw(window)

    missed_ufos.draw()
    shot_ufos.draw()
    rocket_lives.draw()

    if rocket.lives <=0 or rocket.missed_ufos > 5:
        loser_text.draw()
        game_result = True

    if rocket.shot_ufos > 9:
        winner_text.draw()
        if game_result == False:
            game_result = True
            mixer.music.load('win.mp3')
            mixer.music.play()

    display.update()
    clock.tick(60) #fps frames per second
