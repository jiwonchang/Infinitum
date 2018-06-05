import pygame, random
from settings import *

class Pow(pygame.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.type = random.choice(['health', 'gun_2shot', 'gun_speed', 'shield', 'gun_power', 'missile', 'h_missile'])
        self.image = game.powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        # may need to delete the below segments later when i replace the missile powerup sprite
        if self.type in ['missile', 'h_missile']:
            self.image.set_colorkey(WHITE)
        #####
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center, size):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = size
        self.image = game.explosion_anim[self.size][0]
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # larger frame rate = faster explosions. 50 or 75 seems pretty good
        self.frame_rate = 30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

"""
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['med'] = []
explosion_anim['sm'] = []
explosion_anim['tiny'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (150, 150))
    explosion_anim['lg'].append(img_lg)
    img_med = pygame.transform.scale(img, (110, 110))
    explosion_anim['med'].append(img_med)
    img_sm = pygame.transform.scale(img, (80, 80))
    explosion_anim['sm'].append(img_sm)
    img_tiny = pygame.transform.scale(img, (50, 50))
    explosion_anim['tiny'].append(img_tiny)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['health'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun_2shot'] = pygame.image.load(path.join(img_dir, 'things_gold.png')).convert()
powerup_images['gun_speed'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'powerupBlue_shield.png')).convert()
powerup_images['gun_power'] = pygame.image.load(path.join(img_dir, 'star_gold.png')).convert()
missile_pow_img = pygame.image.load(path.join(img_dir, 'PowerUp3.png')).convert()
powerup_images['missile'] = pygame.transform.scale(missile_pow_img, (48, 38))
h_missile_pow_img = pygame.image.load(path.join(img_dir, 'PowerUp2.png')).convert()
powerup_images['h_missile'] = pygame.transform.scale(missile_pow_img, (48, 38))
"""
