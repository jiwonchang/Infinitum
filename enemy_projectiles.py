import pygame, math
from settings import *
from os import path

vec = pygame.math.Vector2

class MobBullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.dmg = 10
        self.game = game

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class MobDefBullet(MobBullet):
    def __init__(self, game, x, y, source=None, target=None):
        self.groups = game.all_sprites, game.enemy_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is set to be (6, 50)
        self.image = game.mob_bullet_img
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.speed = 8
        self.dmg = 10
        self.dirVector = (float(math.cos(math.radians(source.angle))), float(math.sin(math.radians(source.angle))))
        self.target = target
        if target != None:
            self.dirVector = target.pos - vec(x,y)
            directionMagnitude = math.sqrt(((self.dirVector[0]) ** 2) + ((self.dirVector[1]) ** 2))
            if directionMagnitude > 0:
                self.dirVector = vec(self.dirVector[0] / directionMagnitude, self.dirVector[1] / directionMagnitude)

    def update(self):
        self.vel = vec(self.dirVector[0] * self.speed, self.dirVector[1] * self.speed)
        # print(self.vel)
        # we subtract vel here because our screen is flipped
        self.pos += self.vel
        self.rect.center = self.pos
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.x < -20 or self.rect.x > WIDTH + 20:
            self.kill()


class MobFighterBullet(MobBullet):
    def __init__(self, game, x, y, source=None, target=None):
        self.groups = game.all_sprites, game.enemy_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is set to be (6, 50)
        self.image = game.enemy_fighter1_bullet_img
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.speed = 20
        self.dmg = 15
        #self.dirVector = (float(math.cos(math.radians(source.angle))), float(math.sin(math.radians(source.angle))))
        self.dirVector = source.curDirVect
        self.angle = source.angle
        #print(self.angle)
        self.image = pygame.transform.rotate(self.image, -self.angle + 270)
        self.target = target
        if target != None:
            self.dirVector = target.pos - vec(x,y)
            directionMagnitude = math.sqrt(((self.dirVector[0]) ** 2) + ((self.dirVector[1]) ** 2))
            if directionMagnitude > 0:
                self.dirVector = vec(self.dirVector[0] / directionMagnitude, self.dirVector[1] / directionMagnitude)

    def update(self):
        self.vel = vec(self.dirVector[0] * self.speed, self.dirVector[1] * self.speed)
        # print(self.vel)
        # we subtract vel here because our screen is flipped
        self.pos -= self.vel
        self.rect.center = self.pos
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.x < -20 or self.rect.x > WIDTH + 20:
            self.kill()

class MobFighterWeakBullet(MobFighterBullet):
    def __init__(self, game, x, y, source=None, target=None):
        super().__init__(game, x, y, source, target)
        self.speed = 15
        self.dmg = 8

    def update(self):
        super().update()

class MobBomb(MobBullet):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy_bombs
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is set to be (6, 50)
        self.image = pygame.transform.rotate(game.mob_bomb_img, 90)
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.health = 20
        self.dmg = 10
        self.inertia_time = 300
        self.slow_time = pygame.time.get_ticks()
        self.speedy = 7
        self.dmg = 30
        self.btype = 'x_lg'

    def update(self):
        if pygame.time.get_ticks() - self.slow_time <= self.inertia_time:
            self.rect.y += self.speedy * (1 / 3)
        else:
            self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class MobCruiser1Bullet(MobBullet):
    def __init__(self, game, x, y, source=None, target=None):
        self.groups = game.all_sprites, game.enemy_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is set to be (6, 50)
        self.image = game.enemy_cruiser1_bullet_img
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.angle = 90
        #self.speed = 8
        self.speed = 20
        self.dmg = 20
        self.dirVector = (float(math.cos(math.radians(source.angle))), float(math.sin(math.radians(source.angle))))
        self.target = target
        if target != None:
            self.dirVector = target.pos - vec(x,y)
            directionMagnitude = math.sqrt(((self.dirVector[0]) ** 2) + ((self.dirVector[1]) ** 2))
            if directionMagnitude > 0:
                self.dirVector = vec(self.dirVector[0] / directionMagnitude, self.dirVector[1] / directionMagnitude)
        curVec_angle = int(math.degrees(math.atan2(self.dirVector[1], self.dirVector[0])))
        self.angle = (self.angle + curVec_angle) % 360
        self.image = pygame.transform.rotate(self.image, -self.angle)


    def update(self):
        self.vel = vec(self.dirVector[0] * self.speed, self.dirVector[1] * self.speed)
        # print(self.vel)
        # we subtract vel here because our screen is flipped
        self.pos += self.vel
        self.rect.center = self.pos
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.x < -20 or self.rect.x > WIDTH + 20:
            self.kill()

class MobAngledBullet(MobBullet):
    def __init__(self, game, img, x, y, angle=0, bullet_dmg=10, bullet_speed=20, target=None):
        self.groups = game.all_sprites, game.enemy_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is set to be (6, 50)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.angle = 90
        #self.speed = 8
        self.speed = bullet_speed
        self.dmg = bullet_dmg
        self.dirVector = (float(math.cos(math.radians(-angle))), float(math.sin(math.radians(-angle))))
        self.target = target
        if target != None:
            self.dirVector = target.pos - vec(x,y)
            directionMagnitude = math.sqrt(((self.dirVector[0]) ** 2) + ((self.dirVector[1]) ** 2))
            if directionMagnitude > 0:
                self.dirVector = vec(self.dirVector[0] / directionMagnitude, self.dirVector[1] / directionMagnitude)
        curVec_angle = int(math.degrees(math.atan2(self.dirVector[1], self.dirVector[0])))
        self.angle = (self.angle + curVec_angle) % 360
        self.image = pygame.transform.rotate(self.image, -self.angle)


    def update(self):
        self.vel = vec(self.dirVector[0] * self.speed, self.dirVector[1] * self.speed)
        # print(self.vel)
        # we subtract vel here because our screen is flipped
        self.pos += self.vel
        self.rect.center = self.pos
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.x < -20 or self.rect.x > WIDTH + 20:
            self.kill()
