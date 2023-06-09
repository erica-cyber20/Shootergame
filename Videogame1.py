import pygame
# import os
import glob
import random
import csv

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * .80)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

# set frame rate  - how fast the game will run
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
# TILE_SIZE = 40
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21

screen_scroll = 0
bg_scroll = 0
level = 1

# define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# load images
pine1_img = pygame.image.load('Shooter-main/img/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('Shooter-main/img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('Shooter-main/img/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('Shooter-main/img/background/sky_cloud.png').convert_alpha()
# store tiles in the list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Shooter-main/img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# bullet
bullet_img = pygame.image.load('png/icons/bullet.png').convert_alpha()

# grenade
grenade_img = pygame.image.load('png/icons/grenade.png').convert_alpha()

# pick up boxes
health_box_img = pygame.image.load('png/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('png/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('png/icons/grenade_box.png').convert_alpha()

item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img,

}
# define colors (Background)
BG = (160, 144, 190)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# define font
font = pygame.font.SysFont('Futura', 20)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    screen.blit(sky_img, (0, 0))
    screen.blit(mountain_img, (0, SCREEN_HEIGHT- mountain_img.get_height() - 300))
    screen.blit(pine1_img, (0, SCREEN_HEIGHT - pine1_img.get_height() - 150))
    screen.blit(pine2_img, (0, SCREEN_HEIGHT - pine2_img.get_height()))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1  # determine if player is looking to the right or left
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False  # determine if player is looking to the right or left
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            # num_of_frames = len(#os.listdir(f'png/{self.char_type}/{animation}'))
            num_of_frames = len(glob.glob(f"png/{self.char_type}/{animation}/*.png"))
            # print(num_of_frames)
            for i in range(num_of_frames):
                img = pygame.image.load(f'png/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset moving variable

        screen_scroll = 0
        dx = 0  # delta x
        dy = 0  # delta y - means the change in x and y

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check for collision
        for tile in world.obstacle_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if self.char_type == 'player':
            if player.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0


        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # screen scroll opposite of the player.
        if self.char_type == 'player':
            if (player.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (player.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
            #if self.rect.right > (screen_width - SCROLL_THRESH) or self.rect.left < SCROLL_THRESH:
                 #self.rect.x -= dx
                 #screen_scroll = -dx

        return screen_scroll

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0 : False
                self.idling = True
                self.idling_counter = 50
            # check if ai is near the player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)  # 0: idle
                # shoot the player
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1 :ai run
                    self.move_counter += 1
                    # update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since hte last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(
                    self.animation_list[self.action]) - 1  # if person dies, don't reset to move again
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:  # if new action is different than the current action, then update the action
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # runs the player death animation

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)

                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Soldier('player1', x * TILE_SIZE, y * TILE_SIZE, 8, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, .7, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # create item boxes
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # create item boxes
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # create item boxes
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]  # load different types of item images
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # check if player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check the kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            # delete item box
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate haelth ratio
        ratio = self.health / self.max_health

        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullet has gone off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    # print(enemy.health)
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100  # timer for when grenade will blow up.
        self.vel_y = -11  # throwing the grenade in the air and landing on the ground
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # check for collsion with level
        for tile in world.obstacle_list:
            # check if grenade has gone off-screen ( with walls)
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        """"
        # check collision of grenade with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0"""

        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # countdown timer for grenade explosion
        self.timer -= 1
        if self.timer <= 0:
            # make grenade disappear
            self.kill()
            # start the explosion
            explosion = Explosion(self.rect.x, self.rect.y, 1.5)
            explosion_group.add(explosion)

            # do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'png/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4  # define speed at which animation will run
        self.counter += 1  # update explosion animation

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete, then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


# create sprite groups for bullets, grenades, explosions, enemies
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# load in level data and create world

with open(f'Shooter-main/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)

""""
x = 200
y = 200
scale = 4
"""
run = True
while run:

    clock.tick(FPS)

    # update background
    draw_bg()
    # draw world map
    world.draw()

    # show player health
    health_bar.draw(player.health)

    # show ammo
    draw_text('AMMO: ', font, WHITE, 10, 35)
    for x in range(player.ammo):
        screen.blit(bullet_img, (90 + (x * 10), 40))

    # show grenades
    draw_text('GRENADES: ', font, WHITE, 10, 60)
    for x in range(player.grenades):
        screen.blit(grenade_img, (130 + (x * 15), 60))

    player.update()
    player.draw()
    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()

    # update and draw groups
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()
    decoration_group.update()
    water_group.update()
    exit_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)
    decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)

    # update player actions
    if player.alive:
        # shoot bullets
        if shoot:
            player.shoot()
        # throw grenades
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), \
                              player.rect.top, player.direction)
            grenade_group.add(grenade)
            # reduce grenades when thrown
            player.grenades -= 1
            grenade_thrown = True
        if player.in_air:
            player.update_action(2)  # 2 means Jump
        elif moving_left or moving_right:
            player.update_action(1)  # 0 means Idle, 1 means Run
        else:
            player.update_action(0)
        screen_scroll = player.move(moving_left, moving_right)

        print(screen_scroll)

    for event in pygame.event.get():
        # quit game

        if event.type == pygame.QUIT:
            run = False
        # keyboard presses to control player movement
        if event.type == pygame.KEYDOWN:  # press down on any key
            if event.key == pygame.K_a:  # press the 'a' keyboard button to move left
                moving_left = True
            if event.key == pygame.K_d:  # press the 'd' keyboard button to move right
                moving_right = True
            if event.key == pygame.K_SPACE:  # press the 'spacebar' keyboard button to shoot
                shoot = True
            if event.key == pygame.K_q:  # press the 'q' keyboard button to throw grenade
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:  # press escape to exit the game
                run = False

        # release button on keyboard
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()
