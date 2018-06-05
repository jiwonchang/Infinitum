import pygame, random, game_conditions
from settings import *
from os import path
from projectiles import *
#from game import all_sprites, bullets


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # assigns the player's sprite and scales its size (by the tutorial, set at (50, 38))
        self.image = game.player_img
        # takes away the black box around the player sprite
        self.image.set_colorkey(BLACK)
        self.game = game
        self.rect = self.image.get_rect()
        self.radius = 22
        # use the below code to visualize the circle surrounding the player
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100
        # for homing purposes, we create the position variable
        self.pos = vec(self.rect.centerx, self.rect.centery)
        # time between auto-shots (less is faster shots)
        self.shoot_delay = 250
        self.missile_shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.missile_last_shot = pygame.time.get_ticks()
        # implementing multiple lives, and temporarily hiding player sprite while dead
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        # variables related to power-ups (gun power-ups, in this case). power = 1 means player shoots only 1 bullet.
        self.gun_2s = 1
        self.gun_2s_time = pygame.time.get_ticks()
        self.gun_spd = False
        self.gun_spd_time = pygame.time.get_ticks()
        self.gun_power = 1
        self.gun_power_time = pygame.time.get_ticks()
        self.force_field = False
        self.shield_health = 150
        self.shield_regen_time = pygame.time.get_ticks()
        self.missile_equip = 1
        self.missile_equip_time = pygame.time.get_ticks()
        #self.h_missile_equip = 1
        self.h_missile_equip = 1
        self.h_missile_equip_time = pygame.time.get_ticks()
        self.respawn_invul_time = pygame.time.get_ticks()

    def update(self):
        # timeout for gun 2-shot power up
        if self.gun_2s >= 2 and pygame.time.get_ticks() - self.gun_2s_time > POWERUP_TIME:
            self.gun_2s -= 1
            self.gun_2s_time = pygame.time.get_ticks()
        # timeout for gun speed power up
        if self.gun_spd and pygame.time.get_ticks() - self.gun_spd_time > POWERUP_TIME:
            self.shoot_delay = 250
            self.gun_spd = False
            self.gun_spd_time = pygame.time.get_ticks()
        # timeout for gun power up
        if self.gun_power >= 2 and pygame.time.get_ticks() - self.gun_power_time > POWERUP_TIME:
            self.gun_power -= 1
            self.gun_power_time = pygame.time.get_ticks()
        # timeout for missile power up
        if self.missile_equip >= 2 and pygame.time.get_ticks() - self.missile_equip_time > POWERUP_TIME:
            self.missile_equip -= 1
            self.missile_equip_time = pygame.time.get_ticks()
        # timeout for homing missile power up
        if self.h_missile_equip >= 2 and pygame.time.get_ticks() - self.h_missile_equip_time > POWERUP_TIME:
            self.h_missile_equip -= 1
            self.h_missile_equip_time = pygame.time.get_ticks()
        # shield slowly regenerates when down, or even slower, when still active.
        if not self.force_field and pygame.time.get_ticks() - self.shield_regen_time > SHIELD_REGEN_TIME:
            self.shield_health += 0.15
            if self.shield_health > 150:
                self.shield_health = 150
            self.shield_regen_time = pygame.time.get_ticks()
        elif self.force_field and pygame.time.get_ticks() - self.shield_regen_time > SHIELD_REGEN_TIME:
            self.shield_health += 0.07
            if self.shield_health > 150:
                self.shield_health = 150
            self.shield_regen_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.gun_2s = 1
            self.gun_spd = False
            self.shoot_delay = 250
            self.gun_power = 1
            self.hidden = False
            self.missile_equip = 1
            self.h_missile_equip = 1
            game_conditions.player_dead = False
            game_conditions.player_respawn_invinc = True
            self.respawn_invul_time = pygame.time.get_ticks()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        # after a time, respawn invulnerability wears off
        if game_conditions.player_respawn_invinc:
            if pygame.time.get_ticks() - self.respawn_invul_time > 2000:
                game_conditions.player_respawn_invinc = False
        # If arrow keys are pressed, move. Else, stay still.
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if not game_conditions.player_dead:
            self.move(keystate)
        if keystate[pygame.K_SPACE]:
            if not game_conditions.player_dead:
                if self.gun_power == 1:
                    self.shoot(DefaultBullet, self.game.all_sprites, self.game.bullets)
                elif self.gun_power > 1:
                    self.shoot(PowerBullet, self.game.all_sprites, self.game.bullets)
                if self.missile_equip > 1 and self.h_missile_equip == 1:
                    self.missile_shoot(Missile, self.game.all_sprites, self.game.missiles)
                elif self.h_missile_equip > 1:
                    self.h_missile_shoot(self.game.all_sprites, self.game.missiles)
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            # this if condition makes it possible to temporarily move the player off-map once player dies
            if not game_conditions.player_dead:
                self.rect.bottom = HEIGHT
        self.pos = vec(self.rect.centerx, self.rect.centery)

    def move(self, keystate):
        if keystate[pygame.K_UP]:
            self.speedy = -PLAYER_SPEED
        if keystate[pygame.K_DOWN]:
            self.speedy = PLAYER_SPEED
        if keystate[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
        if self.speedx != 0 and self.speedy != 0:
            self.speedx *= 0.7071
            self.speedy *= 0.7071

    def shoot(self, Bullet, all_sprites, bullets):
        now = pygame.time.get_ticks()
        self.game.shoot_sound.set_volume(0.6)
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.gun_2s == 1:
                bullet = Bullet(self.game, self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.game.shoot_sound.play()
            if self.gun_2s >= 2:
                bullet1 = Bullet(self.game, self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.game, self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                self.game.shoot_sound.play()

    def missile_shoot(self, Missile, all_sprites, missiles, target=None):
        now = pygame.time.get_ticks()
        self.game.missile_shoot_sound.set_volume(0.7)
        if now - self.missile_last_shot > self.missile_shoot_delay:
            self.missile_last_shot = now
            bullet1 = Missile(self.game, self.rect.left+20, self.rect.centery)
            bullet2 = Missile(self.game, self.rect.right-20, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            missiles.add(bullet1)
            missiles.add(bullet2)
            self.game.missile_shoot_sound.play()

    def h_missile_shoot(self, all_sprites, missiles):
        now = pygame.time.get_ticks()
        self.game.missile_shoot_sound.set_volume(0.7)
        if now - self.missile_last_shot > self.missile_shoot_delay:
            self.missile_last_shot = now
            mobsList = self.game.mobs.sprites()
            if not mobsList:
                target1 = None
                target2 = None
            else:
                target1 = random.choice(mobsList)
                target2 = random.choice(mobsList)
            #target1 = self
            #target2 = self
            if target1 is None:
                bullet1 = Missile(self.game, self.rect.left + 20, self.rect.centery)
            else:
                bullet1 = HomingMissile(self.game, self.rect.left + 20, self.rect.centery, target1)
            if target2 is None:
                bullet2 = Missile(self.game, self.rect.right - 20, self.rect.centery)
            else:
                bullet2 = HomingMissile(self.game, self.rect.right-20, self.rect.centery, target2)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            missiles.add(bullet1)
            missiles.add(bullet2)
            self.game.missile_shoot_sound.play()

    def gun_2shot(self):
        self.gun_2s += 1
        self.gun_2s_time = pygame.time.get_ticks()

    def gun_speed(self):
        self.gun_spd = True
        self.shoot_delay = 130
        self.gun_spd_time = pygame.time.get_ticks()

    def gun_powerup(self):
        self.gun_power += 1
        self.gun_power_time = pygame.time.get_ticks()

    def shield(self):
        if not self.force_field:
            self.force_field = True
            self.shield_health = 150
        else:
            self.shield_health += random.randrange(30, 50)
            if self.shield_health > 150:
                self.shield_health = 150

    def missile_powerup(self):
        self.missile_equip += 1
        self.missile_equip_time = pygame.time.get_ticks()

    def h_missile_powerup(self):
        self.h_missile_equip += 1
        self.h_missile_equip_time = pygame.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        # to hide, we simply take the sprite outside of the screen
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Shield(pygame.sprite.Sprite):
    def __init__(self, game, ship):
        self.groups = game.all_sprites, game.player_shields
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.shield_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 42.5
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.ship = ship
        self.rect.center = ship.rect.center

    def update(self):
        self.rect.center = self.ship.rect.center

#img_dir = path.join(path.dirname(__file__), 'img')
#sfx_dir = path.join(path.dirname(__file__), 'sfx')

#player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
#player_mini_img = pygame.transform.scale(player_img, (25, 19))
#player_mini_img.set_colorkey(BLACK)

#shield_img = pygame.image.load(path.join(img_dir, 'spr_shield.png'))
#shield_img = pygame.image.load(path.join(img_dir, 'shield_Edit.png'))
