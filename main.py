# Shoot 'Em Up Game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

import pygame, time, sys, random, game_conditions
from settings import *
from player import *
from mob import *
from pups_expls import *
from os import path


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_dir = path.join(game_folder, 'img')
        sfx_dir = path.join(game_folder, 'sfx')
        self.font_name = pygame.font.match_font('arial')
        self.load_sprites()
        self.load_sounds()
        self.load_background_data()


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player_shields = pygame.sprite.Group()

        self.player = Player(self)
        self.enemyType = 'enemyShip1'
        self.spawnEnemy(self.enemyType, 'down_DNA', False)
        # Score
        self.score = 0
        # Background music starts before the game loop starts. loops=-1 instructs pygame to replay/loop the music
        pygame.mixer.music.play(loops=-1)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # the update portion of the game loop
        if game_conditions.game_over:
            self.show_gameover_screen()
            game_conditions.game_over = False
            game_conditions.player_dead = False
            self.all_sprites = pygame.sprite.Group()
            self.mobs = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            self.powerups = pygame.sprite.Group()
            self.player = Player(self)
            #self.all_sprites.add(self.player)

            self.spawnEnemy(self.enemyType, 'down_DNA', False)
            # Score
            self.score = 0
        # keep loop running at the right speed
        #self.clock.tick(FPS)

        # Update
        self.all_sprites.update()

        # Check to see if a bullet hit a mob
        # True, True for killing mobs AND bullets when collision occurs
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True, pygame.sprite.collide_circle)
        for hit in hits:
            # cool discovery! so groupcollide returns a dictionary, where the key is a list of the collided sprite and
            # the value is a list of the colliding sprites. So to refer to every single COLLIDING sprite, need to
            # iterate through hits[hit]
            for bullet in hits[hit]:
                hit.health -= bullet.dmg
                self.explode(bullet.rect.center, 'tiny')
                impactSound = random.choice(self.expl_sounds)
                impactSound.set_volume(0.4)
                impactSound.play()
            if hit.health <= 0:
                hit.kill()
                # smaller meteors give more points
                self.score += hit.radius
                # explosion sounds; edit if meteors or enemies have health
                random.choice(self.expl_sounds).play()
                # spawning explosion
                if hit.mtype == 'lg':
                    self.explode(hit.rect.center, 'lg')
                elif hit.mtype == 'med':
                    self.explode(hit.rect.center, 'med')
                elif hit.mtype == 'sm':
                    self.explode(hit.rect.center, 'sm')
                # chance to drop power-ups. set to > 0.1 if want to test out with super high drop rate
                # > 0.88 seems to be just right
                if random.random() > 0.9:
                    pow = Pow(self, hit.rect.center)
                    #self.all_sprites.add(pow)
                    #self.powerups.add(pow)
                # spawning new enemy
                self.spawnEnemy(self.enemyType, 'down_DNA', True)

        # Check to see if a MISSILE hit a mob
        # True, True for killing mobs AND bullets when collision occurs
        hits = pygame.sprite.groupcollide(self.mobs, self.missiles, False, True, pygame.sprite.collide_circle)
        for hit in hits:
            # cool discovery! so groupcollide returns a dictionary, where the key is a list of the collided sprite and
            # the value is a list of the colliding sprites. So to refer to every single COLLIDING sprite, need to
            # iterate through hits[hit]
            for missile in hits[hit]:
                hit.health -= missile.dmg
                self.explode(missile.rect.center, 'sm')
                impactSound = random.choice(self.expl_sounds)
                impactSound.set_volume(0.5)
                impactSound.play()
            if hit.health <= 0:
                hit.kill()
                # smaller meteors give more points
                self.score += hit.radius
                # explosion sounds; edit if meteors or enemies have health
                random.choice(self.expl_sounds).play()
                # spawning explosion
                if hit.mtype == 'lg':
                    self.explode(hit.rect.center, 'lg')
                elif hit.mtype == 'med':
                    self.explode(hit.rect.center, 'med')
                elif hit.mtype == 'sm':
                    self.explode(hit.rect.center, 'sm')
                # chance to drop power-ups. set to > 0.1 if want to test out with super high drop rate
                # > 0.88 seems to be just right
                if random.random() > 0.9:
                    pow = Pow(self, hit.rect.center)
                    #self.all_sprites.add(pow)
                    #self.powerups.add(pow)
                # spawning new enemy
                self.spawnEnemy(self.enemyType, 'down_DNA', True)

        # Check to see if a mob hit the player
        # hits = a list of any mobs who hit the player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
            hit.kill()
            self.player.health -= hit.collision_dmg
            if hit.mtype == 'lg':
                self.explode(hit.rect.center, 'lg')
            elif hit.mtype == 'med':
                self.explode(hit.rect.center, 'med')
            elif hit.mtype == 'sm':
                self.explode(hit.rect.center, 'sm')
            impactSound = random.choice(self.expl_sounds)
            impactSound.set_volume(0.4)
            impactSound.play()
            # player_damage_sound.set_volume(0.3)
            # player_damage_sound.play()
            self.spawnEnemy(self.enemyType, 'down_DNA', True)
            if self.player.health <= 0:
                game_conditions.player_dead = True
                self.player_death_sound.play()
                self.death_explosion = Explosion(self, self.player.rect.center, 'player')
                #self.all_sprites.add(self.death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.health = 100

        # Check to see if player hit a power-up
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True, pygame.sprite.collide_circle)
        for hit in hits:
            if hit.type == 'health':
                self.player.health += random.randrange(10, 30)
                self.health_power_sound.play()
                if self.player.health >= 100:
                    self.player.health = 100
            if hit.type == 'gun_2shot':
                self.player.gun_2shot()
                self.gun_2shot_sound.play()
            if hit.type == 'gun_speed':
                self.player.gun_speed()
                self.gun_speed_sound.play()
            if hit.type == 'gun_power':
                self.player.gun_powerup()
                self.gun_power_sound.set_volume(0.6)
                self.gun_power_sound.play()
            if hit.type == 'shield':
                if not self.player.force_field:
                    p_shield = Shield(self, self.player)
                    #self.all_sprites.add(p_shield)
                    #self.player_shields.add(p_shield)
                self.shield_power_sound.play()
                self.player.shield()
            if hit.type == 'missile':
                self.player.missile_powerup()
                self.missile_pow_sound.play()
            if hit.type == 'h_missile':
                self.player.h_missile_powerup()
                self.h_missile_pow_sound.play()

        # reactivate the player's shield if shield down and fully regenerated
        if self.player.shield_health == 150 and not self.player.force_field:
            p_shield = Shield(self, self.player)
            #self.all_sprites.add(p_shield)
            #self.player_shields.add(p_shield)
            self.shield_power_sound.play()
            self.player.shield()

        # Check to see if mobs hit the player's shield
        hits = pygame.sprite.groupcollide(self.player_shields, self.mobs, False, True,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            for mob in hits[hit]:
                mob.kill()
                self.player.shield_health -= mob.collision_dmg
                if mob.mtype == 'lg':
                    self.explode(mob.rect.center, 'lg')
                elif mob.mtype == 'med':
                    self.explode(mob.rect.center, 'med')
                elif mob.mtype == 'sm':
                    self.explode(mob.rect.center, 'sm')
                impactSound = random.choice(self.expl_sounds)
                impactSound.set_volume(0.4)
                impactSound.play()
                # player_damage_sound.set_volume(0.3)
                # player_damage_sound.play()
                self.spawnEnemy(self.enemyType, 'down_DNA', True)
                if self.player.shield_health <= 0:
                    self.player.shield_health = 0
                    self.player.force_field = False
                    self.shield_down_sound.play()
                    hit.kill()
                    # self.all_sprites.add(death_explosion)

        # if the player died and the explosion has finished playing
        if self.player.lives == 0 and not self.death_explosion.alive():
            game_conditions.game_over = True

    def draw(self):
        # Draw / render
        # the set_caption code below displays the fps where the name of the applications should be.
        # good for checking performance
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # screen.fill is useful, but not necessary in this case, since we already have a background below
        self.screen.fill(BLACK)
        # blit = "copy the pixels of one thing unto another thing"
        # the screen.blit(background, background.rect) code below draws the background onto the screen
        # screen.blit(background, background_rect)
        self.scroll_background(self.screen, self.background, 2)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.score), 18, WIDTH / 2, 10)
        self.draw_health_bar(self.screen, 5, 5, self.player.health)
        self.draw_shield_bar(self.screen, 5, 15, self.player.shield_health)
        self.draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, self.player_mini_img)
        # for testing purposes, draw green dots on the map where the enemies' paths will go
        self.draw_dots_on_grid([(192, 1024), (768, HEIGHT - 192), (1024, HEIGHT - 224), (1088, HEIGHT - 320),
                                     (1024, HEIGHT - 416), (768, HEIGHT - 448), (608, HEIGHT - 576),
                                     (480, HEIGHT - 768), (416, HEIGHT - 928), (416, -HEIGHT - 50)])
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def load_sprites(self):
        # player sprites
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
        self.player_img = pygame.transform.scale(player_img, (75, 57))
        self.player_mini_img = pygame.transform.scale(player_img, (25, 19))
        # mob sprites
        enemy1_img = pygame.image.load(path.join(img_dir, "enemyRed1.png")).convert()
        self.enemy1_img = pygame.transform.scale(enemy1_img, (50, 38))
        self.meteor_images = []
        self.meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png',
                            'meteorBrown_med3.png',
                            'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
        self.meteor_dict = {}
        for img in self.meteor_list:
            meteor_img = pygame.image.load(path.join(img_dir, img)).convert()
            self.meteor_images.append(meteor_img)
            if img in ['meteorBrown_big1.png', 'meteorBrown_big2.png']:
                self.meteor_dict[meteor_img] = 'lg'
            elif img in ['meteorBrown_med1.png', 'meteorBrown_med3.png']:
                self.meteor_dict[meteor_img] = 'med'
            elif img in ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']:
                self.meteor_dict[meteor_img] = 'sm'
            else:
                self.meteor_dict[meteor_img] = 'med'
        # powerup sprites
        self.powerup_images = {}
        self.powerup_images['health'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
        self.powerup_images['gun_2shot'] = pygame.image.load(path.join(img_dir, 'things_gold.png')).convert()
        self.powerup_images['gun_speed'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
        self.powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'powerupBlue_shield.png')).convert()
        self.powerup_images['gun_power'] = pygame.image.load(path.join(img_dir, 'star_gold.png')).convert()
        missile_pow_img = pygame.image.load(path.join(img_dir, 'PowerUp3.png')).convert()
        self.powerup_images['missile'] = pygame.transform.scale(missile_pow_img, (48, 38))
        h_missile_pow_img = pygame.image.load(path.join(img_dir, 'PowerUp2.png')).convert()
        self.powerup_images['h_missile'] = pygame.transform.scale(h_missile_pow_img, (48, 38))
        # explosion sprites
        self.explosion_anim = {}
        self.explosion_anim['lg'] = []
        self.explosion_anim['med'] = []
        self.explosion_anim['sm'] = []
        self.explosion_anim['tiny'] = []
        self.explosion_anim['player'] = []
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (150, 150))
            self.explosion_anim['lg'].append(img_lg)
            img_med = pygame.transform.scale(img, (110, 110))
            self.explosion_anim['med'].append(img_med)
            img_sm = pygame.transform.scale(img, (80, 80))
            self.explosion_anim['sm'].append(img_sm)
            img_tiny = pygame.transform.scale(img, (50, 50))
            self.explosion_anim['tiny'].append(img_tiny)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.explosion_anim['player'].append(img)
        # projectile sprites
        bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
        self.bullet_img = pygame.transform.scale(bullet_img, (12, 80))
        powerbullet_img = pygame.image.load(path.join(img_dir, "laserGreen10.png")).convert()
        self.powerbullet_img = pygame.transform.scale(powerbullet_img, (12, 80))
        missile_img = pygame.image.load(path.join(img_dir, "spaceMissiles_001.png")).convert()
        self.missile_img = pygame.transform.scale(missile_img, (12, 60))
        shield_img = pygame.image.load(path.join(img_dir, 'shield_Edit.png'))
        self.shield_img = pygame.transform.scale(shield_img, (85, 85))


    def load_sounds(self):
        # Load all the game sounds
        # shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Laser_Shoot4.wav'))
        self.health_power_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow4.wav'))
        self.gun_2shot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow5.wav'))
        self.gun_speed_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Randomize5.wav'))
        self.gun_power_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Randomize6.wav'))
        self.shield_power_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow7.wav'))
        self.shield_down_sound = pygame.mixer.Sound(path.join(sfx_dir, 'shield_destroyed1.wav'))
        self.missile_pow_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow1.wav'))
        self.h_missile_pow_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow2.wav'))
        self.expl_sounds = []
        for sfx in ['Expl1.wav', 'Expl2.wav', 'Explosion1.wav', 'Explosion5.wav',
                    'Explosion11.wav']:
            self.expl_sounds.append(pygame.mixer.Sound(path.join(sfx_dir, sfx)))
        self.hit_hurt_sounds = []
        for sfx in ['Hurt.wav', 'Hurt1.wav', 'Hurt2.wav', 'Hurt3.wav']:
            self.hit_hurt_sounds.append(pygame.mixer.Sound(path.join(sfx_dir, sfx)))
        self.player_damage_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Damaged2.wav'))
        self.player_death_sound = pygame.mixer.Sound(path.join(sfx_dir, 'rumble1.ogg'))
        # pygame.mixer.music.load(path.join(sfx_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.load(path.join(sfx_dir, 'Battle in the Stars.ogg'))
        # lowers the volume of the BGM so that it's not overpowering.
        pygame.mixer.music.set_volume(0.4)
        # projectile sounds
        self.shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Laser_Shoot4.wav'))
        self.missile_shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'HKMISSLE.mp3'))


    def load_background_data(self):
        # background details
        self.background = pygame.image.load(path.join(img_dir, "starfield1.jpg")).convert()
        self.background_rect = self.background.get_rect()

        self.background_size = self.background.get_size()
        self.bg_w, self.bg_h = self.background_size
        self.bg_x, self.bg_y = 0, 0
        self.bg_x1, self.bg_y1 = 0, -self.bg_h
        self.bg_speedy = 0

    def scroll_background(self, surf, bg, speedy):
        speedy = speedy
        self.bg_y += speedy
        self.bg_y1 += speedy
        surf.blit(bg, (self.bg_x, self.bg_y))
        surf.blit(bg, (self.bg_x1, self.bg_y1))
        if self.bg_y > self.bg_h:
            self.bg_y = -self.bg_h
        if self.bg_y1 > self.bg_h:
            self.bg_y1 = -self.bg_h

    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        # the True below indicates whether the font is anti-aliased (edges smoothed) or not
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        # midtop is the position of the x, y of the font
        text_rect.midtop = (x, y)
        # so we want to blit the text onto the surface, which will usually be our screen.
        surf.blit(text_surface, text_rect)

    def spawnEnemy(self, enemyType, formation=None, respawn=False, number=1):
        if enemyType == 'meteor':
            if not respawn:
                for i in range(60):
                    m = Meteor(self)
            else:
                m = Meteor(self)
        elif enemyType == 'enemyShip1':
            if formation == 'down_DNA' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyShip1(self, 'topLeft_DNA', order)
                    m2 = EnemyShip1(self, 'topRight_DNA', order)
            elif formation == 'up_DNA' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyShip1(self, 'botLeft_DNA', order)
                    m2 = EnemyShip1(self, 'botRight_DNA', order)



    def explode(self, center, size):
        # spawning explosion
        expl = Explosion(self, center, size)
        #self.all_sprites.add(expl)

    def draw_grid(self):
        for x in range(0, WIDTH, GRIDSIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRIDSIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_dots_on_grid(self, coordList):
        for coord in coordList:
            image = pygame.Surface((3, 3))
            image.fill(GREEN)
            self.screen.blit(image, coord)

    def draw_health_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if (pct / 100) > 0.49:
            pygame.draw.rect(surf, GREEN, fill_rect)
        elif (pct / 100) > 0.19 and (pct / 100) <= 0.49:
            pygame.draw.rect(surf, YELLOW, fill_rect)
        elif (pct / 100) <= 0.19:
            pygame.draw.rect(surf, RED, fill_rect)
        # the 2 at the end is the pixel-thickness of the outline of the rectangle
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 150) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, BLUE, fill_rect)
        # the 2 at the end is the pixel-thickness of the outline of the rectangle
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def show_gameover_screen(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.screen, "GAME OVER", 50, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * (3 / 4))
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # we could use pygame.KEYDOWN, but pygame.KEYUP makes sure that the player has released the "any key"
                # before starting the game
                if event.type == pygame.KEYUP:
                    waiting = False


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
