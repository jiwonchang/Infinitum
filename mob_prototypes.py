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


class PrototypeEnemyShip(Mob):
    def __init__(self, game, img, movePattern, order, shots_allowed, spawn_distance=100):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = img
        self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        #self.radius = 15
        #self.mtype = 'med'
        #self.health = 10
        self.movePattern = movePattern
        self.formation = movePattern
        self.fireable_range = random.randrange(-300, 301)
        if movePattern[0:3] == 'top':
            self.despawn_location = 'down'
        elif movePattern[0:3] == 'bot':
            self.despawn_location = 'up'
        self.top_spawn_y = -60 - (spawn_distance * order)
        self.bot_spawn_y = 1084 + (spawn_distance * order)
        self.order = order
        self.angle = 270
        self.curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
        self.speed = 14
        self.rot = 0
        self.rot_speed = 8
        # self.rect.bottom = y
        # self.rect.centerx = x
        # for homing purposes, we define target and a rotation angle
        """
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
        elif movePattern == 'topLeft_Z':
            self.moveFormation(128, self.top_spawn_y, self.angle, self.speed, 100,
                               [(128, 160), (1728, 160), (128, 768), (1728, 768), (1728, HEIGHT + 50)])
        elif movePattern == 'topRight_Z':
            self.moveFormation(WIDTH - 128, self.top_spawn_y, self.angle, self.speed, 100,
                               [(WIDTH - 128, 160), (WIDTH - 1728, 160), (WIDTH - 128, 768), (WIDTH - 1728, 768), (WIDTH - 1728, HEIGHT + 50)])
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
        """
        self.last_update = pygame.time.get_ticks()
        self.vel = vec(0, 0)
        #self.rect.center = self.pos
        self.collision_dmg = self.radius * 2
        self.shots_allowed = shots_allowed
        self.shots_fired = 0
        self.shot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.bullet_type = MobDefBullet
        self.fire_chance = 2
        self.killed = False
        self.enemyType = 'enemyShip'

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
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()
        elif self.despawn_location == 'up' and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()

        if self.rect.y > 0 and self.rect.y < HEIGHT and self.shots_fired < self.shots_allowed \
                and pygame.time.get_ticks() - self.last_shot > self.shot_delay:
            shoot_chance = random.randrange(1, 101)
            if shoot_chance < self.fire_chance:
                self.shoot(self.bullet_type)
                self.shots_fired += 1
                self.last_shot = pygame.time.get_ticks()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.spawn_x = x
        self.rect.y = y
        self.spawn_y = y
        self.destination_list = destinationList

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, self, self.game.player)


class PrototypeEnemyFighter(Mob):
    def __init__(self, game, img, movePattern, order, shots_allowed, spawn_distance=100):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = img
        self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.mtype = 'med'
        self.health = 10
        self.movePattern = movePattern
        self.formation = movePattern
        self.fireable_range = random.randrange(-300, 301)
        self.slow_at_last_run = False
        self.shoot_when_aim_down = False
        self.shots_allowed = shots_allowed
        if movePattern[0:3] == 'top':
            self.despawn_location = 'down'
        elif movePattern[0:3] == 'bot':
            self.despawn_location = 'up'
        self.top_spawn_y = -60 - (spawn_distance * order)
        self.bot_spawn_y = 1084 + (spawn_distance * order)
        self.order = order
        #self.angle = 270
        self.curDirVect = (float(math.cos(math.radians(self.angle))), float(math.sin(math.radians(self.angle))))
        self.speed = 14
        self.rot = 0
        self.rot_speed = 8
        self.fire_chance = 5
        self.bullet_type = MobFighterBullet
        # self.rect.bottom = y
        # self.rect.centerx = x
        # for homing purposes, we define target and a rotation angle
        """
        self.destination_list = []
        if movePattern == 'topLeft_Dip':
            self.moveFormation(192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(192, 0), (192, 704), (1056, 320), (1056, 192), (928, 64), (800, 192), (928, 320),
                                (1056, 192), (928, 64), (800, 192), (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.slow_at_last_run = True
        elif movePattern == 'topRight_Dip':
            self.moveFormation(WIDTH - 192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 192, 0), (WIDTH - 192, 704), (WIDTH - 1056, 320), (WIDTH - 1056, 192), (WIDTH - 928, 64), (WIDTH - 800, 192), (WIDTH - 928, 320),
                                (WIDTH - 1056, 192), (WIDTH - 928, 64), (WIDTH - 800, 192), (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.slow_at_last_run = True
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
        elif movePattern == 'topLeftDown_Rand':
            spawn_x = random.randrange(320, WIDTH/2 - 64)
            self.moveFormation(spawn_x, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(spawn_x, 0), (random.randrange(WIDTH/2, WIDTH - 320), 816), (random.randrange(WIDTH/2, WIDTH-320), 192),
                                (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.shots_allowed, self.rot_speed, self.speed = 20, 8, 11
            self.shoot_when_aim_down = True
        elif movePattern == 'topRightDown_Rand':
            spawn_x = random.randrange(WIDTH/2 + 64, WIDTH - 320)
            self.moveFormation(spawn_x, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(spawn_x, 0), (random.randrange(320, WIDTH/2), 816), (random.randrange(320, WIDTH/2), 192),
                                (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.shots_allowed, self.rot_speed, self.speed = 20, 8, 11
            self.shoot_when_aim_down = True
        elif movePattern == 'topDown_0':
            self.moveFormation(192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(192, 0), (352, 544), (640, 768), (1056, 192), (928, 64), (800, 192), (960, 544),
                                (1248, 768), (1664, 192), (1536, 64), (192, HEIGHT + 50)])
            self.shots_allowed = 20
            self.shoot_when_aim_down = True
        elif movePattern == 'topDown_0_pair':
            self.moveFormation(192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(192+64, 0), (352+64, 544), (640+64, 768), (1056+64, 192), (928+64, 64), (800+64, 192), (960+64, 544),
                                (1248+64, 768), (1664+64, 192), (1536+64, 64), (192+64, HEIGHT + 50)])
            self.shots_allowed = 20
            self.shoot_when_aim_down = True
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.dest_list_len = len(self.destination_list)
        """
        self.to_final_dest = False
        #self.pos = vec(self.rect.x, self.rect.y)
        self.last_update = pygame.time.get_ticks()
        #self.slow_time = pygame.time.get_ticks()
        #self.speedx = 0
        #self.speedy = -20
        self.vel = vec(0, 0)
        #self.accel = (0, 0)
        #self.rect.center = self.pos
        self.collision_dmg = self.radius * 2
        self.shots_fired = 0
        self.shot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.killed = False
        self.enemyType = 'enemyFighter'

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
        self.curDirVect = curDirVect
        # print(curDirVect)
        self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
        # print(self.vel)
        # we subtract vel here because our screen is flipped
        self.pos -= self.vel
        self.rect.center = self.pos
        if self.rect.collidepoint(self.destination) and self.alive():
            if self.dest_index < self.dest_list_len - 1:
                self.dest_index += 1
                self.destination = self.destination_list[self.dest_index]
                if self.dest_index == self.dest_list_len - 2:
                    self.to_final_dest = True
                elif self.dest_index == self.dest_list_len - 1 and self.slow_at_last_run:
                    self.speed = 6
        if self.despawn_location == 'down' and self.rect.top > HEIGHT + 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()
        elif self.despawn_location == 'up' and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()

        if self.rect.y > 0 and self.rect.y < HEIGHT and (self.to_final_dest or self.shoot_when_aim_down) and self.shots_fired < self.shots_allowed \
                and pygame.time.get_ticks() - self.last_shot > self.shot_delay:
            if self.shoot_when_aim_down:
                if 180 < self.angle < 359:
                    shoot_chance = random.randrange(1, 101)
                    if shoot_chance < self.fire_chance:
                        self.shoot(self.bullet_type)
                        self.shots_fired += 1
                        self.last_shot = pygame.time.get_ticks()
            else:
                shoot_chance = random.randrange(1, 101)
                if shoot_chance < self.fire_chance:
                    self.shoot(self.bullet_type)
                    self.shots_fired += 1
                    self.last_shot = pygame.time.get_ticks()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.spawn_x = x
        self.rect.y = y
        self.spawn_y = y
        self.destination_list = destinationList

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, self)


# this enemy prototype will move and stay at a certain coordinate on the map
class PrototypeCoordEnemy(Mob):
    def __init__(self, game, img, movePattern, order, shots_allowed, spawn_distance=200, img_is_alpha=False):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = img
        if not img_is_alpha:
            self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        #self.radius = 16
        #self.mtype = 'med'
        #self.health = 30
        self.movePattern = movePattern
        self.formation = movePattern
        self.fireable_range = random.randrange(-300, 301)
        if movePattern[0:3] == 'top':
            self.despawn_location = 'down'
        elif movePattern[0:3] == 'bot':
            self.despawn_location = 'up'
        elif movePattern[0:5] in ['lower', 'upper']:
            self.despawn_location = 'side'
        self.top_spawn_y = -60 - (spawn_distance * order)
        self.bot_spawn_y = 1084 + (spawn_distance * order)
        self.lowerLeftSpawn_x = -60 - (spawn_distance * order)
        self.lowerRightSpawn_x = WIDTH + 60 + (spawn_distance * order)
        self.order = order
        #self.angle = 270
        #self.speed = 8
        #self.rot = 0
        #self.rot_speed = 8
        """
        self.destination_list = []
        if movePattern == 'topLeft_Bomber':
            self.moveFormation(96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(96, 704), (bomber_ten_squad_coords[4-order][0]+48, 704), bomber_ten_squad_coords[4-order]])
        elif movePattern == 'topRight_Bomber':
            self.moveFormation(WIDTH - 96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 96, 704), (bomber_ten_squad_coords[order+5][0]-48, 704), bomber_ten_squad_coords[order+5]])
        elif movePattern == 'lowerLeft_Bomber':
            self.moveSideFormation(self.lowerLeftSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(32, HEIGHT - 160), (1024, 160), (160, 96), bomber_ten_squad_coords[order+5]])
        elif movePattern == 'lowerRight_Bomber':
            self.moveSideFormation(self.lowerRightSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 32, HEIGHT - 160), (WIDTH - 1024, 160), (WIDTH - 160, 96), bomber_ten_squad_coords[order]])
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        """
        self.last_update = pygame.time.get_ticks()
        self.vel = vec(0, 0)
        #self.rect.center = self.pos
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
        self.firing_chance = 2
        self.projectile_type = MobBomb
        self.side_speed = 2
        self.killed = False
        self.enemyType = 'pro_coord_enemy'

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
                if shoot_chance < self.firing_chance:
                    self.shoot(self.projectile_type)
                    self.shots_fired += 1
                    self.last_shot = pygame.time.get_ticks()
            if not self.reached_far_right and self.reached_far_left:
                increment = self.side_speed
                self.pos = vec(self.rect.centerx+increment, self.rect.centery)
                self.rect.center = self.pos
                self.went_right += increment
                self.went_left -= increment
                if self.went_right >= 80:
                    self.reached_far_right = True
                    self.reached_far_left = False
            if not self.reached_far_left and self.reached_far_right:
                increment = -self.side_speed
                self.pos = vec(self.rect.centerx + increment, self.rect.centery)
                self.rect.center = self.pos
                self.went_right += increment
                self.went_left -= increment
                if self.went_left >= 80:
                    self.reached_far_right = False
                    self.reached_far_left = True
            if self.shots_fired >= self.shots_allowed:
                self.despawn_location = "all"
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
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()
        elif self.despawn_location == 'up' and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()
        elif self.despawn_location == 'all' and self.rect.top > HEIGHT + 60 or self.rect.top < -HEIGHT - 60 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.spawn_x = x
        self.rect.y = y
        self.spawn_y = y
        self.destination_list = destinationList

    def shoot(self, Projectile):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Projectile(self.game, self.rect.centerx, self.rect.bottom)


class PrototypeKamikaze(Mob):
    def __init__(self, game, img, movePattern, order, spawn_distance=100, img_is_alpha=False):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = img
        if not img_is_alpha:
            self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        #self.radius = 15
        #self.mtype = 'med'
        #self.health = 10
        self.movePattern = movePattern
        self.formation = movePattern
        if movePattern[0:3] == 'top':
            self.despawn_location = 'down'
        elif movePattern[0:3] == 'bot':
            self.despawn_location = 'up'
        elif movePattern[0:5] in ['lower', 'upper']:
            self.despawn_location = 'side'
        self.top_spawn_y = -60 - (spawn_distance * order)
        self.bot_spawn_y = 1084 + (spawn_distance * order)
        self.lowerLeftSpawn_x = -60 - (spawn_distance * order)
        self.lowerRightSpawn_x = WIDTH + 60 + (spawn_distance * order)
        self.order = order
        #self.angle = 270
        self.speed = 14
        self.rot = 0
        self.rot_speed = 15
        """
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
        """
        self.last_update = pygame.time.get_ticks()
        self.vel = vec(0, 0)
        #self.rect.center = self.pos
        self.collision_dmg = self.radius * 2
        self.homing_speed = 8
        self.killed = False
        self.enemyType = 'kamikaze'

    def update(self):
        if self.destination == self.game.player:
            self.speed = self.homing_speed
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
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()
        elif self.despawn_location == 'up' and (self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100):
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()
        elif self.despawn_location == 'side' and (self.rect.top < -HEIGHT - 60 \
                or self.rect.y > HEIGHT + 70):
            self.game.stage_respawn_list.append((self.enemyType, self.movePattern, False, self.order))
            self.kill()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.destination_list = destinationList

    def moveSideFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.destination_list = destinationList


class ProtoSmugglerLieut(Mob):
    def __init__(self, game, img, movePattern, order, shots_allowed, spawn_distance=200, img_is_alpha=False):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = img
        if not img_is_alpha:
            self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        #self.radius = 16
        #self.mtype = 'med'
        #self.health = 30
        self.movePattern = movePattern
        self.formation = movePattern
        self.fireable_range = random.randrange(-300, 301)
        if movePattern[0:3] == 'top':
            self.despawn_location = 'down'
        elif movePattern[0:3] == 'bot':
            self.despawn_location = 'up'
        elif movePattern[0:5] in ['lower', 'upper']:
            self.despawn_location = 'side'
        self.top_spawn_y = -120 - (spawn_distance * order)
        self.bot_spawn_y = 1084 + (spawn_distance * order)
        self.lowerLeftSpawn_x = -60 - (spawn_distance * order)
        self.lowerRightSpawn_x = WIDTH + 60 + (spawn_distance * order)
        self.order = order
        #self.angle = 270
        #self.speed = 8
        #self.rot = 0
        #self.rot_speed = 8
        """
        self.destination_list = []
        if movePattern == 'topLeft_Bomber':
            self.moveFormation(96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(96, 704), (bomber_ten_squad_coords[4-order][0]+48, 704), bomber_ten_squad_coords[4-order]])
        elif movePattern == 'topRight_Bomber':
            self.moveFormation(WIDTH - 96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 96, 704), (bomber_ten_squad_coords[order+5][0]-48, 704), bomber_ten_squad_coords[order+5]])
        elif movePattern == 'lowerLeft_Bomber':
            self.moveSideFormation(self.lowerLeftSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(32, HEIGHT - 160), (1024, 160), (160, 96), bomber_ten_squad_coords[order+5]])
        elif movePattern == 'lowerRight_Bomber':
            self.moveSideFormation(self.lowerRightSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 32, HEIGHT - 160), (WIDTH - 1024, 160), (WIDTH - 160, 96), bomber_ten_squad_coords[order]])
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        """
        self.last_update = pygame.time.get_ticks()
        self.vel = vec(0, 0)
        #self.rect.center = self.pos
        self.collision_dmg = self.radius * 2
        self.shots_allowed = shots_allowed
        self.shots_fired = 0
        self.shot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.reached_dialog_destination = False
        #self.en_route_final_dest = False
        #self.reached_final_destination = False
        #self.went_right = 0
        #self.went_left = 0
        #self.reached_far_right, self.reached_far_left = False, True
        self.firing_chance = 2
        self.projectile_type = MobSplitBullet
        self.side_speed = 2
        self.kiled = False
        self.enemyType = 'pro_smug_lieut_enemy'

    def update(self):
        if self.game.on_dialogue_stage and not self.reached_dialog_destination:
            if self.rect.centery < 160:
                self.pos = vec(self.rect.centerx, self.rect.centery + self.speed)
                self.rect.center = self.pos
            else:
                self.reached_dialog_destination = True
                self.despawn_location = 'all'
        elif not self.game.on_dialogue_stage and self.reached_dialog_destination:
            if self.rect.y > 0 and self.rect.y < HEIGHT and pygame.time.get_ticks() - self.last_shot > self.shot_delay:
                shoot_chance = random.randrange(1, 101)
                if shoot_chance < self.firing_chance:
                    self.shoot(self.projectile_type)
                    self.shots_fired += 1
                    self.last_shot = pygame.time.get_ticks()
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
                    self.destination = self.destination_list[self.dest_index]
                    if self.dest_index == dest_list_length - 1:
                        #self.en_route_final_dest = True
                        #self.final_destination = self.destination_list[self.dest_index]
                        #curDirVect = (float(math.cos(math.radians(90))), float(math.sin(math.radians(90))))
                        #self.vel = vec(curDirVect[0] * self.speed, curDirVect[1] * self.speed)
                        self.dest_index = 0
        if self.despawn_location == 'down' and self.rect.top > HEIGHT + 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()
        elif self.despawn_location == 'up' and self.rect.top < -HEIGHT - 60 \
                or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()
        elif self.despawn_location == 'all' and self.rect.top > HEIGHT + 60 or self.rect.top < -HEIGHT - 60 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.kill()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.destination_list = destinationList

    def shoot(self, Projectile):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Projectile(self.game, self.rect.centerx, self.rect.bottom)


# for future reference, here is the enemy cruiser class
"""
class EnemyCruiser1(Mob):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        # self.image = bullet_img
        # the bullet's size is originally set to be (6, 50)
        self.image_orig = game.enemy_cruiser1_img
        #self.image_orig.set_colorkey(BLACK)
        self.game = game
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 70
        self.mtype = 'xxx_lg'
        self.health = 200
        self.movePattern = movePattern
        self.fireable_range = random.randrange(-300, 301)
        if movePattern in ['topLeft_Cruiser', 'topRight_Cruiser']:
            self.despawn_location = 'down'
        elif movePattern in ['botLeft_Cruiser', 'botRight_Cruiser']:
            self.despawn_location = 'up'
        elif movePattern in ['lowerLeft_Cruiser', 'lowerRight_Cruiser']:
            self.despawn_location = 'side'
        self.top_spawn_y = -60 - (300 * order)
        self.bot_spawn_y = 1084 + (300 * order)
        self.lowerLeftSpawn_x = -60 - (300 * order)
        self.lowerRightSpawn_x = WIDTH + 60 + (300 * order)
        self.order = (4 if order > 4 else order)
        self.angle = 270
        self.speed = 7
        self.rot = 0
        self.rot_speed = 8
        self.destination_list = []
        if movePattern == 'topLeft_Cruiser':
            self.moveFormation(96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(96, 744), (cruiser1_eight_squad_coords[3-order][0]+120, 704), cruiser1_eight_squad_coords[3-order]])
        elif movePattern == 'topRight_Cruiser':
            self.moveFormation(WIDTH - 96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 96, 744), (cruiser1_eight_squad_coords[order+4][0]-120, 704), cruiser1_eight_squad_coords[order+4]])
        elif movePattern == 'lowerLeft_Cruiser':
            self.moveSideFormation(self.lowerLeftSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(32, HEIGHT - 160), (1024, 160), (160, 96), cruiser1_eight_squad_coords[order+5]])
        elif movePattern == 'lowerRight_Cruiser':
            self.moveSideFormation(self.lowerRightSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 32, HEIGHT - 160), (WIDTH - 1024, 160), (WIDTH - 160, 96), cruiser1_eight_squad_coords[order]])
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
        self.collision_dmg = self.radius * 3
        self.shots_allowed = shots_allowed
        self.shots_fired = 0
        self.shot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.en_route_final_dest = False
        self.reached_final_destination = False
        self.went_right = 0
        self.went_left = 0
        self.reached_far_right, self.reached_far_left = False, True
        self.enemyType = 'enemyCruiser1'

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
                if shoot_chance < 5:
                    self.shoot(MobCruiser1Bullet)
                    self.shots_fired += 1
                    self.last_shot = pygame.time.get_ticks()
            if not self.reached_far_right and self.reached_far_left:
                increment = 1
                self.pos = vec(self.rect.centerx+increment, self.rect.centery)
                self.rect.center = self.pos
                self.went_right += increment
                self.went_left -= increment
                if self.went_right >= 80:
                    self.reached_far_right = True
                    self.reached_far_left = False
            if not self.reached_far_left and self.reached_far_right:
                increment = -1
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

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        self.angle = angle
        self.rot_speed = rot_speed
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.destination_list = destinationList

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.rect.left+10, self.rect.centery, self, self.game.player)
        bullet = Bullet(self.game, self.rect.right-10, self.rect.centery, self, self.game.player)
"""
