import pygame, random, math
from settings import *
from mob_prototypes import *
from enemy_projectiles import *
from os import path


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
        #self.collision_dmg = self.radius * 2
        self.collision_dmg = self.radius
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
            #self.collision_dmg = self.radius * 2
            self.collision_dmg = self.radius * 2


class EnemyShip1(PrototypeEnemyShip):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.mtype = 'med'
        self.health = 10
        self.radius = 15
        super().__init__(game, game.enemyship1_img, movePattern, order, shots_allowed, 100)
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
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        self.rect.center = self.pos
        self.bullet_type = MobDefBullet
        self.fire_chance = 2
        self.enemyType = 'enemyShip1'

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def shoot(self, Bullet):
        super().shoot(Bullet)


class EnemySmuggler1(PrototypeEnemyFighter):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.angle = 270
        super().__init__(game, game.enemy_smuggler1_img, movePattern, order, shots_allowed, 100)
        self.speed = 12
        self.rot_speed = 8
        self.destination_list = []
        cowardice_chance = random.randrange(0, 101)
        if movePattern == 'topDown':
            spawn_x = random.randrange(320, WIDTH-320)
            self.moveFormation(spawn_x, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(random.randrange(spawn_x-192, spawn_x+192), 640),
                                ((random.randrange(32, WIDTH-32), HEIGHT + 100) if cowardice_chance < 76 else (random.choice([-100, WIDTH+100]), random.randrange(192, HEIGHT-640)))])
            self.shoot_when_aim_down = True
            self.speed = 12
        elif movePattern == 'topLeftDown_Rand':
            self.moveFormation(random.randrange(192, WIDTH/2-64), self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(random.randrange(WIDTH/2-480, WIDTH-192),752), ((random.randrange(WIDTH/2, WIDTH-192), 192) if cowardice_chance < 76 else (-100, random.randrange(192, HEIGHT-640))),
                                (random.randrange(WIDTH/2, WIDTH-192), 752), (random.randrange(320, WIDTH/2), 192), (random.randrange(32, WIDTH/2 - 32), HEIGHT + 100)])
            self.shoot_when_aim_down = True
        elif movePattern == 'topRightDown_Rand':
            self.moveFormation(random.randrange(WIDTH/2+64, WIDTH-192), self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(random.randrange(192, WIDTH/2+480),752), ((random.randrange(192, WIDTH/2), 192) if cowardice_chance < 76 else (WIDTH+100, random.randrange(192, HEIGHT-640))),
                                (random.randrange(192, WIDTH/2), 752), (random.randrange(WIDTH/2, WIDTH-320), 192), (random.randrange(WIDTH/2+32, WIDTH-32), HEIGHT + 100)])
            self.shoot_when_aim_down = True
        elif movePattern == 'topLeft_Dip':
            self.moveFormation(192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(192, 0), (192, 704), (1056, 320), (1056, 192), (928, 64), (800, 192), (928, 320),
                                (1056, 192), (928, 64), (800, 192), (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.slow_at_last_run = True
        elif movePattern == 'topRight_Dip':
            self.moveFormation(WIDTH - 192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 192, 0), (WIDTH - 192, 704), (WIDTH - 1056, 320), (WIDTH - 1056, 192),
                                (WIDTH - 928, 64), (WIDTH - 800, 192), (WIDTH - 928, 320),
                                (WIDTH - 1056, 192), (WIDTH - 928, 64), (WIDTH - 800, 192),
                                (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.slow_at_last_run = True
            self.shoot_when_aim_down = True
            self.shots_allowed = 20
            self.shoot_when_aim_down = True
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.dest_list_len = len(self.destination_list)
        self.pos = vec(self.rect.x, self.rect.y)
        self.rect.center = self.pos
        self.fire_chance = 5
        self.bullet_type = MobFighterWeakBullet
        self.enemyType = 'enemySmuggler1'

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def shoot(self, Bullet):
        super().shoot(Bullet)


class EnemySmuggler2(PrototypeCoordEnemy):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.radius = 30
        self.mtype = 'lg'
        self.health = 200
        self.order = (4 if order > 4 else order)
        self.angle = 270
        self.speed = 7
        self.rot = 0
        self.rot_speed = 8
        super().__init__(game, game.enemy_smuggler2_img, movePattern, self.order, shots_allowed, 300, False)
        self.destination_list = []
        if movePattern == 'topLeft_Down':
            self.moveFormation(96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(96, 744), (cruiser1_eight_squad_coords[3-order][0]+50, 704), (cruiser1_eight_squad_coords[3-order][0], 320)])
        elif movePattern == 'topRight_Down':
            self.moveFormation(WIDTH - 96, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 96, 744), (cruiser1_eight_squad_coords[order+4][0]-50, 704), (cruiser1_eight_squad_coords[order+4][0], 320)])
        elif movePattern == 'lowerLeft_Cruiser':
            self.moveSideFormation(self.lowerLeftSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(32, HEIGHT - 160), (1024, 160), (160, 96), cruiser1_eight_squad_coords[order+5]])
        elif movePattern == 'lowerRight_Cruiser':
            self.moveSideFormation(self.lowerRightSpawn_x, HEIGHT - 160, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 32, HEIGHT - 160), (WIDTH - 1024, 160), (WIDTH - 160, 96), cruiser1_eight_squad_coords[order]])
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.pos = vec(self.rect.x, self.rect.y)
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 3
        self.shot_delay = 1000
        self.firing_chance = 100
        self.projectile_type = MobAngledBullet
        self.side_speed = 1
        self.enemyType = 'enemySmuggler2'

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.game.mob_bullet_yellow_img, self.rect.centerx, self.rect.centery, 300, 15, 10)
        bullet = Bullet(self.game, self.game.mob_bullet_yellow_img, self.rect.centerx, self.rect.centery, 240, 15, 10)


class EnemyFighter1(PrototypeEnemyFighter):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.angle = 270
        super().__init__(game, game.enemyfighter1_img, movePattern, order, shots_allowed, 100)
        self.destination_list = []
        if movePattern == 'topLeft_Dip':
            self.moveFormation(192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(192, 0), (192, 704), (1056, 320), (1056, 192), (928, 64), (800, 192), (928, 320),
                                (1056, 192), (928, 64), (800, 192), (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.slow_at_last_run = True
        elif movePattern == 'topRight_Dip':
            self.moveFormation(WIDTH - 192, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH - 192, 0), (WIDTH - 192, 704), (WIDTH - 1056, 320), (WIDTH - 1056, 192),
                                (WIDTH - 928, 64), (WIDTH - 800, 192), (WIDTH - 928, 320),
                                (WIDTH - 1056, 192), (WIDTH - 928, 64), (WIDTH - 800, 192),
                                (random.randrange(0, WIDTH), HEIGHT + 50)])
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
            spawn_x = random.randrange(320, WIDTH / 2 - 64)
            self.moveFormation(spawn_x, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(spawn_x, 0), (random.randrange(WIDTH / 2, WIDTH - 320), 816),
                                (random.randrange(WIDTH / 2, WIDTH - 320), 192),
                                (random.randrange(0, WIDTH), HEIGHT + 50)])
            self.shots_allowed, self.rot_speed, self.speed = 20, 8, 11
            self.shoot_when_aim_down = True
        elif movePattern == 'topRightDown_Rand':
            spawn_x = random.randrange(WIDTH / 2 + 64, WIDTH - 320)
            self.moveFormation(spawn_x, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(spawn_x, 0), (random.randrange(320, WIDTH / 2), 816),
                                (random.randrange(320, WIDTH / 2), 192),
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
                               [(192 + 64, 0), (352 + 64, 544), (640 + 64, 768), (1056 + 64, 192), (928 + 64, 64),
                                (800 + 64, 192), (960 + 64, 544),
                                (1248 + 64, 768), (1664 + 64, 192), (1536 + 64, 64), (192 + 64, HEIGHT + 50)])
            self.shots_allowed = 20
            self.shoot_when_aim_down = True
        self.dest_index = 0
        self.destination = self.destination_list[self.dest_index]
        self.dest_list_len = len(self.destination_list)
        self.pos = vec(self.rect.x, self.rect.y)
        self.rect.center = self.pos
        self.enemyType = 'enemyFighter1'
        self.fire_chance = 5
        self.bullet_type = MobFighterBullet

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def shoot(self, Bullet):
        super().shoot(Bullet)


class EnemyBomber(PrototypeCoordEnemy):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.mtype = 'med'
        self.health = 30
        self.angle = 270
        self.radius = 16
        self.speed = 8
        self.rot = 0
        self.rot_speed = 8
        super().__init__(game, game.enemy_bomber_img, movePattern, order, shots_allowed, 200, False)
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
        self.rect.center = self.pos
        self.firing_chance = 2
        self.projectile_type = MobBomb
        self.side_speed = 2
        self.enemyType = 'enemyBomber'

    def update(self):
        super().update()

    def moveFormation(self, x, spawn_y_list, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, spawn_y_list, angle, speed, rot_speed, destinationList)

    def shoot(self, Bomb):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bomb(self.game, self.rect.centerx, self.rect.bottom)


class Kamikaze(PrototypeKamikaze):
    def __init__(self, game, movePattern, order):
        self.radius = 15
        self.mtype = 'med'
        self.health = 10
        self.angle = 270
        super().__init__(game, game.enemy_kamikaze_img, movePattern, order, 100, False)
        self.speed = 14
        self.rot = 0
        self.rot_speed = 15
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
        self.rect.center = self.pos
        self.homing_speed = 14
        self.enemyType = 'enemyKamikaze'

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def moveSideFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveSideFormation(x, y, angle, speed, rot_speed, destinationList)


class EnemyCruiser1(PrototypeCoordEnemy):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.radius = 70
        self.mtype = 'xxx_lg'
        self.health = 200
        self.order = (4 if order > 4 else order)
        self.angle = 270
        self.speed = 7
        self.rot = 0
        self.rot_speed = 8
        super().__init__(game, game.enemy_cruiser1_img, movePattern, self.order, shots_allowed, 300, True)
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
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 3
        self.shot_delay = 1000
        self.firing_chance = 5
        self.projectile_type = MobCruiser1Bullet
        self.side_speed = 1
        self.enemyType = 'enemyCruiser1'

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.rect.left+10, self.rect.centery, self, self.game.player)
        bullet = Bullet(self.game, self.rect.right-10, self.rect.centery, self, self.game.player)


class EnemySmugglerLieut(ProtoSmugglerLieut):
    def __init__(self, game, movePattern, order, shots_allowed):
        self.radius = 70
        self.mtype = 'xxx_lg'
        self.health = 200
        self.order = (4 if order > 4 else order)
        self.angle = 270
        self.speed = 7
        self.rot = 0
        self.rot_speed = 8
        super().__init__(game, game.enemy_cruiser1_img, movePattern, self.order, shots_allowed, 300, True)
        self.destination_list = []
        if movePattern == 'topDown_SLieut':
            self.moveFormation(WIDTH/2, self.top_spawn_y, self.angle, self.speed, self.rot_speed,
                               [(WIDTH/2, 256), (320, 256), (WIDTH-320, 256), (WIDTH/2, 256), (WIDTH/2, 928), (WIDTH/2, 256)])
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
        self.rect.center = self.pos
        self.collision_dmg = self.radius * 3
        self.shot_delay = 1000
        self.firing_chance = 5
        self.projectile_type = MobCruiser1Bullet
        self.side_speed = 1
        self.enemyType = 'enemySmugglerLieut'

    def update(self):
        super().update()

    def moveFormation(self, x, y, angle=270, speed=14, rot_speed=8, destinationList=[]):
        super().moveFormation(x, y, angle, speed, rot_speed, destinationList)

    def shoot(self, Bullet):
        #now = pygame.time.get_ticks()
        self.game.e1_shoot_sound.set_volume(0.3)
        self.game.e1_shoot_sound.play()
        #if now - self.last_shot > self.shoot_delay:
        #    self.last_shot = now
        bullet = Bullet(self.game, self.rect.left+10, self.rect.centery, self, self.game.player)
        bullet = Bullet(self.game, self.rect.right-10, self.rect.centery, self, self.game.player)
