import random
import pygame
from pygame import sprite
from src.Bonus import Bonus
from src.Field import Field
from src.blocks.Wall import Wall
from src.blocks.Steel import Steel
from src.tanks.Enemy import Enemy
from src.tanks.Player import Player
screenSize = width, height = 800, 650

steel1 = Steel(5 * 50, 12 * 50, 'br')
steel2 = Steel(5 * 50, 12 * 50, 'tr')
steel3 = Steel(5 * 50, 11 * 50, 'br')
steel4 = Steel(6 * 50, 11 * 50, 'br')
steel5 = Steel(6 * 50, 11 * 50, 'bl')
steel6 = Steel(7 * 50, 12 * 50, 'bl')
steel7 = Steel(7 * 50, 12 * 50, 'tl')
steel8 = Steel(7 * 50, 11 * 50, 'bl')


class Loop:
    def __init__(self):
        pass

    def loop(self, levelNo, playerModeInit):
        tankSprites = pygame.sprite.Group()
        playerGroup = pygame.sprite.Group()

        playerBullets = pygame.sprite.Group()
        enemyBullets = pygame.sprite.Group()

        lifeBonus = pygame.sprite.GroupSingle()
        boomBonus = pygame.sprite.GroupSingle()
        protectBonus = pygame.sprite.GroupSingle()
        starBonus = pygame.sprite.GroupSingle()

        hasShovel = False
        shovelTicks = 0

        bullets = []

        enemyCount = 10
        playerLife = 3

        pygame.init()
        screen = pygame.display.set_mode(screenSize)

        panel = pygame.sprite.Sprite()
        panel.image = pygame.transform.scale(
            pygame.image.load('src/sprites/panel.png'), (150, 650))
        panel.rect = panel.image.get_rect()
        panel.rect.x = 650
        panel.rect.y = 0

        f = Field(levelNo)
        f.panel.add(panel)
        fieldSprites = f.fieldSpriteGroup()
        decorate = f.trees
        iceSprites = f.ices

        player = Player(playerBullets, bullets, mode=playerModeInit)
        playerGroup.add(player)

        pygame.font.init()
        firstEnemy = Enemy(enemyBullets, bullets, 0, 0, playerGroup, '1')

        tankSprites.add(firstEnemy)
        enemies = []
        enemies.append(firstEnemy)

        ticks = 0
        enemieAlives = True
        exitgame = False

        while not exitgame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitgame = True

            for enemy in enemies:
                if not enemy.alive():
                    enemies.remove(enemy)

            for enemy in enemies:
                if pygame.sprite.spritecollideany(enemy, iceSprites):
                    enemy.speed = enemy.maxSpeed - 1
                else:
                    enemy.speed = enemy.maxSpeed

            for p in playerGroup:
                if pygame.sprite.spritecollideany(p, iceSprites):
                    p.speed = p.maxSpeed - 1
                else:
                    p.speed = p.maxSpeed

            if ticks >= 300:
                if len(enemies) < 4 and enemyCount > 0 and enemyCount - len(enemies) > 0:
                    newEnemy = Enemy(enemyBullets, bullets, (random.randint(
                        0, 12)) * 50 + 2, 40, playerGroup, random.randint(0, 3))
                    while pygame.sprite.spritecollideany(newEnemy, tankSprites) or pygame.sprite.spritecollideany(newEnemy, playerGroup) or pygame.sprite.spritecollideany(newEnemy, fieldSprites):
                        newEnemy = Enemy(enemyBullets, bullets, (random.randint(
                            0, 12)) * 50 + 2, 40, playerGroup, random.randint(0, 3))
                    enemies.append(newEnemy)
                    tankSprites.add(newEnemy)
                    ticks = 0
                else:
                    ticks = 300

            if hasShovel and shovelTicks >= 1000:
                shovelTicks = 0
                hasShovel = False
                f.steels.remove(steel1)
                f.steels.remove(steel2)
                f.steels.remove(steel3)
                f.steels.remove(steel4)
                f.steels.remove(steel5)
                f.steels.remove(steel6)
                f.steels.remove(steel7)
                f.steels.remove(steel8)
                f.walls.add(Wall(5 * 50, 12 * 50, 'br'))
                f.walls.add(Wall(5 * 50, 12 * 50, 'tr'))
                f.walls.add(Wall(5 * 50, 11 * 50, 'br'))
                f.walls.add(Wall(6 * 50, 11 * 50, 'br'))
                f.walls.add(Wall(6 * 50, 11 * 50, 'bl'))
                f.walls.add(Wall(7 * 50, 12 * 50, 'bl'))
                f.walls.add(Wall(7 * 50, 12 * 50, 'tl'))
                f.walls.add(Wall(7 * 50, 11 * 50, 'bl'))


            tankSprites.update()
            playerGroup.update()
            playerBullets.update()
            enemyBullets.update()
            screen.fill((0, 0, 0))

            tankFields = self.spriteGrouping(tankSprites, fieldSprites)
            playerFields = self.spriteGrouping(playerGroup, fieldSprites)
            for p in playerGroup:
                tmp = self.spriteGrouping(tankFields, playerGroup)
                tmp.remove(player)
                player.checkSprite(tmp)
            for enemy in enemies:
                if enemy.alive():
                    tmp = self.spriteGrouping(tankFields, playerFields)
                    tmp.remove(enemy)
                    enemy.checkSprite(tmp)

            iceSprites.draw(screen)
            fieldSprites.draw(screen)
            tankSprites.draw(screen)
            lifeBonus.draw(screen)
            boomBonus.draw(screen)
            protectBonus.draw(screen)
            starBonus.draw(screen)
            playerBullets.draw(screen)
            enemyBullets.draw(screen)
            playerGroup.draw(screen)
            decorate.draw(screen)
            font = pygame.font.SysFont('Comic Sans MS', 24, True)
            txtEnemyCount = font.render(
                'Enemies: ' + str(enemyCount), False, (255, 255, 255))
            txtLifeCount = font.render(
                'lifes: ' + str(playerLife), False, (255, 255, 255))
            screen.blit(txtEnemyCount, (655, 250))
            screen.blit(txtLifeCount, (655, 350))

            for p in playerGroup:
                if pygame.sprite.spritecollide(p, lifeBonus, True):
                    playerLife += 1
                if pygame.sprite.spritecollide(p, boomBonus, True):
                    for enemy in enemies:
                        if enemy.isAlive:
                            enemy.kill()
                            enemyCount -= 1
                    if enemyCount <= 0:
                        enemieAlives = False
                        return p.mode
                if pygame.sprite.spritecollide(p, protectBonus, True):
                    hasShovel = True
                    f.steels.add(steel1)
                    f.steels.add(steel2)
                    f.steels.add(steel3)
                    f.steels.add(steel4)
                    f.steels.add(steel5)
                    f.steels.add(steel6)
                    f.steels.add(steel7)
                    f.steels.add(steel8)


                if pygame.sprite.spritecollide(p, starBonus, True):
                    p.mode += 1
                    if p.mode > 1:
                       p.maxCooldown = 30
                    if p.mode > 3:
                        p.mode = 3

            if len(bullets) > 0:
                for bullet in bullets:
                    if not bullet.alive():
                        bullets.remove(bullet)

                for bullet in playerBullets:
                    for p in playerGroup:
                        if pygame.sprite.spritecollideany(bullet, f.steels) and p.mode == 3:
                            collided = pygame.sprite.spritecollide(
                                bullet, f.steels, True)
                            fieldSprites = f.fieldSpriteGroup()
                            bullet.kill()

                for bullet in bullets:
                    if pygame.sprite.spritecollideany(bullet, f.walls) \
                        or pygame.sprite.spritecollideany(bullet, f.steels) \
                            or pygame.sprite.spritecollideany(bullet, f.panel):
                        collided = pygame.sprite.spritecollide(
                            bullet, f.walls, True)
                        fieldSprites = f.fieldSpriteGroup()
                        bullet.kill()
                for bullet in bullets:
                    if pygame.sprite.spritecollideany(bullet, f.city):
                        pygame.sprite.spritecollide(bullet, f.city, True)
                        return 'lose'

                for bullet in bullets:
                    if pygame.sprite.spritecollideany(bullet, playerGroup):
                        collided = pygame.sprite.spritecollide(
                            bullet, playerGroup, False)
                        playerLife -= 1
                        if playerLife <= 0:
                            return 'lose'
                        else:
                            for i in collided:
                                i.respawn()
                            for tank in tankSprites:
                                tank.player = playerGroup
                        if playerLife != 3 and len(lifeBonus) == 0 and random.randint(0, 1) == 0:
                            life = Bonus(random.randint(
                                1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'life')
                            lifeBonus.add(life)
                        bullet.kill()

                for bullet in playerBullets:
                    if pygame.sprite.spritecollide(bullet, tankSprites, True):
                        if enemieAlives:
                            enemyCount -= 1
                        if enemyCount <= 0:
                            enemieAlives = False
                            for p in playerGroup:
                                return p.mode
                        bullet.kill()
                        if enemyCount > 0:
                            for enemy in enemies:
                                if not enemy.isAlive:
                                    newEnemy = Enemy(enemyBullets, bullets, (random.randint(
                                        0, 12)) * 50 + 2, 40, playerGroup, random.randint(0, 3))
                                    while pygame.sprite.spritecollideany(newEnemy, tankSprites) or pygame.sprite.spritecollideany(newEnemy, playerGroup) or pygame.sprite.spritecollideany(newEnemy, fieldSprites):
                                        newEnemy = Enemy(enemyBullets, bullets, (random.randint(
                                            0, 12)) * 50 + 2, 40, playerGroup, random.randint(0, 3))
                                    enemy = newEnemy
                                    tankSprites.add(enemy)
                        if random.randint(0, 10) == 0:
                            boom = Bonus(random.randint(
                                1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'boom')
                            boomBonus.add(boom)
                        if random.randint(0, 10) == 1:
                            protect = Bonus(random.randint(
                                1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'protect')
                            protectBonus.add(protect)
                        if random.randint(0, 10) == 2:
                            star = Bonus(random.randint(
                                1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'star')
                            starBonus.add(star)

                pygame.sprite.groupcollide(
                    enemyBullets, playerBullets, True, True)

            pygame.display.flip()
            pygame.time.wait(10)
            ticks += 1
            if hasShovel:
                shovelTicks += 1
        return 'exit'

    def spriteGrouping(self, tanks, fields):
        spriteGroup = pygame.sprite.Group()
        for tank in tanks:
            spriteGroup.add(tank)
        for field in fields:
            spriteGroup.add(field)
        return spriteGroup
