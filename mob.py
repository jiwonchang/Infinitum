import pygame, random, math
from settings import *
from enemy_projectiles import *
from os import path

class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self.health = 100
        self.shots_allowed = 1
        self.shots_fired = 0
        self.game = game


class Meteor(Mob):
    def __init__(self, game, is_gem_meteor=False):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.is_gem_meteor = is_gem_meteor
        if is_gem_meteor:
            randChoice = random.choice(game.gem_meteor_images)
            self.mtype = game.gem_meteor_dict[randChoice]
        else:
            randChoice = random.choice(game.meteor_images)
            self.mtype = game.meteor_dict[randChoice]
        self.image_orig = randChoice
        self.game = game
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
        self.speedy = random.randrange(game.background_scroll_speed + 1, 11)
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
        self.total_health = self.radius
        self.collision_dmg = self.radius * 2
        self.enemyType = 'meteor'

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

            is_gem_met_chance = random.randrange(0, 101)
            if is_gem_met_chance < 5:
                randChoice = random.choice(self.game.gem_meteor_images)
                self.mtype = self.game.gem_meteor_dict[randChoice]
                self.is_gem_meteor = True
            else:
                randChoice = random.choice(self.game.meteor_images)
                self.mtype = self.game.meteor_dict[randChoice]
                self.is_gem_meteor = False
            self.image_orig = randChoice
            # self.image_orig = pygame.transform.scale(meteor_img, ())
            self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * 0.85 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            # by default, speedy ranges from (1,8) and speedx ranges from (-3, 3)
            self.speedy = random.randrange(self.game.background_scroll_speed + 1, 11)
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
            self.total_health = self.radius
            self.collision_dmg = self.radius * 2


class EnemyShip1(Mob):
    def __init__(self, game, movePattern, order, shots_allowed):
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
        self.fireable_range = random.randrange(-300, 301)
        if movePattern in ['topLeft_DNA', 'topRight_DNA', 'topLeft_Zig', 'topRight_Zig']:
            self.despawn_location = 'down'
        elif movePattern in ['botLeft_DNA', 'botRight_DNA', 'botLeft_Zig', 'botRight_Zig']:
            self.despawn_location = 'up'
        self.top_spawn_y = [-60, -160, -260, -360, -460]
        self.bot_spawn_y = [1084, 1184, 1284, 1384, 1484]
        self.order = order
        self.angle = 270
        self.speed = 14
        self.rot = 0
        self.rot_speed = 8
        # self.rect.bottom = y
        # self.rect.centerx = x
        # for homing purposes, we define target and a rotation angle
        self.destination_list = []
        if movePattern == 'topLeft_DNA':
            self.moveFormation(192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(192, 0), (768, 192), (1024, 224), (1088, 320), (1024, 416), (768, 448), (608, 576),
                                (480, 768), (416, 928), (416, HEIGHT + 50)])
        elif movePattern == 'topRight_DNA':
            self.moveFormation(WIDTH - 192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 192, 0), (WIDTH - 768, 192), (WIDTH - 1024, 224), (WIDTH - 1088, 320),
                                (WIDTH - 1024, 416), (WIDTH - 768, 448),
                                (WIDTH - 608, 576), (WIDTH - 480, 768), (WIDTH - 416, 928), (WIDTH - 416, HEIGHT + 50)])
        elif movePattern == 'botLeft_DNA':
            self.moveFormation(192, self.bot_spawn_y, 90, 13, self.rot_speed,
                               [(192, 1024), (768, HEIGHT - 192), (1024, HEIGHT - 224), (1088, HEIGHT - 320),
                                (1024, HEIGHT - 416), (768, HEIGHT - 448), (608, HEIGHT - 576),
                                (480, HEIGHT - 768), (416, HEIGHT - 928), (416, -HEIGHT - 50)])
        elif movePattern == 'botRight_DNA':
            self.moveFormation(WIDTH - 192, self.bot_spawn_y, 90, 13, self.rot_speed,
                               [(WIDTH - 192, HEIGHT), (WIDTH - 768, HEIGHT - 192), (WIDTH - 1024, HEIGHT - 224),
                                (WIDTH - 1088, HEIGHT - 320), (WIDTH - 1024, HEIGHT - 416),
                                (WIDTH - 768, HEIGHT - 448), (WIDTH - 608, HEIGHT - 576),
                                (WIDTH - 480, HEIGHT - 768), (WIDTH - 416, HEIGHT - 928),
                                (WIDTH - 416, -HEIGHT - 50)])
        elif movePattern == 'topLeft_Zig':
            self.moveFormation(192, self.top_spawn_y, self.angle, 16, 50,
                               [(192, 32), (1472, 282), (384, 532), (1472, 782), (1472, HEIGHT + 100)])
        elif movePattern == 'topRight_Zig':
            self.moveFormation(WIDTH - 192, self.top_spawn_y, self.angle, 16, 50,
                               [(WIDTH - 192, 32), (WIDTH - 1472, 282), (WIDTH - 384, 532), (WIDTH - 1472, 782),
                                (WIDTH - 1472, HEIGHT + 100)])
        elif movePattern == 'botLeft_Zig':
            self.moveFormation(192, self.bot_spawn_y, 90, 16, 50,
                               [(192, HEIGHT - 32), (1472, HEIGHT - 282), (384, HEIGHT - 532), (1472, HEIGHT - 782),
                                (1472, -HEIGHT + 100)])
        elif movePattern == 'botRight_Zig':
            self.moveFormation(WIDTH - 192, self.bot_spawn_y, 90, 16, 50,
                               [(WIDTH - 192, HEIGHT - 32), (WIDTH - 1472, HEIGHT - 282), (WIDTH - 384, HEIGHT - 532),
                                (WIDTH - 1472, HEIGHT - 782), (WIDTH - 1472, -HEIGHT - 100)])
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        self.last_update = pygame.time.get_ticks()
        #self.slow_time = pygame.time.get_ticks()
        #self.speedx = 0
        #self.speedy = -20
        self.vel = vec(0, 0)
        #self.accel = (0, 0)
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 2
        self.shots_allowed = shots_allowed
        self.shots_fired = 0
        self.shot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.enemyType = 'enemyShip1'

    def update(self):
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
        if self.despawn_location == 'down' and self.rect.top > HEIGHT + 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()
        elif self.despawn_location == 'up' and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()

        if self.rect.y > 0 and self.rect.y < HEIGHT and self.shots_fired < self.shots_allowed \
                and pygame.time.get_ticks() - self.last_shot > self.shot_delay:
            shoot_chance = random.randrange(1, 101)
            if shoot_chance < 2:
                self.shoot(MobDefBullet)
                self.shots_fired += 1
                self.last_shot = pygame.time.get_ticks()

    def moveFormation(self, x, spawn_y_list, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = spawn_y_list[self.order]
        self.destination_list = destinationList

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.rect.centerx, self.rect.y, self, self.game.player)


class EnemyFighter(Mob):
    def __init__(self, game, movePattern, order):
        pass


class EnemyBomber(Mob):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = game.enemy_bomber_img
        self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 16
        self.mtype = 'med'
        self.health = 30
        self.movePattern = movePattern
        self.fireable_range = random.randrange(-300, 301)
        if movePattern in ['topLeft_Bomber', 'topRight_Bomber']:
            self.despawn_location = 'down'
        elif movePattern in ['botLeft_Bomber', 'botRight_Bomber']:
            self.despawn_location = 'up'
        elif movePattern in ['lowerLeft_Bomber', 'lowerRight_Bomber']:
            self.despawn_location = 'side'
        self.top_spawn_y = [-60, -260, -460, -660, -860]
        self.bot_spawn_y = [1084, 1184, 1284, 1384, 1484]
        self.lowerLeftSpawn_x = [-60, -160, -260, -360, -460]
        self.lowerRightSpawn_x = [WIDTH + 60, WIDTH + 160, WIDTH + 260, WIDTH + 360, WIDTH + 460]
        self.order = order
        self.angle = 270
        self.speed = 8
        self.rot = 0
        self.rot_speed = 8
        self.destination_list = []
        if movePattern == 'topLeft_Bomber':
            self.moveFormation(96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(96, 704), (ten_squad_coords[4-order][0]+48, 704), ten_squad_coords[4-order]])
        elif movePattern == 'topRight_Bomber':
            self.moveFormation(WIDTH - 96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 96, 704), (ten_squad_coords[order+5][0]-48, 704), ten_squad_coords[order+5]])
        elif movePattern == 'lowerLeft_Bomber':
            self.moveSideFormation(self.lowerLeftSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(32, HEIGHT - 160), (1024, 160), (160, 96), ten_squad_coords[order+5]])
        elif movePattern == 'lowerRight_Bomber':
            self.moveSideFormation(self.lowerRightSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 32, HEIGHT - 160), (WIDTH - 1024, 160), (WIDTH - 160, 96), ten_squad_coords[order]])
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        self.last_update = pygame.time.get_ticks()
        #self.slow_time = pygame.time.get_ticks()
        #self.speedx = 0
        #self.speedy = -20
        self.vel = vec(0, 0)
        #self.accel = (0, 0)
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 2
        self.shots_allowed = shots_allowed
        self.shots_fired = 0
        self.shot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.en_route_final_dest = False
        self.reached_final_destination = False
        self.went_right = 0
        self.went_left = 0
        self.reached_far_right, self.reached_far_left = False, True
        self.enemyType = 'enemyBomber'

    def update(self):
        if (self.en_route_final_dest and not self.reached_final_destination and not self.rect.collidepoint(self.final_destination))\
                or (self.shots_fired == self.shots_allowed):
            # print(self.vel)
            # we subtract vel here because our screen is flipped
            directionVector = vec(0,-1)
            directionMagnitude = math.sqrt(((directionVector[0]) ** 2) + ((directionVector[1]) ** 2))
            if directionMagnitude > 0:
                directionVector = (directionVector[0] / directionMagnitude,
                                   directionVector[1] / directionMagnitude)
            # get cross product between the direction vector (from the missile to target) and actual angle vector
            # (the direction in which the missile is actually / currently headed)
            # print(directionVector)
            curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
            crossProduct = cross(directionVector, curDirVect)
            rotateAmount = crossProduct
            # print(crossProduct)
            # angular velocity
            self.rot = rotateAmount * 20
            self.angle = (self.angle + self.rot) % 360
            new_image = pygame.transform.rotate(self.image_orig, -self.angle + 90)
            self.image = new_image
            self.rect = self.image.get_rect()
            self.pos -= self.vel
            self.rect.center = self.pos
            if self.rect.collidepoint(self.final_destination):
                self.reached_final_destination = True
        elif self.reached_final_destination and self.shots_fired < 100:
            self.rect.center = self.pos
            if self.rect.y > 0 and self.rect.y < HEIGHT and self.shots_fired < self.shots_allowed \
                    and pygame.time.get_ticks() - self.last_shot > self.shot_delay:
                shoot_chance = random.randrange(1, 101)
                if shoot_chance < 2:
                    self.shoot(MobBomb)
                    self.shots_fired += 1
                    self.last_shot = pygame.time.get_ticks()
            if not self.reached_far_right and self.reached_far_left:
                increment = 2
                self.pos = vec(self.rect.centerx+increment, self.rect.centery)
                self.rect.center = self.pos
                self.went_right += increment
                self.went_left -= increment
                if self.went_right >= 80:
                    self.reached_far_right = True
                    self.reached_far_left = False
            if not self.reached_far_left and self.reached_far_right:
                increment = -2
                self.pos = vec(self.rect.centerx + increment, self.rect.centery)
                self.rect.center = self.pos
                self.went_right += increment
                self.went_left -= increment
                if self.went_left >= 80:
                    self.reached_far_right = False
                    self.reached_far_left = True
        else:
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
            new_image = pygame.transform.rotate(self.image_orig, -self.angle + 90)
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
                dest_list_length = len(self.destination_list)
                if self.dest_index < dest_list_length - 1:
                    self.dest_index += 1
                    if self.dest_index == dest_list_length - 1:
                        self.en_route_final_dest = True
                        self.final_destination = self.destination_list[self.dest_index]
                        curDirVect = (float(math.cos(math.radians(90))), float(math.sin(math.radians(90))))
                        self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
                    self.destination = self.destination_list[self.dest_index]
        if self.despawn_location == 'down' and self.rect.top > HEIGHT + 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()
        elif self.despawn_location == 'up' and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()

    def moveFormation(self, x, spawn_y_list, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = spawn_y_list[self.order]
        self.destination_list = destinationList

    def shoot(self, Bomb):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bomb(self.game, self.rect.centerx, self.rect.bottom)


class Kamikaze(Mob):
    def __init__(self, game, movePattern, order):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = game.enemy_kamikaze_img
        self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.mtype = 'med'
        self.health = 10
        self.movePattern = movePattern
        if movePattern in ['topLeft_Kami', 'topRight_Kami']:
            self.despawn_location = 'down'
        elif movePattern in ['botLeft_Kami', 'botRight_Kami']:
            self.despawn_location = 'up'
        elif movePattern in ['lowerLeft_Kami', 'lowerRight_Kami']:
            self.despawn_location = 'side'
        self.top_spawn_y = [-60, -160, -260, -360, -460]
        self.bot_spawn_y = [1084, 1184, 1284, 1384, 1484]
        self.lowerLeftSpawn_x = [-60, -160, -260, -360, -460]
        self.lowerRightSpawn_x = [WIDTH + 60, WIDTH + 160, WIDTH + 260, WIDTH + 360, WIDTH + 460]
        self.order = order
        self.angle = 270
        self.speed = 14
        self.rot = 0
        self.rot_speed = 15
        # self.rect.bottom = y
        # self.rect.centerx = x
        # for homing purposes, we define target and a rotation angle
        self.destination_list = []
        if movePattern == 'topLeft_Kami':
            self.moveFormation(96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(96, 704), (1024, 64), game.player])
        elif movePattern == 'topRight_Kami':
            self.moveFormation(WIDTH - 96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 96, 704), (WIDTH - 1024, 64), game.player])
        elif movePattern == 'lowerLeft_Kami':
            self.moveSideFormation(self.lowerLeftSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(32, HEIGHT - 160), (1024, 160), (160, 96), game.player])
        elif movePattern == 'lowerRight_Kami':
            self.moveSideFormation(self.lowerRightSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 32, HEIGHT - 160), (WIDTH - 1024, 160), (WIDTH - 160, 96), game.player])
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        self.last_update = pygame.time.get_ticks()
        #self.slow_time = pygame.time.get_ticks()
        #self.speedx = 0
        #self.speedy = -20
        self.vel = vec(0, 0)
        #self.accel = (0, 0)
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 2

    def update(self):
        if self.destination == self.game.player:
            self.speed = 8
            directionVector = self.game.player.pos - self.pos
        else:
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
        if self.destination_list[self.dest_index] != self.game.player and self.rect.collidepoint(self.destination) and self.alive():
            if self.dest_index < len(self.destination_list) - 1:
                self.dest_index += 1
                self.destination = self.destination_list[self.dest_index]
        if self.despawn_location == 'down' and (self.rect.top > HEIGHT + 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100):
            self.kill()
        elif self.despawn_location == 'up' and (self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100):
            self.kill()
        elif self.despawn_location == 'side' and (self.rect.top < -HEIGHT - 60 \
                or self.rect.y > HEIGHT + 70):
            self.kill()

    def moveFormation(self, x, spawn_y_list, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = spawn_y_list[self.order]
        self.destination_list = destinationList

    def moveSideFormation(self, spawn_x_list, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = spawn_x_list[self.order]
        self.rect.y = y
        self.destination_list = destinationList

