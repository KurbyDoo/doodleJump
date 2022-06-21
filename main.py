import pygame
import sys
import os
from random import randint, choice

pygame.init()

# GLOBAL VAR
FPS = 60


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.xVelo = 0
        self.yVelo = 0
        self.distanceTravelled = 0

        # self.image = pygame.Surface((75, 150))
        # self.image.fill((0, 200, 0))

        self.image = pygame.transform.rotozoom(pygame.image.load('DoodlerCropped.png').convert_alpha(), 0, 0.5)
        self.rect = self.image.get_rect(center = (screen.get_width()/2, screen.get_height() * 0.6))
        self.rect.height *= 0.9
        self.rect.width *= 0.9

    def __repr__(self) -> str:
        return f"{super().__repr__()} object as the player"
    
    def updateKeys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.xVelo -= 1
            self.image = pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load('Doodler.png'), 0, 0.5), True, False)

        if keys[pygame.K_RIGHT]:
            self.xVelo += 1
            self.image = pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load('Doodler.png'), 0, 0.5), False, False)


        # if keys[pygame.K_UP]:
        self.rect.y += 1
        for platform in platforms.sprites():
            if platform.rect.colliderect(self.rect) and self.yVelo > 0 and platform.rect.bottom > player.sprite.rect.bottom:
                if platform.type == 'spring':
                    self.yVelo = -60 - ((player.sprite.distanceTravelled // -2000) * (randint(5, 20) / 10))
                else: self.yVelo = -40 - (player.sprite.distanceTravelled // -10000)
                break
    
        self.rect.y -= 1

        if keys[pygame.K_DOWN]:
            self.yVelo += 1

    def updateVelocity(self):
        self.distanceTravelled += self.yVelo

        self.rect.x += int(self.xVelo)

        if self.rect.right < 0:
            self.rect.left = screen.get_width()

        if self.rect.left > screen.get_width():
            self.rect.right = 0

        self.yVelo += 0.5

        self.xVelo *= 0.95
        self.yVelo *= 0.99

    def update(self):
        self.updateKeys()
        self.updateVelocity()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, number = None, width = 150, height = 30, fill = (110,182,66), image = 'Platform.png', type = 'default') -> None:
        super().__init__()

        # self.image = pygame.Surface((width, height))
        # self.image.fill(fill)

        self.image = pygame.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(midtop = (x, y))
        # self.rect.height *= 0.3

        self.type = type


    def updateMovement(self):
        global highestPlatform
        # self.rect.x -= int(player.sprite.xVelo)
        self.rect.y -= int(player.sprite.yVelo)

        if self.rect.y > screen.get_height() * 2:
            platforms.remove(self)


    def checkCollision(self):
        if self.rect.colliderect(player.sprite.rect) and self.rect.bottom > player.sprite.rect.bottom and player.sprite.yVelo > 0:
            player.sprite.yVelo = 0
            while self.rect.colliderect(player.sprite.rect) and self.rect.bottom > player.sprite.rect.bottom and player.sprite.yVelo >= 0:
                for i in platforms.sprites():
                    i.rect.y += 1

    def update(self):
        self.checkCollision()

class MovingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, fill = (6,179,213), image = 'MovingPlatform.png', type = 'moving')

        self.velocity = choice([-5, 5])

    def move(self):
        self.rect.x += self.velocity

        if self.rect.left <= 0:
            self.velocity = 5

        if self.rect.right >= screen.get_width():
            self.velocity = -5

    def update(self):
        super().update()
        self.move()

class SpringPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, fill = (6,179,213), image = 'SpringPlatform.png', type = 'spring')

        self.image = pygame.transform.rotozoom(pygame.image.load('SpringPlatform.png').convert_alpha(), 0, 0.7)
        self.rect = self.image.get_rect(midbottom = (x, y))

screen = pygame.display.set_mode((600, 1200))

clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(Player())

platforms = pygame.sprite.Group()

platforms.add(Platform(screen.get_width() / 2, screen.get_height() * 0.9, width = screen.get_width(), height = screen.get_height() * 0.5, fill = 'darkgreen'))
for i in range(10):
    platforms.add(Platform(randint(0, screen.get_width()), randint(0, screen.get_height() * 0.8), i))

highestPlatformY = float('inf')
highestPlatform = None
for i in platforms.sprites():
    if i.rect.y < highestPlatformY:
        highestPlatformY = i.rect.y
        highestPlatform = i

createPlatform = pygame.USEREVENT + 1
pygame.time.set_timer(createPlatform, 1000)

while True:
    screen.fill((245,240,228))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == createPlatform:
            # print('create platfomr')
            # platforms.add(Platform(randint(0, screen.get_width()), 0))
            pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                os.execl(sys.executable, sys.executable, *sys.argv)


    player.update()

    if highestPlatform.rect.y > player.sprite.distanceTravelled // -200 + 50:
            newPlatform = choice(
                                [Platform(randint(0, screen.get_width()), 0) for _ in range(15)]
                                + [MovingPlatform(randint(0, screen.get_width()), 0) for _ in range(3)]
                                + [SpringPlatform(randint(0, screen.get_width()), 0) for _ in range(2)]
                                )
            platforms.add(newPlatform)
            highestPlatform = newPlatform

    for i in platforms.sprites():
        i.updateMovement()
    platforms.update()


    platforms.draw(screen)
    player.draw(screen)


    pygame.display.update()
    clock.tick(FPS)