
# Shoot 'Em Up Game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

"""
import pygame, time, sys, random, sp_groups, game_conditions
from settings import *
from os import path

# The directories (of Sprites, etc)
#img_dir = path.join(path.dirname(__file__), 'img')
#sfx_dir = path.join(path.dirname(__file__), 'sfx')

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
# initialize pygame and create window
pygame.init()
# the mixer init starts the sound system
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot 'Em Up")
clock = gameclock

from player import Player, player_mini_img, Shield
from mob import Meteor
from pups_expls import Pow, Explosion
import bground


# scrolling background
def scroll_background(surf, bg, speedy):
    background_size = bg.get_size()
    w, h = background_size
    bground.speedy = speedy
    bground.y += speedy
    bground.y1 += speedy
    surf.blit(bg, (bground.x, bground.y))
    surf.blit(bg, (bground.x1, bground.y1))
    if bground.y > h:
        bground.y = -h
    if bground.y1 > h:
        bground.y1 = -h

# drawing text on the screen
# font.match_font searches a computer's list of fonts and matches a font to one that most resembles whatever is specified.
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # the True below indicates whether the font is anti-aliased (edges smoothed) or not
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    # midtop is the position of the x, y of the font
    text_rect.midtop = (x, y)
    # so we want to blit the text onto the surface, which will usually be our screen.
    surf.blit(text_surface, text_rect)

def spawnMeteor():
    m = Meteor()
    sp_groups.all_sprites.add(m)
    sp_groups.mobs.add(m)

def explode(center, size):
    # spawning explosion
    expl = Explosion(center, size)
    sp_groups.all_sprites.add(expl)

def draw_health_bar(surf, x, y, pct):
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

def draw_shield_bar(surf, x, y, pct):
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

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_gameover_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GAME OVER", 50, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * (3/4))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # we could use pygame.KEYDOWN, but pygame.KEYUP makes sure that the player has released the "any key"
            # before starting the game
            if event.type == pygame.KEYUP:
                waiting = False


# Load all game graphics
#background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background = pygame.image.load(path.join(img_dir, "starfield1.jpg")).convert()
background_rect = background.get_rect()
#player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
#player_mini_img = pygame.transform.scale(player_img, (25, 19))
#player_mini_img.set_colorkey(BLACK)
#bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
#meteor_images = []
#meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
#               'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
#for img in meteor_list:
#    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
"""
"""
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
"""
"""
# Load all the game sounds
#shoot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Laser_Shoot4.wav'))
health_power_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow4.wav'))
gun_2shot_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow5.wav'))
gun_speed_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Randomize5.wav'))
gun_power_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Randomize6.wav'))
shield_power_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow7.wav'))
shield_down_sound = pygame.mixer.Sound(path.join(sfx_dir, 'shield_destroyed1.wav'))
missile_pow_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow1.wav'))
h_missile_pow_sound = pygame.mixer.Sound(path.join(sfx_dir, 'pow2.wav'))
expl_sounds = []
for sfx in ['Expl1.wav', 'Expl2.wav', 'Explosion1.wav', 'Explosion5.wav',
            'Explosion11.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sfx_dir, sfx)))
hit_hurt_sounds = []
for sfx in ['Hurt.wav', 'Hurt1.wav', 'Hurt2.wav', 'Hurt3.wav']:
    hit_hurt_sounds.append(pygame.mixer.Sound(path.join(sfx_dir, sfx)))
player_damage_sound = pygame.mixer.Sound(path.join(sfx_dir, 'Damaged2.wav'))
player_death_sound = pygame.mixer.Sound(path.join(sfx_dir, 'rumble1.ogg'))
#pygame.mixer.music.load(path.join(sfx_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.load(path.join(sfx_dir, 'Battle in the Stars.ogg'))

# lowers the volume of the BGM so that it's not overpowering.
pygame.mixer.music.set_volume(0.4)

# Make the below section (including the score section) into a separate function called "initGame()"!! Or maybe not...
#all_sprites = pygame.sprite.Group()
#mobs = pygame.sprite.Group()
#bullets = pygame.sprite.Group()
#powerups = pygame.sprite.Group()
player = Player()
sp_groups.all_sprites.add(player)
for i in range(40):
    spawnMeteor()

# Score
score = 0

# Background music starts before the game loop starts. loops=-1 instructs pygame to replay/loop the music
pygame.mixer.music.play(loops=-1)

# Game loop
running = True
while running:
    if game_conditions.game_over:
        show_gameover_screen()
        game_conditions.game_over = False
        game_conditions.player_dead = False
        sp_groups.all_sprites = pygame.sprite.Group()
        sp_groups.mobs = pygame.sprite.Group()
        sp_groups.bullets = pygame.sprite.Group()
        sp_groups.powerups = pygame.sprite.Group()
        player = Player()
        sp_groups.all_sprites.add(player)
        for i in range(40):
            spawnMeteor()
        # Score
        score = 0
    # keep loop running at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        #player shoots bullet
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_SPACE:
        #        player.shoot()

    # Update
    sp_groups.all_sprites.update()

    # Check to see if a bullet hit a mob
    # True, True for killing mobs AND bullets when collision occurs
    hits = pygame.sprite.groupcollide(sp_groups.mobs, sp_groups.bullets, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        # cool discovery! so groupcollide returns a dictionary, where the key is a list of the collided sprite and
        # the value is a list of the colliding sprites. So to refer to every single COLLIDING sprite, need to
        # iterate through hits[hit]
        for bullet in hits[hit]:
            hit.health -= bullet.dmg
            explode(bullet.rect.center, 'tiny')
            impactSound = random.choice(expl_sounds)
            impactSound.set_volume(0.4)
            impactSound.play()
        if hit.health <= 0:
            hit.kill()
            # smaller meteors give more points
            score += hit.radius
            # explosion sounds; edit if meteors or enemies have health
            random.choice(expl_sounds).play()
            # spawning explosion
            if hit.mtype == 'lg':
                explode(hit.rect.center, 'lg')
            elif hit.mtype == 'med':
                explode(hit.rect.center, 'med')
            elif hit.mtype == 'sm':
                explode(hit.rect.center, 'sm')
            # chance to drop power-ups. set to > 0.1 if want to test out with super high drop rate
            # > 0.88 seems to be just right
            if random.random() > 0.1:
                pow = Pow(hit.rect.center)
                sp_groups.all_sprites.add(pow)
                sp_groups.powerups.add(pow)
            # spawning new enemy
            spawnMeteor()

    # Check to see if a bullet hit a mob
    # True, True for killing mobs AND bullets when collision occurs
    hits = pygame.sprite.groupcollide(sp_groups.mobs, sp_groups.missiles, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        # cool discovery! so groupcollide returns a dictionary, where the key is a list of the collided sprite and
        # the value is a list of the colliding sprites. So to refer to every single COLLIDING sprite, need to
        # iterate through hits[hit]
        for missile in hits[hit]:
            hit.health -= missile.dmg
            explode(missile.rect.center, 'sm')
            impactSound = random.choice(expl_sounds)
            impactSound.set_volume(0.5)
            impactSound.play()
        if hit.health <= 0:
            hit.kill()
            # smaller meteors give more points
            score += hit.radius
            # explosion sounds; edit if meteors or enemies have health
            random.choice(expl_sounds).play()
            # spawning explosion
            if hit.mtype == 'lg':
                explode(hit.rect.center, 'lg')
            elif hit.mtype == 'med':
                explode(hit.rect.center, 'med')
            elif hit.mtype == 'sm':
                explode(hit.rect.center, 'sm')
            # chance to drop power-ups. set to > 0.1 if want to test out with super high drop rate
            # > 0.88 seems to be just right
            if random.random() > 0.1:
                pow = Pow(hit.rect.center)
                sp_groups.all_sprites.add(pow)
                sp_groups.powerups.add(pow)
            # spawning new enemy
            spawnMeteor()

    # Check to see if a mob hit the player
    # hits = a list of any mobs who hit the player
    hits = pygame.sprite.spritecollide(player, sp_groups.mobs, False, pygame.sprite.collide_circle)
    for hit in hits:
        if game_conditions.player_respawn_invinc:
            continue
        hit.kill()
        player.health -= hit.collision_dmg
        if hit.mtype == 'lg':
            explode(hit.rect.center, 'lg')
        elif hit.mtype == 'med':
            explode(hit.rect.center, 'med')
        elif hit.mtype == 'sm':
            explode(hit.rect.center, 'sm')
        impactSound = random.choice(expl_sounds)
        impactSound.set_volume(0.4)
        impactSound.play()
        #player_damage_sound.set_volume(0.3)
        #player_damage_sound.play()
        spawnMeteor()
        if player.health <= 0:
            game_conditions.player_dead = True
            player_death_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            sp_groups.all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.health = 100

    # Check to see if player hit a power-up
    hits = pygame.sprite.spritecollide(player, sp_groups.powerups, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit.type == 'health':
            player.health += random.randrange(10, 30)
            health_power_sound.play()
            if player.health >= 100:
                player.health = 100
        if hit.type == 'gun_2shot':
            player.gun_2shot()
            gun_2shot_sound.play()
        if hit.type == 'gun_speed':
            player.gun_speed()
            gun_speed_sound.play()
        if hit.type == 'gun_power':
            player.gun_powerup()
            gun_power_sound.set_volume(0.6)
            gun_power_sound.play()
        if hit.type == 'shield':
            if not player.force_field:
                p_shield = Shield(player)
                sp_groups.all_sprites.add(p_shield)
                sp_groups.player_shields.add(p_shield)
            shield_power_sound.play()
            player.shield()
        if hit.type == 'missile':
            player.missile_powerup()
            missile_pow_sound.play()
        if hit.type == 'h_missile':
            player.h_missile_powerup()
            h_missile_pow_sound.play()

    # reactivate the player's shield if shield down and fully regenerated
    if player.shield_health == 150 and not player.force_field:
        p_shield = Shield(player)
        sp_groups.all_sprites.add(p_shield)
        sp_groups.player_shields.add(p_shield)
        shield_power_sound.play()
        player.shield()

    # Check to see if mobs hit the player's shield
    hits = pygame.sprite.groupcollide(sp_groups.player_shields, sp_groups.mobs, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        for mob in hits[hit]:
            mob.kill()
            player.shield_health -= mob.collision_dmg
            if mob.mtype == 'lg':
                explode(mob.rect.center, 'lg')
            elif mob.mtype == 'med':
                explode(mob.rect.center, 'med')
            elif mob.mtype == 'sm':
                explode(mob.rect.center, 'sm')
            impactSound = random.choice(expl_sounds)
            impactSound.set_volume(0.4)
            impactSound.play()
        # player_damage_sound.set_volume(0.3)
        # player_damage_sound.play()
            spawnMeteor()
            if player.shield_health <= 0:
                player.shield_health = 0
                player.force_field = False
                shield_down_sound.play()
                hit.kill()
                #sp_groups.all_sprites.add(death_explosion)

    # if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        game_conditions.game_over = True

    # Draw / render
    # screen.fill is useful, but not necessary in this case, since we already have a background below
    screen.fill(BLACK)
    # blit = "copy the pixels of one thing unto another thing"
    # the screen.blit(background, background.rect) code below draws the background onto the screen
    #screen.blit(background, background_rect)
    scroll_background(screen, background, 2)
    sp_groups.all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health_bar(screen, 5, 5, player.health)
    draw_shield_bar(screen, 5, 15, player.shield_health)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # the set_caption code below displays the fps where the name of the applications should be.
    # good for checking performance
    pygame.display.set_caption("{:.2f}".format(clock.get_fps()))
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

"""