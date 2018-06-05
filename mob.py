import pygame, random, math
from settings import *
from os import path

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        self.health = 100

class Meteor(Mob):
    def __init__(self, game):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        randChoice = random.choice(game.meteor_images)
        self.image_orig = randChoice
        self.game = game
        self.mtype = game.meteor_dict[randChoice]
        # self.image_orig = pygame.transform.scale(meteor_img, ())
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image_orig, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        # for homing purposes, we make the position variable
        self.pos = vec(self.rect.centerx, self.rect.centery)
        # by default, speedy ranges from (1,8) and speedx ranges from (-3, 3)
        self.speedy = random.randrange(game.bg_speedy + 1, 11)
        self.speedx = random.randrange(-3, 3)
        # now, adding the rotation of meteor (take away if enemy is not a meteor
        self.rot = 0
        # rotation speed is, by default, between (-8, 8)
        #self.rot_speed = random.randrange(-8, 8)
        self.rot_speed = random.choice([i for i in range(-9, 9) if i != 0])
        # to make sure that meteor doesn't rotate for all 60 fps,
        # we get the ticks since the game started
        self.last_update = pygame.time.get_ticks()
        self.health = self.radius
        self.collision_dmg = self.radius * 2

    def rotate(self):
        now = pygame.time.get_ticks()
        # after 50 ticks since last update, rotate
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # we want to rotate the mob IF it is a meteor
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.pos = vec(self.rect.centerx, self.rect.centery)
        if self.rect.top > HEIGHT + 15 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            # change the meteor's properties when it respawn on top of map
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            #self.speedy = random.randrange(1, 8)
            #self.speedx = random.randrange(-3, 3)

            randChoice = random.choice(self.game.meteor_images)
            self.image_orig = randChoice
            self.mtype = self.game.meteor_dict[randChoice]
            # self.image_orig = pygame.transform.scale(meteor_img, ())
            self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * 0.85 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            # by default, speedy ranges from (1,8) and speedx ranges from (-3, 3)
            self.speedy = random.randrange(self.game.bg_speedy + 1, 11)
            self.speedx = random.randrange(-3, 3)
            # now, adding the rotation of meteor (take away if enemy is not a meteor
            self.rot = 0
            # rotation speed is, by default, between (-8, 8)
            # self.rot_speed = random.randrange(-8, 8)
            self.rot_speed = random.choice([i for i in range(-9, 9) if i != 0])
            # to make sure that meteor doesn't rotate for all 60 fps,
            # we get the ticks since the game started
            self.last_update = pygame.time.get_ticks()
            self.health = self.radius
            self.collision_dmg = self.radius * 2


class EnemyShip1(Mob):
    def __init__(self, game, movePattern, order):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = game.enemy1_img
        self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.mtype = 'med'
        self.health = 10
        self.movePattern = movePattern
        self.order = order
        self.angle = 270
        self.speed = 14
        # self.rect.bottom = y
        # self.rect.centerx = x
        # for homing purposes, we define target and a rotation angle
        self.destination_list = []
        if movePattern == 'topLeft_DNA':
            self.spawn_y_list = [-60, -160, -260, -360, -460]
            self.rect.x = 192
            self.rect.y = self.spawn_y_list[order]
            self.destination_list = [(192, 0), (768, 192), (1024, 224), (1088, 320), (1024, 416), (768, 448), (608, 576), (480, 768), (416, 928), (416, HEIGHT + 50)]
        elif movePattern == 'topRight_DNA':
            self.spawn_y_list = [-60, -160, -260, -360, -460]
            self.rect.x = WIDTH - 192
            self.rect.y = self.spawn_y_list[order]
            self.destination_list = [(WIDTH - 192, 0), (WIDTH - 768, 192), (WIDTH - 1024, 224), (WIDTH - 1088, 320), (WIDTH - 1024, 416), (WIDTH - 768, 448),
                                     (WIDTH - 608, 576), (WIDTH - 480, 768), (WIDTH - 416, 928), (WIDTH - 416, HEIGHT + 50)]
        elif movePattern == 'botLeft_DNA':
            self.angle = 90
            self.speed = 13
            self.spawn_y_list = [1084, 1184, 1284, 1384, 1484]
            self.rect.x = 192
            self.rect.y = self.spawn_y_list[order]
            self.destination_list = [(192, 1024), (768, HEIGHT - 192), (1024, HEIGHT - 224), (1088, HEIGHT - 320),
                                     (1024, HEIGHT - 416), (768, HEIGHT - 448), (608, HEIGHT - 576),
                                     (480, HEIGHT - 768), (416, HEIGHT - 928), (416, -HEIGHT - 50)]
        elif movePattern == 'botRight_DNA':
            self.angle = 90
            self.speed = 13
            self.spawn_y_list = [HEIGHT + 60, HEIGHT + 160, HEIGHT + 260, HEIGHT + 360, HEIGHT + 460]
            self.rect.x = WIDTH - 192
            self.rect.y = self.spawn_y_list[order]
            self.destination_list = [(WIDTH - 192, HEIGHT), (WIDTH - 768, HEIGHT - 192), (WIDTH - 1024, HEIGHT - 224),
                                     (WIDTH - 1088, HEIGHT - 320), (WIDTH - 1024, HEIGHT - 416),
                                     (WIDTH - 768, HEIGHT - 448), (WIDTH - 608, HEIGHT - 576),
                                     (WIDTH - 480, HEIGHT - 768), (WIDTH - 416, HEIGHT - 928),
                                     (WIDTH - 416, -HEIGHT - 50)]
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        self.rot = 0
        self.rot_speed = 8
        self.last_update = pygame.time.get_ticks()
        #self.slow_time = pygame.time.get_ticks()
        #self.speedx = 0
        #self.speedy = -20
        self.vel = vec(0, 0)
        #self.accel = (0, 0)
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 2

    def update(self):
        #if pygame.time.get_ticks() - self.slow_time <= self.inertia_time:
        #    self.rect.y += self.speedy * (1 / 3)
        #    self.pos = (self.rect.centerx, self.rect.centery)
        #else:
        #    if not self.target.alive():
        #        # if target is dead, then fly toward the direction it is facing
        #        new_image = pygame.transform.rotate(self.image_orig, -self.angle + 90)
        #        self.image = new_image
        #        self.rect = self.image.get_rect()
        #        curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
        #        self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
        #        self.pos -= self.vel
        #        self.rect.center = self.pos
        #print(self.dest_index)
        #print(self.destination_list)
        directionVector = self.destination - self.pos
        directionMagnitude = math.sqrt(((directionVector[0]) ** 2) + ((directionVector[1]) ** 2))
        if directionMagnitude > 0:
            directionVector = (directionVector[0] / directionMagnitude,
                               directionVector[1] / directionMagnitude)
        # get cross product between the direction vector (from the missile to target) and actual angle vector
        # (the direction in which the missile is actually / currently headed)
        # print(directionVector)
        curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
        # print(curDirVect)
        # print(self.angle)
        crossProduct = cross(directionVector, curDirVect)
        rotateAmount = crossProduct
        # print(crossProduct)
        # angular velocity
        self.rot = rotateAmount * self.rot_speed
        self.angle = (self.angle + self.rot) % 360
        new_image = pygame.transform.rotate(self.image_orig, -self.angle + 270)
        self.image = new_image
        self.rect = self.image.get_rect()

        # now, missile will head in direction it is currently facing with its speed
        curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
        # print(curDirVect)
        self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
        # print(self.vel)
        # we subtract vel here because our screen is flipped
        self.pos -= self.vel
        self.rect.center = self.pos
        if self.rect.collidepoint(self.destination) and self.alive():
            if self.dest_index < len(self.destination_list) - 1:
                self.dest_index += 1
                self.destination = self.destination_list[self.dest_index]
        if self.movePattern in ['topLeft_DNA', 'topRight_DNA'] and self.rect.top > HEIGHT + 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()
        elif self.movePattern in ['botLeft_DNA', 'botRight_DNA'] and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()



"""
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
meteor_dict = {}
for img in meteor_list:
    meteor_img = pygame.image.load(path.join(img_dir, img)).convert()
    meteor_images.append(meteor_img)
    if img in ['meteorBrown_big1.png', 'meteorBrown_big2.png']:
        meteor_dict[meteor_img] = 'lg'
    elif img in ['meteorBrown_med1.png', 'meteorBrown_med3.png']:
        meteor_dict[meteor_img] = 'med'
    elif img in ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']:
        meteor_dict[meteor_img] = 'sm'
    else:
        meteor_dict[meteor_img] = 'med'
"""