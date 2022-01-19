import pygame
from src.tanks.Tank import Tank
from src.tanks.Bullet import Bullet


class Player(Tank):
    def __init__(self, spriteGroup, bullets, mode=0):
        imageUp = pygame.transform.scale(
            pygame.image.load('src/sprites/green.gif'), (40, 40))
        super().__init__(spriteGroup, bullets, imageUp)
        self.bullet = Bullet(0, 0, 0)
        self.maxCooldown = 45
        self.mode = mode
        self.secondShooted = False
        if self.mode > 0:
            self.maxSpeed = 3
            self.maxCooldown = 30
        self.bullet.kill()

    def shoot(self):
        if (not self.bullet.alive() and self.cooldown <= self.maxCooldown - 15) or self.cooldown == 0:
            self.bullet = Bullet(
                self.rect.centerx, self.rect.top, self.direction)
            self.sprites.add(self.bullet)
            self.cooldown = self.maxCooldown
            self.bullets.append(self.bullet)

    def update(self):
        super().update()
        self.deltaX = 0
        self.deltaY = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.goLeft()
        elif key[pygame.K_d]:
            self.goRight()
        elif key[pygame.K_w]:
            self.goUp()
        elif key[pygame.K_s]:
            self.goDown()
        if key[pygame.K_j]:
            self.shoot()
        if self.mode > 1 and self.cooldown > 0 and self.cooldown < 25 and not self.secondShooted:
            self.bullet = Bullet(
                self.rect.centerx, self.rect.top, self.direction)
            self.sprites.add(self.bullet)
            self.cooldown = self.maxCooldown
            self.bullets.append(self.bullet)
            self.secondShooted = True
        if self.cooldown == 0:
            self.secondShooted = False
        self.checkSprite()
        self.setTankSprite()

    def respawn(self):
        self.__init__(self.sprites, self.bullets)

    def changeImage(self, imageName):
        self.imageUp = pygame.transform.scale(
            pygame.image.load('src/sprites/' + imageName), (40, 40))
        self.imageLeft = pygame.transform.rotate(self.imageUp, 90)
        self.imageRight = pygame.transform.rotate(self.imageUp, 270)
        self.imageDown = pygame.transform.rotate(self.imageUp, 180)
