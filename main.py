# Shoot 'Em Up Game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# space ship sprites by http://millionthvector.blogspot.com/, http://pixeljoint.com/p/887.htm, http://fractalsoftworks.com/forum/index.php?action=profile;u=2206;sa=showPosts
# space ship sprites by Skorpio

# Story to be implemented: as a new graduate of the Republic Intergalactic Military Academy, the protagonist is assigned
# to a special unit that hunts down criminal smuggler and slaver-trader rings that have formed near neutral planets.
# Successfully accomplishing the missions will convince neutral planets to join the Sovereign Planetary League.
# After the protagonist has destroyed the crime boss Victor Yagga, rumors and reports of a wide-spread rebellion/coup
# begin to spread. Grand General Rex leads the new insurrection in hopes of establishing a galactic empire, taking with
# him the vast majority of the Republic Intergalactic Army and leaving the loyalists without a head commander.
# Here the protagonist must choose to either remain loyal to the Republic or join the rebellion.
#
# Side with the Republic:
# Lieutenant General Ulysses Halcyon takes command of the remaining Republic forces and orders the protagonist to
# re-establish Republic rule in rebel planets. After re-capturing most of the rogue planets, the protagonist faces off
# against General Rex and, despite his attempt to bring Rex into custody for trial, ends the rebellion by killing Rex.
# The old republic, even with all its flaws, continues to endure into an uncertain future.
#
# Side with the Insurrection:
# Grand General Rex orders the protagonist to establish Imperial dominion in the planets that remain loyal to the
# Republic. After conquering most of the remaining planets, the protagonist faces off against his old comrades and is
# forced to kill them. After this point, the protagonist may choose to overthrow General Rex and become the new leader
# of the insurrection. Nearing the end, the protagonist fights and kills General Ulysses Halcyon, thus bringing an
# end to the millenial reign of the old Republic. With the rise of a new empire, the newly-crowned Imperator is free
# to rule as he see fits, though whether he will establish a just nation or reign as a tyrant is unknown.

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
        self.stages = ['stage1', 'stage2']
        self.stage_index = 0
        self.stage_beaten = False

        # keep track of current stage so that, when game over, we can continue on the stage if we so chose
        self.current_stage = self.stages[self.stage_index]
        # make True if we are currently having a dialogue.
        self.dialog_flag_encountered = False
        self.on_dialogue_stage = False
        #self.dialog_name_index = 0
        self.dialog_turn_index = 0
        #self.dialog_line_broken = False
        self.stage_respawn_list = []

        self.money = 1000000
        self.inventory = {'Amethyst Ore': 0, 'Aquamarine Ore': 0, 'Bronze Ore': 0, 'Diamond Ore': 0, 'Emerald Ore': 0,
                          'Garnet Ore': 0, 'Gold Ore': 0, 'Sapphire Ore': 0, 'Silver Ore': 0, 'Steel Ore': 0,
                          'Titanium Ore': 0, 'Topaz Ore': 0, 'Amethyst': 0, 'Aquamarine': 0, 'Bronze Plate': 0,
                          'Diamond': 0, 'Emerald': 0, 'Garnet': 0, 'Gold Plate': 0, 'Sapphire': 0, 'Silver Plate': 0,
                          'Steel Plate': 0, 'Titanium Plate': 0, 'Topaz': 0}

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
        #if game_conditions.game_over:
        #    self.show_gameover_screen()
        #    print('hi')

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
                self.explode(hit.rect.center, hit.mtype)
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
                self.explode(hit.rect.center, hit.mtype)
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
            self.explode(hit.rect.center, hit.mtype)
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
                self.player.health = self.player.total_health

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
                self.player.health = self.player.total_health

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
                if self.player.health >= self.player.total_health:
                    self.player.health = self.player.total_health
            elif hit.type == 'gun_2shot':
                self.player.gun_2shot()
                self.gun_2shot_sound.play()
            elif hit.type == 'gun_speed':
                self.player.gun_speed()
                self.gun_speed_sound.play()
            elif hit.type == 'gun_power':
                self.player.gun_powerup()
                self.gun_power_sound.set_volume(0.6)
                self.gun_power_sound.play()
            elif hit.type == 'shield':
                if not self.player.force_field:
                    p_shield = Shield(self, self.player)
                    #self.all_sprites.add(p_shield)
                    #self.player_shields.add(p_shield)
                self.shield_power_sound.play()
                self.player.shield()
            elif hit.type == 'missile':
                self.player.missile_powerup()
                self.missile_pow_sound.play()
            elif hit.type == 'h_missile':
                self.player.h_missile_powerup()
                self.h_missile_pow_sound.play()
            else:
                self.inventory[hit.type] += 1
                self.jewel_pow_sound.play()

        # reactivate the player's shield if shield down and fully regenerated
        if self.player.shield_health == self.player.shield_total_health and not self.player.force_field:
            p_shield = Shield(self, self.player)
            #self.all_sprites.add(p_shield)
            #self.player_shields.add(p_shield)
            self.shield_power_sound.play()
            self.player.shield()

        # Check to see if mobs hit the player's shield
        hits = pygame.sprite.groupcollide(self.player_shields, self.mobs, False, False,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
            for mob in hits[hit]:
                mob.kill()
                self.player.shield_health -= mob.collision_dmg
                self.explode(mob.rect.center, mob.mtype)
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
        hits = pygame.sprite.groupcollide(self.player_shields, self.enemy_bullets, False, False,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
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
                    self.player.health = self.player.total_health

        # Check to see if a damaging explosion hit the player's shield
        hits = pygame.sprite.groupcollide(self.player_shields, self.damanging_explosions, False, False,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            if game_conditions.player_respawn_invinc:
                continue
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
                self.explode(hit.rect.center, hit.mtype)
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
        self.draw_grid()
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
        # if on dialog screen, keep iterating through the dialog pages when ENTER is pressed until pages run out
        if self.on_dialogue_stage:
            self.screen.blit(self.dialog_background, self.dialog_background_rect)
            line_counter = 0
            for line in dialog_box_dict[self.current_stage][self.dialog_turn_index]:
                self.ui_box_leftText(line, WHITE, 20, 384, 768 + (40 * line_counter))
                line_counter += 1
            self.ui_box_leftText("Press ENTER", WHITE, 15, 1248, 992)
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
                if event.key == pygame.K_RETURN:
                    if self.on_dialogue_stage:
                        if self.dialog_turn_index < len(dialog_box_dict[self.current_stage]) - 1:
                            self.dialog_turn_index += 1
                        else:
                            self.on_dialogue_stage = False
                            self.dialog_turn_index = 0

    def load_sprites(self):
        # dialog backgound
        self.dialog_background = pygame.image.load(path.join(img_dir, '1856x1024_dialog_stage.png')).convert_alpha()
        self.dialog_background_rect = self.dialog_background.get_rect()
        # player sprites
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
        self.player_img = pygame.transform.scale(player_img, (75, 57))
        self.player_mini_img = pygame.transform.scale(player_img, (25, 19))
        self.player_mini_img.set_colorkey(BLACK)
        # mob sprites
        enemyship1_img = pygame.image.load(path.join(img_dir, "enemyRed1.png")).convert()
        self.enemyship1_img = pygame.transform.scale(enemyship1_img, (50, 38))
        enemyfighter1_img = pygame.image.load(path.join(img_dir, "enemyRed2.png")).convert()
        self.enemyfighter1_img = pygame.transform.scale(enemyfighter1_img, (50, 38))
        enemy_kamikaze_img = pygame.image.load(path.join(img_dir, "enemyGreen5.png")).convert()
        self.enemy_kamikaze_img = pygame.transform.scale(enemy_kamikaze_img, (50, 38))
        self.enemy_bomber_img = pygame.image.load(path.join(img_dir, "heavyfreighter.png")).convert()
        #self.enemy_bomber_img = pygame.transform.scale(enemy_bomber_img, (50, 38))
        self.enemy_cruiser1_img = pygame.image.load(path.join(img_dir, "Human-Battleship2.png")).convert_alpha()
        # Smuggler Faction sprites
        enemy_smuggler1_img = pygame.image.load(path.join(img_dir, "smugglerShip.png")).convert()
        self.enemy_smuggler1_img = pygame.transform.scale(enemy_smuggler1_img, (60, 40))
        enemy_smuggler2_img = pygame.image.load(path.join(img_dir, "smugglerShip2.png")).convert()
        self.enemy_smuggler2_img = pygame.transform.scale(enemy_smuggler2_img, (103, 82))
        self.enemy_smuggler0_img = pygame.image.load(path.join(img_dir, "bgspeedship.png")).convert()
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
        self.shop_images = {}
        self.upgrade_images['gun_power_up'] = pygame.image.load(path.join(img_dir, 'SC2_vehicle_weapons_1.png')).convert()
        self.upgrade_images['gun_2shot_up'] = pygame.image.load(path.join(img_dir, 'SC2_ship_weapons_1.png')).convert()
        self.upgrade_images['gun_speed_up'] = pygame.image.load(path.join(img_dir, 'SC2_infantry_weapons_1.png')).convert()
        self.upgrade_images['shield_up'] = pygame.image.load(path.join(img_dir, 'SC2_shields_1.png')).convert()
        self.upgrade_images['ship_plating_up'] = pygame.image.load(path.join(img_dir, 'SC2_vehicle_plating_1.png')).convert()
        self.upgrade_images['missile_up'] = pygame.image.load(path.join(img_dir, 'SC2_missiles.jpg')).convert()
        self.upgrade_images['h_missile_up'] = pygame.image.load(path.join(img_dir, 'SC2_hisec_auto_tracking.png')).convert()
        self.upgrade_images['booster_up'] = pygame.image.load(path.join(img_dir, 'SC2_booster_1.png')).convert()
        # gems and other supplies
        self.shop_images['Amethyst Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Amethyst_Ore.png')).convert()
        self.shop_images['Aquamarine Ore'] = pygame.image.load(path.join(img_dir, 'Etc_AquaMarine_Ore.png')).convert()
        self.shop_images['Bronze Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Bronze_Ore.png')).convert()
        self.shop_images['Diamond Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Diamond_Ore.png')).convert()
        self.shop_images['Emerald Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Emerald_Ore.png')).convert()
        self.shop_images['Garnet Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Garnet_Ore.png')).convert()
        self.shop_images['Gold Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Gold_Ore.png')).convert()
        self.shop_images['Sapphire Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Sapphire_Ore.png')).convert()
        self.shop_images['Silver Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Silver_Ore.png')).convert()
        self.shop_images['Steel Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Steel_Ore.png')).convert()
        self.shop_images['Titanium Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Titanium_Ore.png')).convert()
        self.shop_images['Topaz Ore'] = pygame.image.load(path.join(img_dir, 'Etc_Topaz_Ore.png')).convert()
        self.shop_images['Amethyst'] = pygame.image.load(path.join(img_dir, 'Etc_Amethyst.png')).convert()
        self.shop_images['Aquamarine'] = pygame.image.load(path.join(img_dir, 'Etc_AquaMarine.png')).convert()
        self.shop_images['Bronze Plate'] = pygame.image.load(path.join(img_dir, 'Etc_Bronze_Plate.png')).convert()
        self.shop_images['Diamond'] = pygame.image.load(path.join(img_dir, 'Etc_Diamond.png')).convert()
        self.shop_images['Emerald'] = pygame.image.load(path.join(img_dir, 'Etc_Emerald.png')).convert()
        self.shop_images['Garnet'] = pygame.image.load(path.join(img_dir, 'Etc_Garnet.png')).convert()
        self.shop_images['Gold Plate'] = pygame.image.load(path.join(img_dir, 'Etc_Gold_Plate.png')).convert()
        self.shop_images['Sapphire'] = pygame.image.load(path.join(img_dir, 'Etc_Sapphire.png')).convert()
        self.shop_images['Silver Plate'] = pygame.image.load(path.join(img_dir, 'Etc_Silver.png')).convert()
        self.shop_images['Steel Plate'] = pygame.image.load(path.join(img_dir, 'Etc_Steel_Plate.png')).convert()
        self.shop_images['Titanium Plate'] = pygame.image.load(path.join(img_dir, 'Etc_Titanium_Plate.png')).convert()
        self.shop_images['Topaz'] = pygame.image.load(path.join(img_dir, 'Etc_Topaz.png')).convert()
        # explosion sprites
        self.explosion_anim = {}
        self.explosion_anim['xxx_lg'] = []
        self.explosion_anim['xx_lg'] = []
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
            img_xxx_lg = pygame.transform.scale(img, (300, 300))
            self.explosion_anim['xxx_lg'].append(img_xxx_lg)
            img_xx_lg = pygame.transform.scale(img, (250, 250))
            self.explosion_anim['xx_lg'].append(img_xx_lg)
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
        self.bullet_img = pygame.transform.scale(bullet_img, (12, 80))
        bullet_small_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
        self.bullet_small_img = pygame.transform.scale(bullet_small_img, (11, 80))
        powerbullet1_img = pygame.image.load(path.join(img_dir, "laserRed14.png")).convert()
        self.powerbullet1_img = pygame.transform.scale(powerbullet1_img, (12, 80))
        powerbullet1_small_img = pygame.image.load(path.join(img_dir, "laserRed15.png")).convert()
        self.powerbullet1_small_img = pygame.transform.scale(powerbullet1_small_img, (11, 80))
        powerbullet2_img = pygame.image.load(path.join(img_dir, "laserGreen06.png")).convert()
        self.powerbullet2_img = pygame.transform.scale(powerbullet2_img, (12, 80))
        powerbullet2_small_img = pygame.image.load(path.join(img_dir, "laserGreen07.png")).convert()
        self.powerbullet2_small_img = pygame.transform.scale(powerbullet2_small_img, (11, 80))
        powerbullet3_img = pygame.image.load(path.join(img_dir, "laserBlue14.png")).convert()
        self.powerbullet3_img = pygame.transform.scale(powerbullet3_img, (12, 80))
        powerbullet3_small_img = pygame.image.load(path.join(img_dir, "laserBlue14.png")).convert()
        self.powerbullet3_small_img = pygame.transform.scale(powerbullet3_small_img, (11, 80))
        missile_img = pygame.image.load(path.join(img_dir, "spaceMissiles_001.png")).convert()
        self.missile_img = pygame.transform.scale(missile_img, (12, 60))
        shield_img = pygame.image.load(path.join(img_dir, 'shield_Edit.png'))
        self.shield_img = pygame.transform.scale(shield_img, (85, 85))
        mob_bullet_img = pygame.image.load(path.join(img_dir, "laserRed08.png")).convert()
        self.mob_bullet_img = pygame.transform.scale(mob_bullet_img, (25, 25))
        mob_bullet_yellow_img = pygame.image.load(path.join(img_dir, "laserYellow03.png")).convert()
        self.mob_bullet_yellow_img = pygame.transform.scale(mob_bullet_yellow_img, (25, 25))
        mob_bullet_orange_img = pygame.image.load(path.join(img_dir, "laserOrange03.png")).convert()
        self.mob_bullet_orange_img = pygame.transform.scale(mob_bullet_orange_img, (35, 35))
        self.mob_bullet_orange_split_img = pygame.transform.scale(mob_bullet_orange_img, (30, 30))
        self.mob_bomb_img = pygame.image.load(path.join(img_dir, "spaceMissiles_006.png")).convert()
        self.enemy_fighter1_bullet_img = pygame.image.load(path.join(img_dir, "laserRed07.png")).convert()
        #self.enemy_fighter1_bullet_img = pygame.transform.scale(enemy_fighter1_bullet_img, (9, 25))
        self.enemy_cruiser1_bullet_img = pygame.image.load(path.join(img_dir, "laserGreen06.png")).convert()
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
        self.jewel_pow_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Jewel.wav'))
        #self.jewel_pow_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Pickup_Coin6.wav'))
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

    def spawnEnemy(self, enemyType, formation=None, respawn=False, number=1, leftover_respawn=False):
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
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemyShip1(self, formation, order, 2)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemyShip1(self, formation, number, 2)
                m.formation = formation
        elif enemyType == 'enemySmuggler1':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemySmuggler1(self, formation, order, 20)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemySmuggler1(self, formation, number, 20)
                m.formation = formation
        elif enemyType == 'enemySmuggler2':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemySmuggler2(self, formation, order, 20)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemySmuggler2(self, formation, number, 20)
                m.formation = formation
        elif enemyType == 'enemySmugglerLieut':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemySmugglerLieut(self, formation, order, 200)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemySmugglerLieut(self, formation, number, 20)
                m.formation = formation
        elif enemyType == 'enemyFighter1':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemyFighter1(self, formation, order, 5)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemyFighter1(self, formation, number, 5)
                m.formation = formation
        elif enemyType == 'kamikaze':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = Kamikaze(self, formation, order)
                    m.formation = formation
            elif leftover_respawn:
                m = Kamikaze(self, formation, number)
                m.formation = formation
        elif enemyType == 'enemyBomber':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemyBomber(self, formation, order, 5)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemyBomber(self, formation, number, 5)
                m.formation = formation
        elif enemyType == 'enemyCruiser1':
            if not respawn and not leftover_respawn:
                for order in range(0, number if number > 1 else 1):
                    m = EnemyCruiser1(self, formation, order, 100)
                    m.formation = formation
            elif leftover_respawn:
                m = EnemyCruiser1(self, formation, number, 100)
                m.formation = formation

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
        options_cursor_coords = [((WIDTH / 2) - 240, HEIGHT / 2 - 5), ((WIDTH / 2) - 300, HEIGHT * (6 / 10) - 5),
                                 ((WIDTH / 2) - 250, HEIGHT * (7 / 10) - 5)]
        pygame.display.flip()
        choice  = self.navigate_menu([0,1,2], options_cursor_coords)
        if choice == 0:
            self.player.lives = 3
            self.initialize()
            self.all_sprites.add(self.player)
            self.run(self.current_stage)
        elif choice == 1:
            self.ship_deck_menu()
        elif choice == 2:
            self.quit()

    def show_stage_conclusion_screen(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.screen, "Mission Successful!", 70, WIDTH / 2, HEIGHT * (2.5 / 10))
        self.draw_text(self.screen, "Proceed to Menu", 30, WIDTH / 2, HEIGHT * (5/10))
        self.draw_text(self.screen, "Retry Stage", 30, WIDTH / 2, HEIGHT * (6/10))
        self.draw_text(self.screen, "Exit Game", 30, WIDTH / 2, HEIGHT * (7/10))
        self.draw_text(self.screen, "Press Enter to select", 20, WIDTH / 2, HEIGHT * (9 / 10))
        options_cursor_coords = [((WIDTH / 2) - 370, HEIGHT / 2 - 5), ((WIDTH / 2) - 300, HEIGHT * (6 / 10) - 5),
                                 ((WIDTH / 2) - 250, HEIGHT * (7 / 10) - 5)]
        pygame.display.flip()
        choice  = self.navigate_menu([0,1,2], options_cursor_coords)
        if choice == 0:
            if self.stage_index < len(self.stages):
                self.stage_index += 1
            self.ship_deck_menu()
        elif choice == 1:
            self.player.lives = 3
            self.initialize()
            self.all_sprites.add(self.player)
            self.run(self.current_stage)
        elif choice == 2:
            self.quit()

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
            self.current_stage = 'asteroid_field'
            self.run('asteroid_field')
        elif choice == 1:
            self.upgrade_shop()
        elif choice == 2:
            self.initialize()
            self.all_sprites.add(self.player)
            self.current_stage = self.stages[self.stage_index]
            self.run(self.stages[self.stage_index])
        elif choice == 3:
            self.show_controls()

    def upgrade_shop(self):
        self.screen.fill(BLACK)
        pygame.display.flip()

        self.item_upgrade_corresp = {'gun_power_up': self.player.gun_power_upgrade,
                                     'gun_speed_up': self.player.gun_speed_upgrade,
                                     'gun_2shot_up': self.player.gun_2shot_upgrade,
                                     'missile_up': self.player.missile_upgrade,
                                     'h_missile_up': self.player.h_missile_upgrade,
                                     'shield_up': self.player.shield_upgrade,
                                     'ship_plating_up': self.player.ship_plating_upgrade,
                                     'booster_up': self.player.booster_upgrade}
        self.item_name_player_lvl = {'gun_power_up': self.player.gun_power_upgraded_lvl,
                                     'gun_speed_up': self.player.gun_speed_upgraded_lvl,
                                     'gun_2shot_up': self.player.gun_2s_upgraded_lvl,
                                     'missile_up': self.player.missile_upgraded_lvl,
                                     'h_missile_up': self.player.h_missile_upgraded_lvl,
                                     'shield_up': self.player.shield_upgraded_lvl,
                                     'ship_plating_up': self.player.ship_plating_upgraded_lvl,
                                     'booster_up': self.player.booster_upgraded_lvl}
        self.item_name_png_corresp = {'gun_power_up': 'SC2_vehicle_weapons_1.png',
                                     'gun_speed_up': 'SC2_infantry_weapons_1.png',
                                     'gun_2shot_up': 'SC2_ship_weapons_1.png',
                                     'missile_up': 'SC2_missiles.jpg',
                                     'h_missile_up': 'SC2_hisec_auto_tracking.png',
                                     'shield_up': 'SC2_shields_1.png',
                                     'ship_plating_up': 'SC2_vehicle_plating_1.png',
                                     'booster_up': 'SC2_booster_1.png'}

        self.mouse_press_lifted = True

        selected_to_buy, selected_to_sell = False, False
        buy, sell, cancel, plus, minus, is_first_sell_amount = False, False, False, False, False, True
        buy_amount, sell_amount = 1, 1
        selected_item, old_selected_item = None, None

        exit = False
        while not exit:
            self.clock.tick(FPS)

            mouse_clicked = pygame.mouse.get_pressed()
            if mouse_clicked[0] == 0:
                self.mouse_press_lifted = True

            self.item_name_player_lvl['gun_power_up'] = self.player.gun_power_upgraded_lvl
            self.item_name_player_lvl['gun_speed_up'] = self.player.gun_speed_upgraded_lvl
            self.item_name_player_lvl['gun_2shot_up'] = self.player.gun_2s_upgraded_lvl
            self.item_name_player_lvl['missile_up'] = self.player.missile_upgraded_lvl
            self.item_name_player_lvl['h_missile_up'] = self.player.h_missile_upgraded_lvl
            self.item_name_player_lvl['shield_up'] = self.player.shield_upgraded_lvl
            self.item_name_player_lvl['ship_plating_up'] = self.player.ship_plating_upgraded_lvl
            self.item_name_player_lvl['booster_up'] = self.player.booster_upgraded_lvl

            # boxes and text headers within
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
            if selected_to_buy:
                is_first_sell_amount = True
                if old_selected_item != selected_item:
                    buy_amount = 1
                    old_selected_item = selected_item
                if selected_item[1] == 'upgrade':
                    buy = self.button("BUY", WHITE, 30, 60, 160, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                    cancel = self.button("CANCEL", WHITE, 22, 60, 264, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE,
                                         None)
                    buy_upgrade_img = self.upgrade_images[selected_item[0]]
                    #buy_upgrade_img.set_colorkey(WHITE)
                    self.screen.blit(buy_upgrade_img, (140, 555))
                    #self.ui_box_centerText(str(buy_amount), WHITE, 30, 170, 660)
                    if buy and self.money >= item_prices[selected_item[0]]:
                        self.money -= item_prices[selected_item[0]]
                        self.item_upgrade_corresp[selected_item[0]]()
                elif selected_item[1] == 'shop':
                    buy = self.button("BUY", WHITE, 30, 60, 160, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                    plus = self.button("+", WHITE, 30, 125, 400, 86, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                    minus = self.button("-", WHITE, 30, 125, 755, 86, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                    cancel = self.button("CANCEL", WHITE, 22, 60, 264, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE,
                                         None)
                    temp_buy_item_img = self.shop_images[selected_item[0]]
                    buy_item_img = pygame.transform.scale(temp_buy_item_img, (
                    int(temp_buy_item_img.get_size()[0] * 1.7), int(temp_buy_item_img.get_size()[1] * 1.7)))
                    buy_item_img.set_colorkey(BLACK)
                    self.screen.blit(buy_item_img, (155, 555))
                    self.ui_box_centerText(str(buy_amount), WHITE, 30, 170, 660)
                    if plus and buy_amount < 1000:
                        buy_amount += 1
                    elif minus and buy_amount > 1:
                        buy_amount -= 1
                    elif buy and self.money >= item_prices[selected_item[0]] * buy_amount:
                        self.money -= item_prices[selected_item[0]] * buy_amount
                        self.inventory[selected_item[0]] += buy_amount
            elif selected_to_sell:
                if old_selected_item != selected_item:
                    is_first_sell_amount = True
                    old_selected_item = selected_item
                buy_amount = 1
                sell = self.button("SELL", WHITE, 30, 60, 160, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                plus = self.button("+", WHITE, 30, 125, 400, 86, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                minus = self.button("-", WHITE, 30, 125, 755, 86, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                cancel = self.button("CANCEL", WHITE, 22, 60, 264, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)
                if is_first_sell_amount:
                    curr_stock_inv = self.inventory[selected_item[0]]
                    sell_amount = curr_stock_inv
                    is_first_sell_amount = False
                temp_sell_item_img = self.shop_images[selected_item[0]]
                sell_item_img = pygame.transform.scale(temp_sell_item_img, (int(temp_sell_item_img.get_size()[0] * 1.7), int(temp_sell_item_img.get_size()[1] * 1.7)))
                sell_item_img.set_colorkey(BLACK)
                self.screen.blit(sell_item_img, (155, 555))
                self.ui_box_centerText(str(sell_amount), WHITE, 30, 170, 660)
                if plus and sell_amount < curr_stock_inv:
                    sell_amount += 1
                elif minus and sell_amount > 1:
                    sell_amount -= 1
                elif sell and self.inventory[selected_item[0]] > 0:
                    self.inventory[selected_item[0]] -= sell_amount
                    if selected_item[1] == 'inv':
                        self.money += int(item_prices[selected_item[0]] / 2) * sell_amount
                    else:
                        self.money += item_prices[selected_item[0]] * sell_amount
                    sell_amount = self.inventory[selected_item[0]]
            else:
                self.ui_box(60, 160, 219, 86, UI_BOX_BLUE)
                self.ui_box(60, 264, 219, 86, UI_BOX_BLUE)
            back = self.button("BACK", WHITE, 30, 60, 890, 219, 86, BUTTON_LIGHT_BLUE, BUTTON_SELECTED_BLUE, None)

            if cancel:
                selected_to_buy, selected_to_sell = False, False
                buy, sell, cancel, plus, minus, is_first_sell_amount = False, False, False, False, False, True
                buy_amount, sell_amount = 1, 1
                selected_item = None

            # inventory buttons
            inv_amethyst_ore = self.shop_item_button('Amethyst Ore', 340, 200)
            inv_aquamarine_ore = self.shop_item_button('Aquamarine Ore', 340, 260)
            inv_bronze_ore = self.shop_item_button('Bronze Ore', 340, 320)
            inv_diamond_ore = self.shop_item_button('Diamond Ore', 340, 380)
            inv_emerald_ore = self.shop_item_button('Emerald Ore', 340, 440)
            inv_garnet_ore = self.shop_item_button('Garnet Ore', 340, 500)

            inv_gold_ore = self.shop_item_button('Gold Ore', 540, 200)
            inv_sapphire_ore = self.shop_item_button('Sapphire Ore', 540, 260)
            inv_silver_ore = self.shop_item_button('Silver Ore', 540, 320)
            inv_steel_ore = self.shop_item_button('Steel Ore', 540, 380)
            inv_titanium_ore = self.shop_item_button('Titanium Ore', 540, 440)
            inv_topaz_ore = self.shop_item_button('Topaz Ore', 540, 500)

            inv_amethyst = self.shop_item_button('Amethyst', 345, 580)
            inv_aquamarine = self.shop_item_button('Aquamarine', 345, 640)
            inv_bronze_plate = self.shop_item_button('Bronze Plate', 335, 700)
            inv_diamond = self.shop_item_button('Diamond', 345, 760)
            inv_emerald = self.shop_item_button('Emerald', 345, 820)
            inv_garnet = self.shop_item_button('Garnet', 345, 880)

            inv_gold_plate = self.shop_item_button('Gold Plate', 535, 580)
            inv_sapphire = self.shop_item_button('Sapphire', 545, 640)
            inv_silver_plate = self.shop_item_button('Silver Plate', 535, 700)
            inv_steel_plate = self.shop_item_button('Steel Plate', 535, 760)
            inv_titanium_plate = self.shop_item_button('Titanium Plate', 535, 820)
            inv_topaz = self.shop_item_button('Topaz', 545, 880)

            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (200 + 20))
            self.ui_box_rightText(str(self.inventory["Amethyst Ore"]), WHITE, 15, (540 - 40), (200 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (260 + 20))
            self.ui_box_rightText(str(self.inventory["Aquamarine Ore"]), WHITE, 15, (540 - 40), (260 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (320 + 20))
            self.ui_box_rightText(str(self.inventory["Bronze Ore"]), WHITE, 15, (540 - 40), (320 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (380 + 20))
            self.ui_box_rightText(str(self.inventory["Diamond Ore"]), WHITE, 15, (540 - 40), (380 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (440 + 20))
            self.ui_box_rightText(str(self.inventory["Emerald Ore"]), WHITE, 15, (540 - 40), (440 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (500 + 20))
            self.ui_box_rightText(str(self.inventory["Garnet Ore"]), WHITE, 15, (540 - 40), (500 + 20))

            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (200 + 20))
            self.ui_box_rightText(str(self.inventory["Gold Ore"]), WHITE, 15, (750 - 40), (200 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (260 + 20))
            self.ui_box_rightText(str(self.inventory["Sapphire Ore"]), WHITE, 15, (750 - 40), (260 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (320 + 20))
            self.ui_box_rightText(str(self.inventory["Silver Ore"]), WHITE, 15, (750 - 40), (320 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (380 + 20))
            self.ui_box_rightText(str(self.inventory["Steel Ore"]), WHITE, 15, (750 - 40), (380 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (440 + 20))
            self.ui_box_rightText(str(self.inventory["Titanium Ore"]), WHITE, 15, (750 - 40), (440 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (500 + 20))
            self.ui_box_rightText(str(self.inventory["Topaz Ore"]), WHITE, 15, (750 - 40), (500 + 20))

            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (580 + 20))
            self.ui_box_rightText(str(self.inventory["Amethyst"]), WHITE, 15, (540 - 40), (580 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (640 + 20))
            self.ui_box_rightText(str(self.inventory["Aquamarine"]), WHITE, 15, (540 - 40), (640 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (700 + 20))
            self.ui_box_rightText(str(self.inventory["Bronze Plate"]), WHITE, 15, (540 - 40), (700 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (760 + 20))
            self.ui_box_rightText(str(self.inventory["Diamond"]), WHITE, 15, (540 - 40), (760 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (820 + 20))
            self.ui_box_rightText(str(self.inventory["Emerald"]), WHITE, 15, (540 - 40), (820 + 20))
            self.ui_box_leftText("x", WHITE, 10, (340 + 50), (880 + 20))
            self.ui_box_rightText(str(self.inventory["Garnet"]), WHITE, 15, (540 - 40), (880 + 20))

            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (580 + 20))
            self.ui_box_rightText(str(self.inventory["Gold Plate"]), WHITE, 15, (750 - 40), (580 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (640 + 20))
            self.ui_box_rightText(str(self.inventory["Sapphire"]), WHITE, 15, (750 - 40), (640 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (700 + 20))
            self.ui_box_rightText(str(self.inventory["Silver Plate"]), WHITE, 15, (750 - 40), (700 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (760 + 20))
            self.ui_box_rightText(str(self.inventory["Steel Plate"]), WHITE, 15, (750 - 40), (760 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (820 + 20))
            self.ui_box_rightText(str(self.inventory["Titanium Plate"]), WHITE, 15, (750 - 40), (820 + 20))
            self.ui_box_leftText("x", WHITE, 10, (540 + 50), (880 + 20))
            self.ui_box_rightText(str(self.inventory["Topaz"]), WHITE, 15, (750 - 40), (880 + 20))

            # upgrade buttons
            gun_power_upgrade = self.shop_item_button('gun_power_up', 830, 146)
            gun_2shot_upgrade = self.shop_item_button('gun_2shot_up', 830, 238)
            gun_speed_upgrade = self.shop_item_button('gun_speed_up', 830, 330)
            shield_upgrade = self.shop_item_button('shield_up', 830, 422)

            missile_upgrade = self.shop_item_button('missile_up', 922, 146)
            h_missile_upgrade = self.shop_item_button('h_missile_up', 922, 238)
            ship_plating_upgrade = self.shop_item_button('ship_plating_up', 922, 330)
            booster_upgrade = self.shop_item_button('booster_up', 922, 422)

            # gems and other materials buttons
            shop_amethyst = self.shop_item_button('Amethyst', 1064, 156)
            shop_aquamarine = self.shop_item_button('Aquamarine', 1064, 248)
            shop_bronze_plate = self.shop_item_button('Bronze Plate', 1054, 340)
            shop_diamond = self.shop_item_button('Diamond', 1064, 432)

            shop_emerald = self.shop_item_button('Emerald', 1164, 156)
            shop_garnet = self.shop_item_button('Garnet', 1164, 248)
            shop_gold_plate = self.shop_item_button('Gold Plate', 1154, 340)
            shop_sapphire = self.shop_item_button('Sapphire', 1164, 432)

            shop_silver_plate = self.shop_item_button('Silver Plate', 1254, 156)
            shop_steel_plate = self.shop_item_button('Steel Plate', 1254, 248)
            shop_titanium_plate = self.shop_item_button('Titanium Plate', 1254, 340)
            shop_topaz = self.shop_item_button('Topaz', 1264, 432)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    self.quit()
            if back:
                exit = True

            # display the item price and descriptions
            if gun_power_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['gun_power_up']), WHITE, 20, 1190-10, 580+60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190-205, 580+100)
                # description
                self.ui_box_leftText("Upgrade: Gun Power", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Increases the DAMAGE", WHITE, 20, 1220+10, 580+120)
                self.ui_box_leftText("output of your gun.", WHITE, 20, 1220 + 10, 580 + 160)
                if gun_power_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["gun_power_up", "upgrade"]
            elif gun_2shot_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['gun_2shot_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Double Guns", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Allows the ship to", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("fire from two cannons.", WHITE, 20, 1220 + 10, 580 + 160)
                if gun_2shot_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["gun_2shot_up", "upgrade"]
            elif gun_speed_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['gun_speed_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Rapid Fire", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Increases the rate of", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("fire from your gun(s).", WHITE, 20, 1220 + 10, 580 + 160)
                if gun_speed_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["gun_speed_up", "upgrade"]
            elif shield_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['shield_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Shield", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Increases the DURATION", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("of the ship's shield.", WHITE, 20, 1220 + 10, 580 + 160)
                if shield_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["shield_up", "upgrade"]
            elif missile_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['missile_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Missiles", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Installs missiles in", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("the ship. Fire by", WHITE, 20, 1220 + 10, 580 + 160)
                self.ui_box_leftText("pressing [A]", WHITE, 20, 1220 + 10, 580 + 200)
                if missile_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["missile_up", "upgrade"]
            elif h_missile_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['h_missile_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Homing", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Missiles", WHITE, 20, 1467, 580 + 100)
                self.ui_box_leftText("Installs homing", WHITE, 20, 1220 + 10, 580 + 160)
                self.ui_box_leftText("missiles in the ship.", WHITE, 20, 1220 + 10, 580 + 200)
                self.ui_box_leftText("Fire by pressing [A]", WHITE, 20, 1220 + 10, 580 + 240)
                if h_missile_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["h_missile_up", "upgrade"]
            elif ship_plating_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['ship_plating_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Ship Plating", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Increases the HEALTH", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("of the ship.", WHITE, 20, 1220 + 10, 580 + 160)
                if ship_plating_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["ship_plating_up", "upgrade"]
            elif booster_upgrade[0]:
                # price
                self.ui_box_rightText(str(item_prices['booster_up']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Upgrade: Booster", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("Engine", WHITE, 20, 1467, 580 + 100)
                self.ui_box_leftText("Increases the ship's", WHITE, 20, 1220 + 10, 580 + 160)
                self.ui_box_leftText("MOVEMENT SPEED.", WHITE, 20, 1220 + 10, 580 + 200)
                if booster_upgrade[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["booster_up", "upgrade"]

            elif shop_amethyst[0] or inv_amethyst[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Amethyst'] / 2) if inv_amethyst[0] else item_prices['Amethyst']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Amethyst", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious purple", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_amethyst[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Amethyst", "shop"]
                elif inv_amethyst[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Amethyst", "inv"]
            elif shop_aquamarine[0] or inv_aquamarine[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Aquamarine'] / 2) if inv_aquamarine[0] else item_prices['Aquamarine']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Aquamarine", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious blue", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_aquamarine[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Aquamarine", "shop"]
                elif inv_aquamarine[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Aquamarine", "inv"]
            elif shop_bronze_plate[0] or inv_bronze_plate[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Bronze Plate'] / 2) if inv_bronze_plate[0] else item_prices['Bronze Plate']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Bronze Plate", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A light, weak and", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("refined bronze.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_bronze_plate[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Bronze Plate", "shop"]
                elif inv_bronze_plate[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Bronze Plate", "inv"]
            elif shop_diamond[0] or inv_diamond[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Diamond'] / 2) if inv_diamond[0] else item_prices['Diamond']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Diamond", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious and", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("transparent jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_diamond[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Diamond", "shop"]
                elif inv_diamond[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Diamond", "inv"]
            elif shop_emerald[0] or inv_emerald[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Emerald'] / 2) if inv_emerald[0] else item_prices['Emerald']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Emerald", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious green", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_emerald[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Emerald", "shop"]
                elif inv_emerald[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Emerald", "inv"]
            elif shop_garnet[0] or inv_garnet[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Garnet'] / 2) if inv_garnet[0] else item_prices['Garnet']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Garnet", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious red", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_garnet[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Garnet", "shop"]
                elif inv_garnet[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Garnet", "inv"]
            elif shop_gold_plate[0] or inv_gold_plate[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Gold Plate'] / 2) if inv_gold_plate[0] else item_prices['Gold Plate']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Gold Plate", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A very rare and", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("refined gold.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_gold_plate[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Gold Plate", "shop"]
                elif inv_gold_plate[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Gold Plate", "inv"]
            elif shop_sapphire[0] or inv_sapphire[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Sapphire'] / 2) if inv_sapphire[0] else item_prices['Sapphire']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Sapphire", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious, blue, and", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("transparent jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_sapphire[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Sapphire", "shop"]
                elif inv_sapphire[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Sapphire", "inv"]
            elif shop_silver_plate[0] or inv_silver_plate[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Silver Plate'] / 2) if inv_silver_plate[0] else item_prices['Silver Plate']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Silver Plate", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A shiny, refined", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("silver.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_silver_plate[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Silver Plate", "shop"]
                elif inv_silver_plate[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Silver Plate", "inv"]
            elif shop_steel_plate[0] or inv_steel_plate[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Steel Plate'] / 2) if inv_steel_plate[0] else item_prices['Steel Plate']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Steel Plate", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A tough, refined", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("steel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_steel_plate[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Steel Plate", "shop"]
                elif inv_steel_plate[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Steel Plate", "inv"]
            elif shop_titanium_plate[0] or inv_titanium_plate[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Titanium Plate'] / 2) if inv_titanium_plate[0] else item_prices['Titanium Plate']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Titanium Plate", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A solid, light, and", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("refined titanium.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_titanium_plate[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Titanium Plate", "shop"]
                elif inv_titanium_plate[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Titanium Plate", "inv"]
            elif shop_topaz[0] or inv_topaz[0]:
                # price
                self.ui_box_rightText(str(int(item_prices['Topaz'] / 2) if inv_topaz[0] else item_prices['Topaz']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Topaz", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A precious yellow", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if shop_topaz[1]:
                    selected_to_buy, selected_to_sell = True, False
                    selected_item = ["Topaz", "shop"]
                elif inv_topaz[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Topaz", "inv"]

            elif inv_amethyst_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Amethyst Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Amethyst Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a precious", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("purple jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_amethyst_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Amethyst Ore", "inv_ore"]
            elif inv_aquamarine_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Aquamarine Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Aquamarine Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a precious", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("blue jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_aquamarine_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Aquamarine Ore", "inv_ore"]
            elif inv_bronze_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Bronze Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Bronze Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("A light, weak bronze", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("ore.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_bronze_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Bronze Ore", "inv_ore"]
            elif inv_diamond_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Diamond Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Diamond Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a precious", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("transparent jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_diamond_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Diamond Ore", "inv_ore"]
            elif inv_emerald_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Emerald Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Emerald Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a precious", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("green jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_emerald_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Emerald Ore", "inv_ore"]
            elif inv_garnet_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Garnet Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Garnet Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a precious", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("red jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_garnet_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Garnet Ore", "inv_ore"]
            elif inv_gold_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Gold Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Gold Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a very", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("rare mineral.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_gold_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Gold Ore", "inv_ore"]
            elif inv_sapphire_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Sapphire Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Sapphire Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a blue,", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("transparent jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_sapphire_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Sapphire Ore", "inv_ore"]
            elif inv_silver_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Silver Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Silver Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a shiny", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("silver.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_silver_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Silver Ore", "inv_ore"]
            elif inv_steel_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Steel Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Steel Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a tough", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("steel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_steel_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Steel Ore", "inv_ore"]
            elif inv_titanium_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Titanium Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Titanium Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a solid and", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("light titanium.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_titanium_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Titanium Ore", "inv_ore"]
            elif inv_topaz_ore[0]:
                # price
                self.ui_box_rightText(str(item_prices['Topaz Ore']), WHITE, 20, 1190 - 10, 580 + 60)
                self.ui_box_leftText("Credits", WHITE, 20, 1190 - 205, 580 + 100)
                # description
                self.ui_box_leftText("Topaz Ore", WHITE, 20, 1220 + 10, 580 + 60)
                self.ui_box_leftText("The ore of a precious", WHITE, 20, 1220 + 10, 580 + 120)
                self.ui_box_leftText("yellow jewel.", WHITE, 20, 1220 + 10, 580 + 160)
                if inv_topaz_ore[1]:
                    selected_to_buy, selected_to_sell = False, True
                    selected_item = ["Topaz Ore", "inv_ore"]
            pygame.display.flip()
        self.ship_deck_menu()
        #self.wait_for_key()

    def shop_item_button(self, shop_item_name, x, y, action=None):
        #img.set_colorkey(WHITE)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if shop_item_name in self.upgrade_images:
            img = self.upgrade_images[shop_item_name]
            if shop_item_name in ['gun_power_up', 'gun_2shot_up', 'gun_speed_up', 'shield_up', 'ship_plating_up', 'booster_up']:
                img = pygame.image.load(path.join(img_dir, self.item_name_png_corresp[shop_item_name][:-5] + str(self.item_name_player_lvl[shop_item_name]) + '.png'))
        elif shop_item_name in self.shop_images:
            orig_img = self.shop_images[shop_item_name]
            img = pygame.transform.scale(orig_img, (int(orig_img.get_size()[0] * 1.7), int(orig_img.get_size()[1] * 1.7)))
            img.set_colorkey(BLACK)
        rect = img.get_rect()
        w, h = img.get_size()
        mouse_on_button, mouse_clicked_button = False, False
        returnBools = [mouse_on_button, mouse_clicked_button]
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            # pygame.draw.rect(self.screen, select_color, (x,y,w,h))
            button = pygame.Surface((w-2, h-2)).convert_alpha()
            button.fill((255, 255, 255, 50))
            self.screen.blit(img, (x, y))
            self.screen.blit(button, (x+1, y+1))
            returnBools[0] = True
            # if click[0] == 1 and action:
            #    action()
            if click[0] == 1:
                returnBools[1] = True
            return returnBools
        else:
            # pygame.draw.rect(self.screen, color, (x,y,w,h))
            self.screen.blit(img, (x, y))
        return returnBools

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
            if click[0] == 1 and self.mouse_press_lifted:
                self.mouse_press_lifted = False
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
        #button = pygame.Surface((w, h)).convert_alpha()
        button = pygame.Surface((w, h)).convert()
        button.fill(color)
        self.screen.blit(button, (x, y))
        return

    def ui_box_centerText(self, text, text_color, size, text_centerx, text_centery):
        textSurf, textRect = self.text_objects(text, text_color, size)
        textRect.centerx, textRect.centery = text_centerx, text_centery
        self.screen.blit(textSurf, textRect)

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

    def reset_player_stats(self):
        # resets player stats and location in preparation for a new game
        self.player.lives = self.player.total_lives
        self.player.rect.center = (WIDTH / 2, HEIGHT - 10)
        self.player.health = self.player.total_health
        self.player.shield_health = self.player.shield_total_health
        # we need the player.forcefield to be false so that the shield will reboot
        self.player.force_field = False

    def initialize(self):
        # initialize all variables and do all the setup for a new game
        self.current_stage = self.stages[self.stage_index]
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player_shields = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.damanging_explosions = pygame.sprite.Group()
        self.enemy_bombs = pygame.sprite.Group()
        self.stage_respawn_list = []

        if game_conditions.game_over:
            game_conditions.game_over = False
            game_conditions.player_dead = False
            game_conditions.player_respawn_invinc = False
            game_conditions.player_temp_invulnerable = False
            # resets the player's position, health, etc.
            self.reset_player_stats()
        elif self.stage_beaten:
            self.reset_player_stats()
            self.stage_beaten = False

        # Score
        self.score = 0
        self.paused = False
        # Background music starts before the game loop starts. loops=-1 instructs pygame to replay/loop the music
        #pygame.mixer.music.play(loops=-1)

    def run(self, stage_name):
        # game loop - set self.playing = False to end the game
        pygame.mixer.music.play(loops=-1)
        #self.stage_beaten = False
        asteroid_end_of_list = False
        spawned_first_enemy = False
        spawned_meteor_wave = False
        self.reached_stage_end = False
        self.playing = True
        stage_wave_index = 0
        timer = pygame.time.get_ticks()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused and not self.on_dialogue_stage:
                now = pygame.time.get_ticks()
                # spawning meteors when we are playing in an asteroid field
                if stage_name == 'asteroid_field' and not asteroid_end_of_list and not self.stage_beaten:
                    asteroid_spawn_list = stage_dict[stage_name]
                    asteroid_spawn = asteroid_spawn_list[stage_wave_index]
                    #now = pygame.time.get_ticks()
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
                # also, spawns the next wave of the stage if no mobs are on map or if 7 seconds have passed
                # also, if not all enemies in a wave are killed, then return those enemies later
                elif stage_name != 'asteroid_field' and (not self.mobs or now - timer > 7000) and not self.stage_beaten:
                    stage = stage_dict[stage_name]
                    #now = pygame.time.get_ticks()
                    if stage[stage_wave_index] == 'empty wave':
                        timer = now
                        if stage_wave_index < len(stage)-1:
                            stage_wave_index += 1
                        else:
                            self.stage_beaten = True
                    elif stage[stage_wave_index] == 'fin':
                        self.reached_stage_end = True
                    elif stage[stage_wave_index] == 'no boss':
                        self.stage_respawn_list = []
                    elif not spawned_first_enemy or now - timer > 1000:
                        for mob_descript in stage[stage_wave_index]:
                            #if mob_descript == 'dialogue' and (self.mobs or self.stage_respawn_list):
                            if mob_descript == 'dialogue' and self.mobs:
                                self.dialog_flag_encountered = True
                                #print(stage[stage_wave_index])
                            #elif (self.dialog_flag_encountered and not (self.mobs or self.stage_respawn_list)) or (mob_descript == 'dialogue' and not (self.mobs or self.stage_respawn_list)):
                            elif (self.dialog_flag_encountered and not self.mobs) or (mob_descript == 'dialogue' and not self.mobs):
                                self.on_dialogue_stage = True
                                self.stage_respawn_list = []
                                self.dialog_flag_encountered = False
                            elif not self.dialog_flag_encountered:
                                self.spawnEnemy(mob_descript[0], mob_descript[1], mob_descript[2], mob_descript[3])
                        while self.stage_respawn_list and not self.on_dialogue_stage:
                            mob_descript = self.stage_respawn_list.pop(0)
                            self.spawnEnemy(mob_descript[0], mob_descript[1], mob_descript[2], mob_descript[3], True)
                        #else:
                        #   self.stage_beaten = True
                        timer = now
                        spawned_first_enemy = True
                    if stage_wave_index < len(stage)-1 or self.dialog_flag_encountered:
                        if not self.dialog_flag_encountered:
                            stage_wave_index += 1
                    elif self.reached_stage_end and not (self.mobs):
                        self.stage_beaten = True
                self.update()
            elif self.on_dialogue_stage:
                timer = pygame.time.get_ticks()
                self.update()
            self.draw()
            if game_conditions.game_over or self.stage_beaten:
                self.playing = False
        if game_conditions.game_over:
            self.show_gameover_screen()
        elif self.stage_beaten:
            self.show_stage_conclusion_screen()

# create the game object
g = Game()
choice = g.show_start_screen()

#while True:
#    g.new()
#    g.run()
    #g.show_go_screen()
