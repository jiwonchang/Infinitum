# Shoot 'Em Up Game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# space ship sprites by http://millionthvector.blogspot.com/, http://pixeljoint.com/p/887.htm, http://fractalsoftworks.com/forum/index.php?action=profile;u=2206;sa=showPosts
# space ship sprites by Skorpio

import pygame, time, sys, random, game_conditions
from settings import *
from player import *
from mob import *
from pups_expls import *
from stages import *
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
        #self.font_name = pygame.font.match_font('arial')
        self.font_name = path.join(font_dir, 'Scifi Adventure.otf')
        #self.font_name = path.join(font_dir, 'BITSUMIS.TTF')

        self.load_sprites()
        self.load_sounds()
        self.load_background_data()
        self.load_gui()

        # list of all stages, in order, so that we iterate through every time we accomplish mission
        self.stages = ['stage1']
        self.stage_index = 0

        self.money = 0
        self.inventory = {'Amethyst Ore': 0, 'Aquamarine Ore': 0, 'Bronze Ore': 0, 'Diamond Ore': 0, 'Emerald Ore': 0,
                          'Garnet Ore': 0, 'Gold Ore': 0, 'Sapphire Ore': 0, 'Silver Ore': 0, 'Steel Ore': 0,
                          'Titanium Ore': 0, 'Topaz Ore': 0, 'Amethyst': 0, 'Aquamarine': 0, 'Bronze': 0, 'Diamond': 0,
                          'Emerald': 0, 'Garnet': 0, 'Gold': 0, 'Sapphire': 0, 'Silver': 0, 'Steel': 0, 'Titanium': 0,
                          'Topaz': 0}

    """
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player_shields = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.damanging_explosions = pygame.sprite.Group()
        self.enemy_bombs = pygame.sprite.Group()

        self.player = Player(self)
        self.enemyType = 'enemyBomber'
        self.spawnEnemy('enemyShip1', 'down_DNA', False)
        self.spawnEnemy(self.enemyType, 'down_Bomber', False)
        #self.spawnEnemy(self.enemyType, 'down_Kami', False)
        # Score
        self.score = 0
        self.paused = False
        # Background music starts before the game loop starts. loops=-1 instructs pygame to replay/loop the music
        pygame.mixer.music.play(loops=-1)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused:
                self.update()
            self.draw()
    """

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
            self.enemy_bullets = pygame.sprite.Group()
            self.damanging_explosions = pygame.sprite.Group()
            self.enemy_bombs = pygame.sprite.Group()
            #self.all_sprites.add(self.player)

            #self.spawnEnemy(self.enemyType, 'down_DNA', False)
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
                #if random.random() > 0.9:
                #    pow = Pow(self, hit)
                pow = Pow(self, hit)
                # spawning new enemy
                self.spawnEnemy(hit.enemyType, hit.formation, True)

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
                #if random.random() > 0.9:
                #    pow = Pow(self, hit.rect.center)
                pow = Pow(self, hit)
                    #self.all_sprites.add(pow)
                    #self.powerups.add(pow)
                # spawning new enemy
                self.spawnEnemy(hit.enemyType, hit.formation, True)

        # Check to see if a bullet hit an enemy's bomb
        hits = pygame.sprite.groupcollide(self.enemy_bombs, self.bullets, False, True, pygame.sprite.collide_circle)
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
                # explosion sounds; edit if meteors or enemies have health
                random.choice(self.expl_sounds).play()
                # spawning explosion
                self.explode(hit.rect.center, 'x_lg')
                # chance to drop power-ups. set to > 0.1 if want to test out with super high drop rate
                # > 0.88 seems to be just right

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
            self.spawnEnemy(hit.enemyType, hit.formation, True)
            if self.player.health <= 0:
                game_conditions.player_dead = True
                self.player_death_sound.play()
                self.death_explosion = Explosion(self, self.player.rect.center, 'player')
                #self.all_sprites.add(self.death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.health = 100

        # Check to see if an enemy bullet hit the player
        # hits = a list of any enemy bullet that hit the player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, False, pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
            hit.kill()
            self.player.health -= hit.dmg
            self.explode(hit.rect.center, 'sm')
            impactSound = random.choice(self.expl_sounds)
            impactSound.set_volume(0.4)
            impactSound.play()
            # player_damage_sound.set_volume(0.3)
            # player_damage_sound.play()
            if self.player.health <= 0:
                game_conditions.player_dead = True
                self.player_death_sound.play()
                self.death_explosion = Explosion(self, self.player.rect.center, 'player')
                # self.all_sprites.add(self.death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.health = 100

        # Check to see if a an enemy bomb hit the player
        # hits = a list of any enemy bomb that have hit the player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bombs, False, pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
            hit.kill()
            if hit.btype == 'x_lg':
                self.damageExplode(hit.rect.center, 'x_lg')
            elif hit.btype == 'med':
                self.damageExplode(hit.rect.center, 'med')
            elif hit.btype == 'sm':
                self.damageExplode(hit.rect.center, 'sm')
            impactSound = random.choice(self.expl_sounds)
            #impactSound.set_volume(0.4)
            impactSound.play()
            # player_damage_sound.set_volume(0.3)
            # player_damage_sound.play()

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
                self.spawnEnemy(mob.enemyType, mob.formation, True)
                if self.player.shield_health <= 0:
                    self.player.shield_health = 0
                    self.player.force_field = False
                    self.shield_down_sound.play()
                    hit.kill()
                    # self.all_sprites.add(death_explosion)

        # Check to see if an enemy bullet hit the player's shield
        hits = pygame.sprite.groupcollide(self.player_shields, self.enemy_bullets, False, True,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            for enemy_bullet in hits[hit]:
                enemy_bullet.kill()
                self.player.shield_health -= enemy_bullet.dmg
                self.explode(enemy_bullet.rect.center, 'sm')
                impactSound = random.choice(self.expl_sounds)
                impactSound.set_volume(0.4)
                impactSound.play()
                # player_damage_sound.set_volume(0.3)
                # player_damage_sound.play()
                if self.player.shield_health <= 0:
                    self.player.shield_health = 0
                    self.player.force_field = False
                    self.shield_down_sound.play()
                    hit.kill()
                    # self.all_sprites.add(death_explosion)

        # Check to see if a damaging explosion hit the player
        # hits = a list of any damaging explosions that have hit the player
        hits = pygame.sprite.spritecollide(self.player, self.damanging_explosions, False, pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
            if (not self.player.force_field and not hit.damaged_p_shield) and not hit.damaged_player:
                # hit.kill()
                self.player.health -= hit.contact_dmg
                hit.damaged_player = True
                if self.player.health <= 0:
                    game_conditions.player_dead = True
                    self.player_death_sound.play()
                    self.death_explosion = Explosion(self, self.player.rect.center, 'player')
                    # self.all_sprites.add(self.death_explosion)
                    self.player.hide()
                    self.player.lives -= 1
                    self.player.health = 100

        # Check to see if a damaging explosion hit the player's shield
        hits = pygame.sprite.groupcollide(self.player_shields, self.damanging_explosions, False, False,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            for dmg_explosion in hits[hit]:
                if not dmg_explosion.damaged_p_shield:
                    self.player.shield_health -= dmg_explosion.contact_dmg
                    dmg_explosion.damaged_p_shield = True
                    if self.player.shield_health <= 0:
                        self.player.shield_health = 0
                        self.player.force_field = False
                        self.shield_down_sound.play()
                        hit.kill()
                        # self.all_sprites.add(death_explosion)

        # Check to see if a damaging explosion hit a mob
        # True, True for killing mobs AND damaging explosions when collision occurs
        hits = pygame.sprite.groupcollide(self.mobs, self.damanging_explosions, False, False, pygame.sprite.collide_circle)
        for hit in hits:
            # cool discovery! so groupcollide returns a dictionary, where the key is a list of the collided sprite and
            # the value is a list of the colliding sprites. So to refer to every single COLLIDING sprite, need to
            # iterate through hits[hit]
            for explosion in hits[hit]:
                if not explosion.damaged_mob:
                    hit.health -= explosion.contact_dmg
                    explosion.damaged_mob = True
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
                # spawning new enemy
                self.spawnEnemy(hit.enemyType, hit.formation, True)

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
        self.scroll_background(self.screen, self.background, self.background_scroll_speed)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.score), 18, WIDTH / 2, 10)
        self.draw_health_bar(self.screen, 5, 5, self.player.health, self.player.total_health, 100, 10)
        self.draw_shield_bar(self.screen, 5, 15, self.player.shield_health, self.player.shield_total_health)
        self.draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, self.player_mini_img)
        # for testing purposes, draw green dots on the map where the enemies' paths will go
        self.draw_dots_on_grid([(192, 32), (1472, 282), (384, 532), (1472, 782), (1472, HEIGHT + 100)])
        # when paused, draw the 'paused' text on screen
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text(self.screen, "Paused", 60, WIDTH / 2, HEIGHT / 2)
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
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def load_sprites(self):
        # player sprites
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
        self.player_img = pygame.transform.scale(player_img, (75, 57))
        self.player_mini_img = pygame.transform.scale(player_img, (25, 19))
        self.player_mini_img.set_colorkey(BLACK)
        # mob sprites
        enemy1_img = pygame.image.load(path.join(img_dir, "enemyRed1.png")).convert()
        self.enemy1_img = pygame.transform.scale(enemy1_img, (50, 38))
        enemy_kamikaze_img = pygame.image.load(path.join(img_dir, "enemyGreen5.png")).convert()
        self.enemy_kamikaze_img = pygame.transform.scale(enemy_kamikaze_img, (50, 38))
        self.enemy_bomber_img = pygame.image.load(path.join(img_dir, "heavyfreighter.png")).convert()
        #self.enemy_bomber_img = pygame.transform.scale(enemy_bomber_img, (50, 38))
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
        # gem meteor sprites
        self.gem_meteor_images = []
        self.gem_meteor_list = ['meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_med1.png',
                                'meteorGrey_med2.png',
                                'meteorGrey_small1.png', 'meteorGrey_small2.png', 'meteorGrey_tiny1.png']
        self.gem_meteor_dict = {}
        for img in self.gem_meteor_list:
            gem_meteor_img = pygame.image.load(path.join(img_dir, img)).convert()
            self.gem_meteor_images.append(gem_meteor_img)
            if img in ['meteorGrey_big1.png', 'meteorGrey_big2.png']:
                self.gem_meteor_dict[gem_meteor_img] = 'lg'
            elif img in ['meteorGrey_med1.png', 'meteorGrey_med2.png']:
                self.gem_meteor_dict[gem_meteor_img] = 'med'
            elif img in ['meteorGrey_small1.png', 'meteorGrey_small2.png', 'meteorGrey_tiny1.png']:
                self.gem_meteor_dict[gem_meteor_img] = 'sm'
            else:
                self.gem_meteor_dict[gem_meteor_img] = 'med'
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
        self.powerup_images['Amethyst Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Amethyst_Ore.png')).convert()
        self.powerup_images['Aquamarine Ore'] = pygame.image.load(path.join(img_dir, 'Etc_AquaMarine_Ore.png')).convert()
        self.powerup_images['Bronze Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Bronze_Ore.png')).convert()
        self.powerup_images['Diamond Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Diamond_Ore.png')).convert()
        self.powerup_images['Emerald Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Emerald_Ore.png')).convert()
        self.powerup_images['Garnet Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Garnet_Ore.png')).convert()
        self.powerup_images['Gold Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Gold_Ore.png')).convert()
        self.powerup_images['Sapphire Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Sapphire_Ore.png')).convert()
        self.powerup_images['Silver Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Silver_Ore.png')).convert()
        self.powerup_images['Steel Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Steel_Ore.png')).convert()
        self.powerup_images['Titanium Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Titanium_Ore.png')).convert()
        self.powerup_images['Topaz Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Topaz_Ore.png')).convert()
        # upgrade sprites
        self.upgrade_images = {}
        self.upgrade_images['gun_power_up'] = pygame.image.load(path.join(img_dir, 'SC2_vehicle_weapons_1.png')).convert()
        self.upgrade_images['gun_2shot_up'] = pygame.image.load(path.join(img_dir, 'SC2_ship_weapons_1.png')).convert()
        self.upgrade_images['gun_speed_up'] = pygame.image.load(path.join(img_dir, 'SC2_infantry_weapons_1.png')).convert()
        self.upgrade_images['shield_up'] = pygame.image.load(path.join(img_dir, 'SC2_shields_1.png')).convert()
        self.upgrade_images['ship_plating_up'] = pygame.image.load(path.join(img_dir, 'SC2_vehicle_plating_1.png')).convert()
        self.upgrade_images['missile_up'] = pygame.image.load(path.join(img_dir, 'SC2_missiles.jpg')).convert()
        self.upgrade_images['h_missile_up'] = pygame.image.load(path.join(img_dir, 'SC2_hisec_auto_tracking.png')).convert()
        self.upgrade_images['booster_up'] = pygame.image.load(path.join(img_dir, 'SC2_mag_field_launchers.png')).convert()
        # explosion sprites
        self.explosion_anim = {}
        self.explosion_anim['x_lg'] = []
        self.explosion_anim['lg'] = []
        self.explosion_anim['med'] = []
        self.explosion_anim['sm'] = []
        self.explosion_anim['tiny'] = []
        self.explosion_anim['player'] = []
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_x_lg = pygame.transform.scale(img, (200, 200))
            self.explosion_anim['x_lg'].append(img_x_lg)
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
        #bullet_img = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()
        self.bullet_img = pygame.transform.scale(bullet_img, (12, 80))
        powerbullet_img = pygame.image.load(path.join(img_dir, "laserGreen10.png")).convert()
        self.powerbullet_img = pygame.transform.scale(powerbullet_img, (12, 80))
        missile_img = pygame.image.load(path.join(img_dir, "spaceMissiles_001.png")).convert()
        self.missile_img = pygame.transform.scale(missile_img, (12, 60))
        shield_img = pygame.image.load(path.join(img_dir, 'shield_Edit.png'))
        self.shield_img = pygame.transform.scale(shield_img, (85, 85))
        mob_bullet_img = pygame.image.load(path.join(img_dir, "laserRed08.png")).convert()
        self.mob_bullet_img = pygame.transform.scale(mob_bullet_img, (25, 25))
        self.mob_bomb_img = pygame.image.load(path.join(img_dir, "spaceMissiles_006.png")).convert()
        # menu sprite
        cursor_img = pygame.image.load(path.join(img_dir, "cursor.png")).convert()
        self.cursor_img = pygame.transform.rotate(cursor_img, -135)
        self.cursor_img.set_colorkey(BLACK)

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

        # enemy projectile sounds
        self.e1_shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Laser_Shoot1.wav'))

    def load_background_data(self):
        # background details
        #self.background = pygame.image.load(path.join(img_dir, "starfield1.jpg")).convert()
        self.background = pygame.image.load(path.join(img_dir, "starfield2.jpg")).convert()
        self.background_rect = self.background.get_rect()

        self.background_size = self.background.get_size()
        self.bg_w, self.bg_h = self.background_size
        self.bg_x, self.bg_y = 0, 0
        self.bg_x1, self.bg_y1 = 0, -self.bg_h
        #self.bg_speedy = 0
        self.background_scroll_speed = 3

        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.obs_deck_img = pygame.image.load(path.join(img_dir, "obs_deck.jpg")).convert()
        self.obs_deck_rect = self.obs_deck_img.get_rect()

    def load_gui(self):
        self.gui_dial_box = pygame.image.load(path.join(img_dir, 'dialogue_sprite.png')).convert_alpha()
        #self.gui_dial_box = pygame.image.load(path.join(img_dir, 'futureui1.png')).convert()
        self.gui_dial_box.set_colorkey(WHITE)
        self.dial_box_rect = self.gui_dial_box.get_rect()

    def scroll_background(self, surf, bg, speedy):
        if not self.paused:
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
                for i in range(number):
                    gem_meteor_chance = random.randrange(0, 101)
                    if gem_meteor_chance < 5:
                        m = Meteor(self, True)
                        m.formation = 'w/e'
                    else:
                        m = Meteor(self, False)
                        m.formation = 'w/e'
            else:
                gem_meteor_chance = random.randrange(0, 101)
                if gem_meteor_chance < 5:
                    m = Meteor(self, True)
                    m.formation = 'w/e'
                else:
                    m = Meteor(self, False)
                    m.formation = 'w/e'
        elif enemyType == 'enemyShip1':
            if formation == 'down_DNA' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyShip1(self, 'topLeft_DNA', order, 2)
                    m2 = EnemyShip1(self, 'topRight_DNA', order, 2)
                    m1.formation = 'topLeft_DNA'
                    m2.formation = 'topRight_DNA'
            elif formation == 'up_DNA' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyShip1(self, 'botLeft_DNA', order, 2)
                    m2 = EnemyShip1(self, 'botRight_DNA', order, 2)
                    m1.formation = 'botLeft_DNA'
                    m2.formation = 'botRight_DNA'
            elif formation == 'down_Zig' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyShip1(self, 'topLeft_Zig', order, 2)
                    m2 = EnemyShip1(self, 'topRight_Zig', order, 2)
                    m1.formation = 'topLeft_Zig'
                    m2.formation = 'topRight_Zig'
            elif formation == 'up_Zig' and not respawn:
                for order in range(0,5):
                    m1 = EnemyShip1(self, 'botLeft_Zig', order, 2)
                    m2 = EnemyShip1(self, 'botRight_Zig', order, 2)
                    m1.formation = 'botLeft_Zig'
                    m2.formation = 'botRight_Zig'
        elif enemyType == 'kamikaze':
            if formation == 'down_Kami' and not respawn:
                for order in range(0, 3):
                    m1 = Kamikaze(self, 'topLeft_Kami', order)
                    m2 = Kamikaze(self, 'topRight_Kami', order)
                    m1.formation = 'topLeft_Kami'
                    m2.formation = 'topRight_Kami'
            if formation == 'lowerDiag_Kami' and not respawn:
                for order in range(0, 3):
                    m1 = Kamikaze(self, 'lowerLeft_Kami', order)
                    m2 = Kamikaze(self, 'lowerRight_Kami', order)
                    m1.formation = 'lowerLeft_Kami'
                    m2.formation = 'lowerRight_Kami'
        elif enemyType == 'enemyBomber':
            if formation == 'down_Bomber' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyBomber(self, 'topLeft_Bomber', order, 5)
                    m2 = EnemyBomber(self, 'topRight_Bomber', order, 5)
                    m1.formation = 'topLeft_Bomber'
                    m2.formation = 'topRight_Bomber'
            if formation == 'lowerDiag_Bomber' and not respawn:
                for order in range(0, 5):
                    m1 = EnemyBomber(self, 'lowerLeft_Bomber', order, 5)
                    m2 = EnemyBomber(self, 'lowerRight_Bomber', order, 5)
                    m1.formation = 'lowerLeft_Bomber'
                    m2.formation = 'lowerRight_Bomber'

    def explode(self, center, size):
        # spawning explosion
        expl = Explosion(self, center, size)

    def damageExplode(self, center, size):
        expl = DamagingExplosion(self, center, size)

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

    def draw_health_bar(self, surf, x, y, pct, total_health, BAR_LENGTH, BAR_HEIGHT):
        if pct < 0:
            pct = 0
        #BAR_LENGTH = 100
        #BAR_HEIGHT = 10
        fill = (pct / total_health) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if (pct / total_health) > 0.49:
            pygame.draw.rect(surf, GREEN, fill_rect)
        elif (pct / total_health) > 0.19 and (pct / total_health) <= 0.49:
            pygame.draw.rect(surf, YELLOW, fill_rect)
        elif (pct / total_health) <= 0.19:
            pygame.draw.rect(surf, RED, fill_rect)
        # the 2 at the end is the pixel-thickness of the outline of the rectangle
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_shield_bar(self, surf, x, y, pct, total_health):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / total_health) * BAR_LENGTH
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

    def show_start_screen(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.screen, "Infinitum", 100, WIDTH / 2, HEIGHT * (2.5/10))
        self.draw_text(self.screen, "New Game", 30, WIDTH / 2, HEIGHT * (5/10))
        self.draw_text(self.screen, "Load Game", 30, WIDTH / 2, HEIGHT * (6/10))
        self.draw_text(self.screen, "Controls", 30, WIDTH / 2, HEIGHT * (7/10))
        self.draw_text(self.screen, "Press Enter to select", 20, WIDTH / 2, HEIGHT * (9 / 10))
        options_cursor_coords = [((WIDTH / 2) - 220, HEIGHT / 2 - 5), ((WIDTH / 2) - 240, HEIGHT * (6/10) - 5),
                                 ((WIDTH / 2) - 230, HEIGHT * (7/10) - 5)]
        #self.wait_for_key()
        choice = self.navigate_menu([0, 1, 2], options_cursor_coords)
        if choice == 0:
            self.begin_new_game()
        elif choice == 1:
            self.load_game()
        elif choice == 2:
            self.show_controls()
        #return choice

    def show_gameover_screen(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.screen, "GAME OVER", 70, WIDTH / 2, HEIGHT * (2.5 / 10))
        self.draw_text(self.screen, "Continue", 30, WIDTH / 2, HEIGHT * (5/10))
        self.draw_text(self.screen, "Exit to Menu", 30, WIDTH / 2, HEIGHT * (6/10))
        self.draw_text(self.screen, "Exit Game", 30, WIDTH / 2, HEIGHT * (7/10))
        self.draw_text(self.screen, "Press Enter to select", 20, WIDTH / 2, HEIGHT * (9 / 10))
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                # we could use pygame.KEYDOWN, but pygame.KEYUP makes sure that the player has released the "any key"
                # before starting the game
                if event.type == pygame.KEYUP:
                    waiting = False

    def navigate_menu(self, optionsList, optCurCoords):
        pygame.event.wait()
        index = 0
        old_index = 0
        chosen = False
        lenOpts = len(optionsList)
        self.screen.blit(self.cursor_img, optCurCoords[index])
        while not chosen:
            self.clock.tick(FPS)
            #self.screen.blit(self.cursor_img, optCurCoords[index])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_DOWN]:
                        index += 1
                        if index == lenOpts:
                            index = 0
                        # redraws the background where the cursor used to be, giving the appearance of the cursor moving
                        self.screen.blit(self.background, optCurCoords[old_index], pygame.Rect(optCurCoords[old_index][0], optCurCoords[old_index][1], 60, 60))
                        old_index += 1
                        if old_index == lenOpts:
                            old_index = 0
                    elif keystate[pygame.K_UP]:
                        index -= 1
                        if index < 0:
                            index = lenOpts - 1
                        self.screen.blit(self.background, optCurCoords[old_index],
                                         pygame.Rect(optCurCoords[old_index][0], optCurCoords[old_index][1], 60, 60))
                        old_index -= 1
                        if old_index < 0:
                            old_index = lenOpts - 1
                    elif keystate[pygame.K_RETURN] or keystate[pygame.K_SPACE]:
                        chosen = True
                        return optionsList[index]
            self.screen.blit(self.cursor_img, optCurCoords[index])
            pygame.display.flip()

    def load_game(self):
        pass

    def show_controls(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.screen, "Controls", 60, WIDTH / 2, HEIGHT * (1 / 10))
        self.draw_text(self.screen, "Press Space to Shoot", 30, WIDTH / 2, HEIGHT * (5/10))
        #self.draw_text(self.screen, "Exit to Menu", 50, WIDTH / 2, HEIGHT * (6/10))
        #self.draw_text(self.screen, "Exit Game", 50, WIDTH / 2, HEIGHT * (7/10))
        #self.draw_text(self.screen, "Press Enter to select", 30, WIDTH / 2, HEIGHT * (9 / 10))
        pygame.display.flip()
        self.wait_for_key()

    def begin_new_game(self):
        # this function will contain a scene
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.screen, "Beginning new game!", 60, WIDTH / 2, HEIGHT * (1 / 10))
        self.initialize()
        self.player = Player(self)

        self.ship_deck_menu()
        #pygame.display.flip()

    def ship_deck_menu(self):
        self.screen.blit(self.obs_deck_img, (self.obs_deck_rect[0]-40, self.obs_deck_rect[1]))
        gui_dial_box = pygame.transform.scale(self.gui_dial_box, (300, 114))
        self.screen.blit(gui_dial_box, (260, 260))
        self.screen.blit(gui_dial_box, (260, 404))
        self.screen.blit(gui_dial_box, (1270, 260))
        self.screen.blit(gui_dial_box, (1270, 404))

        self.draw_text(self.screen, "Engage", 15, 340, 270)
        self.draw_text(self.screen, "Asteroid", 20, 390, 300)
        self.draw_text(self.screen, "Field", 20, 450, 325)
        self.draw_text(self.screen, "Visit", 15, 340, 415)
        self.draw_text(self.screen, "Upgrade", 20, 390, 445)
        self.draw_text(self.screen, "Shop", 20, 450, 470)

        self.draw_text(self.screen, "Begin", 15, 1350, 270)
        self.draw_text(self.screen, "Mission", 20, 1400, 300)
        self.draw_text(self.screen, "Engage", 15, 1350, 415)
        self.draw_text(self.screen, "Random", 20, 1400, 445)
        self.draw_text(self.screen, "Battle", 20, 1460, 470)
        options_cursor_coords = [(200, 280), (200, 424), (1210, 280), (1210, 424)]
        pygame.display.flip()
        #self.wait_for_key()
        choice = self.navigate_menu([0, 1, 2, 3], options_cursor_coords)
        if choice == 0:
            self.initialize()
            self.all_sprites.add(self.player)
            self.run('asteroid_field')
        elif choice == 1:
            self.upgrade_shop()
        elif choice == 2:
            self.initialize()
            self.all_sprites.add(self.player)
            self.run(self.stages[self.stage_index])
        elif choice == 3:
            self.show_controls()

    def upgrade_shop(self):
        self.screen.fill(BLACK)
        #self.screen.blit(self.gui_dial_box, (60, 160))
        #self.screen.blit(self.gui_dial_box, (60, 264))
        #self.screen.blit(self.gui_dial_box, (60, 890))
        """
        money_box = pygame.transform.scale(self.gui_dial_box, (700, 86))
        self.screen.blit(money_box, (60, 56))
        quantity_box = pygame.transform.scale(self.gui_dial_box, (219, 490))
        self.screen.blit(quantity_box, (60, 374))

        inventory_box = pygame.transform.scale(self.gui_dial_box, (440, 820))
        self.screen.blit(inventory_box, (320, 160))
        upgrade_box = pygame.transform.scale(self.gui_dial_box, (1010, 500))
        self.screen.blit(upgrade_box, (790, 56))
        price_box = pygame.transform.scale(self.gui_dial_box, (400, 400))
        self.screen.blit(price_box, (790, 580))
        descript_box = pygame.transform.scale(self.gui_dial_box, (580, 400))
        self.screen.blit(descript_box, (1220, 580))
        """
        pygame.display.flip()

        exit = False
        while not exit:
            self.clock.tick(FPS)
            # boxes
            money_box = self.ui_box(60, 56, 700, 86, UI_BOX_BLUE)
            self.ui_box_leftText("Credits:", WHITE, 20, (60+10), (56+20))
            self.ui_box_rightText(str(self.money), WHITE, 25, 760-10, 56+60)
            quantity_box = self.ui_box(60, 374, 219, 490, UI_BOX_BLUE)
            inventory_box = self.ui_box(320, 160, 440, 820, UI_BOX_BLUE)
            self.ui_box_leftText("Inventory:", WHITE, 20, 320+10, 160+20)
            upgrade_box = self.ui_box(790, 56, 1010, 500, UI_BOX_BLUE)
            self.ui_box_leftText("Upgrades & Supplies:", WHITE, 20, 790+10, 56+20)
            price_box = self.ui_box(790, 580, 400, 400, UI_BOX_BLUE)
            self.ui_box_leftText("Price:", WHITE, 20, 790+10, 580+20)
            descript_box = self.ui_box(1220, 580, 580, 400, UI_BOX_BLUE)
            self.ui_box_leftText("Description:", WHITE, 20, 1220+10, 580+20)

            # buttons
            buy = self.button("BUY", WHITE, 30, 60, 160, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
            sell = self.button("SELL", WHITE, 30, 60, 264, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
            back = self.button("BACK", WHITE, 30, 60, 890, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
            gun_power_upgrade = self.upgrade_button('gun_power_up', 830, 146)
            gun_2shot_upgrade = self.upgrade_button('gun_2shot_up', 830, 238)
            gun_speed_upgrade = self.upgrade_button('gun_speed_up', 830, 330)
            shield_upgrade = self.upgrade_button('shield_up', 830, 422)

            missile_upgrade = self.upgrade_button('missile_up', 922, 146)
            h_missile_upgrade = self.upgrade_button('h_missile_up', 922, 238)
            ship_plating_upgrade = self.upgrade_button('ship_plating_up', 922, 330)
            booster_upgrade = self.upgrade_button('booster_up', 922, 422)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    self.quit()
            if back:
                exit = True
            pygame.display.flip()
        self.ship_deck_menu()
        #self.wait_for_key()

    def upgrade_button(self, upgrade_name, x, y, action=None):
        #img.set_colorkey(WHITE)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        img = self.upgrade_images[upgrade_name]
        rect = img.get_rect()
        w, h = img.get_size()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            # pygame.draw.rect(self.screen, select_color, (x,y,w,h))
            button = pygame.Surface((w-2, h-2)).convert_alpha()
            button.fill((255, 255, 255, 50))
            self.screen.blit(img, (x, y))
            self.screen.blit(button, (x+1, y+1))
            # if click[0] == 1 and action:
            #    action()
            if click[0] == 1:
                return True
        else:
            # pygame.draw.rect(self.screen, color, (x,y,w,h))
            self.screen.blit(img, (x, y))
        #textSurf, textRect = self.text_objects(msg, msg_color, msg_size)
        #textRect.center = ((x + (w / 2)), (y + (h / 2)))
        #self.screen.blit(textSurf, textRect)
        return False

    def button(self, msg, msg_color, msg_size, x, y, w, h, color, select_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            #pygame.draw.rect(self.screen, select_color, (x,y,w,h))
            button = pygame.Surface((w,h)).convert_alpha()
            button.fill(select_color)
            self.screen.blit(button, (x,y))
            #if click[0] == 1 and action:
            #    action()
            if click[0] == 1:
                return True
        else:
            #pygame.draw.rect(self.screen, color, (x,y,w,h))
            button = pygame.Surface((w, h)).convert_alpha()
            button.fill(color)
            self.screen.blit(button, (x, y))
        textSurf, textRect = self.text_objects(msg, msg_color, msg_size)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        self.screen.blit(textSurf, textRect)
        return False

    def ui_box(self, x, y, w, h, color):
        button = pygame.Surface((w, h)).convert_alpha()
        button.fill(color)
        self.screen.blit(button, (x, y))
        return

    def ui_box_leftText(self, text, text_color, size, text_left, text_centery):
        textSurf, textRect = self.text_objects(text, text_color, size)
        textRect.left, textRect.centery = text_left, text_centery
        self.screen.blit(textSurf, textRect)

    def ui_box_rightText(self, text, text_color, size, text_right, text_centery):
        textSurf, textRect = self.text_objects(text, text_color, size)
        textRect.right, textRect.centery = text_right, text_centery
        self.screen.blit(textSurf, textRect)

    def text_objects(self, text, text_color, size):
        font = pygame.font.Font(self.font_name, size)
        textSurface = font.render(text, True, text_color)
        return textSurface, textSurface.get_rect()

    def initialize(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player_shields = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.damanging_explosions = pygame.sprite.Group()
        self.enemy_bombs = pygame.sprite.Group()

        # Score
        self.score = 0
        self.paused = False
        # Background music starts before the game loop starts. loops=-1 instructs pygame to replay/loop the music
        #pygame.mixer.music.play(loops=-1)

    def run(self, stage_name):
        # game loop - set self.playing = False to end the game
        pygame.mixer.music.play(loops=-1)
        self.stage_beaten = False
        asteroid_end_of_list = False
        spawned_first_enemy = False
        spawned_meteor_wave = False
        self.playing = True
        stage_wave_index = 0
        timer = pygame.time.get_ticks()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused:
                # spawning meteors when we are playing in an asteroid field
                if stage_name == 'asteroid_field' and not asteroid_end_of_list and not self.stage_beaten:
                    asteroid_spawn_list = stage_dict[stage_name]
                    asteroid_spawn = asteroid_spawn_list[stage_wave_index]
                    now = pygame.time.get_ticks()
                    if not spawned_first_enemy or now - timer > 30000:
                        self.spawnEnemy(asteroid_spawn[0], asteroid_spawn[1], asteroid_spawn[2], asteroid_spawn[3])
                        spawned_meteor_wave = True
                        spawned_first_enemy = True
                    if stage_wave_index < len(asteroid_spawn_list) - 1:
                        if spawned_meteor_wave:
                            stage_wave_index += 1
                            timer = now
                            spawned_meteor_wave = False
                    else:
                        asteroid_end_of_list = True
                    if game_conditions.game_over:
                        self.stage_beaten = True
                # spawning waves when not playing the asteroid field
                elif stage_name != 'asteroid_field' and not self.mobs and not self.stage_beaten:
                    stage = stage_dict[stage_name]
                    now = pygame.time.get_ticks()
                    if not spawned_first_enemy or now - timer > 1000:
                        for mob_descript in stage[stage_wave_index]:
                            self.spawnEnemy(mob_descript[0], mob_descript[1], mob_descript[2])
                        if stage_wave_index < len(stage)-1:
                            stage_wave_index += 1
                        else:
                            self.stage_beaten = True
                        timer = now
                        spawned_first_enemy = True
                self.update()
            self.draw()

# create the game object
g = Game()
choice = g.show_start_screen()

#while True:
#    g.new()
#    g.run()
    #g.show_go_screen()
