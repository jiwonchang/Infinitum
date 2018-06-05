import pygame, math
from settings import *
from os import path

vec = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.dmg = 10
        self.game = game

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class DefaultBullet(Bullet):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is set to be (6, 50)
        self.image = pygame.transform.scale(game.bullet_img, (12, 80))
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -30
        self.dmg = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class PowerBullet(Bullet):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image = pygame.transform.scale(game.powerbullet_img, (12, 80))
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -30
        self.dmg = 15

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Missile(Bullet):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.missiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image = pygame.transform.scale(game.missile_img, (12, 60))
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        #self.old_centerx = self.rect.centerx
        self.inertia_time = 300
        self.slow_time = pygame.time.get_ticks()
        self.speedy = -30
        self.dmg = 30

    def update(self):
        if pygame.time.get_ticks() - self.slow_time <= self.inertia_time:
            self.rect.y += self.speedy * (1/3)
        else:
            self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class HomingMissile(Bullet):
    def __init__(self, game, x, y, target):
        self.groups = game.all_sprites, game.missiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        #self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = pygame.transform.scale(game.missile_img, (12, 60))
        self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        #self.rect.bottom = y
        #self.rect.centerx = x
        #for homing purposes, we define target and a rotation angle
        self.pos = vec(x, y)
        self.target = target
        self.rot = 0
        self.rot_speed = 10
        self.last_update = pygame.time.get_ticks()
        self.angle = 90
        #self.orig_angle = 0
        #self.dx = 0
        #elf.dy = 0
        #self.old_centerx = self.rect.centerx
        self.inertia_time = 300
        self.slow_time = pygame.time.get_ticks()
        self.speed = 15
        self.speedx = 0
        self.speedy = -20
        self.vel = vec(0, 0)
        self.accel = (0, 0)
        self.rect.center = self.pos
        self.dmg = 30
        # for homing purposes, according to Unity tutorial
        # self.directionVector = (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.x)
        # self.directionMagnitude = math.sqrt(((self.directionVector[0]) ** 2) + ((self.directionVector[1]) ** 2))
        # self.normalizedDirVec = (self.directionVector[0] / self.directionMagnitude,
        #                         self.directionVector[1] / self.directionMagnitude)
        # self.crossProduct = (self.normalizedDirVec[0] * self.speedy) - (self.normalizedDirVec[1] * self.speedx)
        # self.rotateAmount = self.crossProduct
        # self.angularVelocity = -self.rotateAmount * self.rot_speed

    """
    def rotate(self):
        now = pygame.time.get_ticks()
        # after 50 ticks since last update, rotate
        if now - self.last_update > 50:
            self.last_update = now
            self.directionVector = (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.x)
            self.directionMagnitude = math.sqrt(((self.directionVector[0]) ** 2) + ((self.directionVector[1]) ** 2))
            self.normalizedDirVec = (self.directionVector[0] / self.directionMagnitude, self.directionVector[1] / self.directionMagnitude)
            self.crossProduct = (self.normalizedDirVec[0] * self.speedy) - (self.normalizedDirVec[1] * self.speedx)
            self.rotateAmount = self.crossProduct
            self.angularVelocity = -self.rotateAmount * self.rot_speed
            self.rot = math.degrees(math.atan2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)) + 180
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    """

    def update(self):
        if pygame.time.get_ticks() - self.slow_time <= self.inertia_time:
            self.rect.y += self.speedy * (1/3)
            self.pos = (self.rect.centerx, self.rect.centery)
        else:
            if not self.target.alive():
                # if target is dead, then fly toward the direction it is facing
                new_image = pygame.transform.rotate(self.image_orig, -self.angle + 90)
                self.image = new_image
                self.rect = self.image.get_rect()
                curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
                self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
                self.pos -= self.vel
                self.rect.center = self.pos
            else:
                directionVector = self.target.pos - self.pos
                directionMagnitude = math.sqrt(((directionVector[0]) ** 2) + ((directionVector[1]) ** 2))
                if directionMagnitude > 0:
                    directionVector = (directionVector[0] / directionMagnitude,
                                         directionVector[1] / directionMagnitude)
                # get cross product between the direction vector (from the missile to target) and actual angle vector
                # (the direction in which the missile is actually / currently headed)
                #print(directionVector)
                curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
                #print(curDirVect)
                #print(self.angle)
                crossProduct = cross(directionVector, curDirVect)
                rotateAmount = crossProduct
                #print(crossProduct)
                # angular velocity
                self.rot = rotateAmount * self.rot_speed
                self.angle = (self.angle + self.rot) % 360
                new_image = pygame.transform.rotate(self.image_orig, -self.angle + 90)
                self.image = new_image
                self.rect = self.image.get_rect()

                # now, missile will head in direction it is currently facing with its speed
                curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
                #print(curDirVect)
                self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
                #print(self.vel)
                # we subtract vel here because our screen is flipped
                self.pos -= self.vel
                self.rect.center = self.pos


        #if pygame.time.get_ticks() - self.slow_time <= self.inertia_time:
        #    self.rect.y += self.speedy * (1/3)
        #else:
        #    self.rect.y += self.speedy

        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.centerx < -100\
                or self.rect.centerx > WIDTH + 100 or self.rect.centery > WIDTH + 100:
            self.kill()

"""
img_dir = path.join(path.dirname(__file__), 'img')
sfx_dir = path.join(path.dirname(__file__), 'sfx')

bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
powerbullet_img = pygame.image.load(path.join(img_dir, "laserGreen10.png")).convert()
missile_img = pygame.image.load(path.join(img_dir, "spaceMissiles_001.png")).convert()

shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Laser_Shoot4.wav'))
missile_shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'HKMISSLE.mp3'))
"""
