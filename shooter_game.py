from pygame import *
import random
import time as timer

Win_HEGIHT = 500
Win_WIDTH = 700
FPS = 40

lost = 0
score = 0
live = 3

window = display.set_mode((Win_WIDTH, Win_HEGIHT))
display.set_caption('Space')

clock = time.Clock()

background = transform.scale(image.load('erd.jpg'), (Win_WIDTH, Win_HEGIHT))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Button(sprite.Sprite):
    def __init__(self, reference_image, pos_x, pos_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(reference_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
    def click(self, function):
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if self.rect.collidepoint(pos):
                function()
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x <= Win_WIDTH - 5:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 15, 20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= Win_HEGIHT:
            lost += 1
            self.rect.y = -75
            self.x = random.randint(5, Win_WIDTH-75)
            self.speed = random.randint(1, 5)

class asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= Win_HEGIHT:
            self.rect.y = -75
            self.x = random.randint(5, Win_WIDTH-75)
            self.speed = random.randint(1, 5)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <=  -20:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_song = mixer.Sound('fire.ogg')

player = Player('ew.png', 5,Win_HEGIHT - 100, 10, 100, 100)
reset_button = Button('asteroid.png', 200, 200, 80, 50)
def restert_game():
    global score, lost, num_bullets, monsters, bullets, asteroids, finish
    for b in bullets:
        b.kill()
    for m in monsters:
        m.kill()
    for h in asteroids:
        h.kill()

        
    player.rect.x = 5
    player.rect.y = Win_HEGIHT - 100
    for i in range(10):
        x = random.randint(5, Win_WIDTH-75)
        speed = random.randint(1, 2)
        enemy = Enemy('qwe.png', x, -75, speed, 100, 150)
        monsters.add(enemy)
    for i in range(2):
        x = random.randint(5, Win_WIDTH-75)
        speed = random.randint(1, 3)
        enemy = asteroid('ew.png', x, -75, speed, 100, 100)
        asteroids.add(enemy)
    score = 0
    lost = 0
    num_bullets = 0
    live = 3
    finish = False

asteroids = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

for i in range(10):
    x = random.randint(5, Win_WIDTH-75)
    speed = random.randint(1, 2)
    enemy = Enemy('qwe.png', x, -75, speed, 100, 150)
    monsters.add(enemy)

for i in range(2):
    x = random.randint(5, Win_WIDTH-75)
    speed = random.randint(1, 3)
    enemy = asteroid('ew.png', x, -75, speed, 100, 100)
    asteroids.add(enemy)

game = True
finish = False
font.init()
font_score = font.SysFont('Arial', 36)

font_end = font.SysFont('Arial', 70)
win = font_end.render('Вы выиграли', True, (2, 31, 245))
lose =  font_end.render('Вы проиграли',  True, (2, 31, 245))
reload_text = font_score.render('Перезарядка',  True, (2, 31, 245))
draw_and_text = None

num_bullets = 0
rel_time = False
start_rel = None

finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and not finish:
            if e.key == K_SPACE:
                if num_bullets < 5:
                    player.fire()
                    fire_song.play()
                    num_bullets += 1
                else:
                    rel_time = True
                    start_rel = timer.time()


    window.blit(background, (0,0))

    if not finish:
        if rel_time:
            now_time = timer.time()
            window.blit(reload_text,(200, 450))
            if now_time - start_rel >= 1:
                rel_time = False
                num_bullets = 0

        text_lost = font_score.render('Пропущено'+ str(lost), True, (2, 31, 245))
        window.blit(text_lost, (10, 30))
        text_win = font_score.render('Счет'+ str(score), True, (2, 31, 245))
        window.blit(text_win, (15, 60))
        
        monsters.draw(window)
        asteroids.draw(window)
        player.update()
        player.reset()
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.update()

        collide_bullets_and_enemy = sprite.groupcollide(monsters, bullets, True, True)
        for _ in collide_bullets_and_enemy:
            score += 1
            x = random.randint(5, Win_WIDTH-75)
            speed = random.randint(1, 2)
            enemy = Enemy('qwe.png', x, -75, speed, 100, 150)
            monsters.add(enemy)

        if sprite.spritecollide(player, monsters, True):
            live -= 1
        if lost >= 6:
            finish = True
            draw_and_text = lose
        if score >= 6:
            finish = True
            draw_and_text = win

        if sprite.spritecollide(player, asteroids, False):
            finish = True
            draw_and_text = lose
         

        if live == 0:
            finish = True
            draw_and_text = lose
      
    elif finish:
        window.blit(draw_and_text,(200, 200))
        reset_button.click(restert_game)
        reset_button.reset()
        

    display.update()
    clock.tick(FPS)

    

