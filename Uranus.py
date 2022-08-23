import pygame

BACKGROUND = (194, 215, 226)  # bluish white snow
ALPHA_COL = (255, 0, 0)  # not in anything, to be turned transparent

# Image loading and other misc stuff
START_RAD = 15   # starting radius of snowballs
BALL_IMG_OFF = pygame.transform.scale(pygame.image.load("Images/snowball.png"), (START_RAD*2, START_RAD*2))
BALL_IMG_ON = pygame.transform.scale(pygame.image.load("Images/snowball_blue.png"), (START_RAD*2, START_RAD*2))
TILES_X = 18  # num of tiles on x axis
TILES_Y = 10  # num of tiles on y axis
TILE_SPACING = 2  # pixels between tiles


class Lvl(object):
    def __init__(self, screen):
        # level stuff
        self.level_num = 0  # which level to start at (0-2)
        self.snowman_step = 0  # how many parts completed
        self.rewind = False  # for redoing a level
        self.is_passed = False
        self.next_type = "Dialogue"
        self.next_info = "Uranus"  # ----------- add index !! ---------------
        
        self.screen = screen
        self.current_level_stuff = None
        self.current_snowman = pygame.sprite.Group()
        self.current_objects = pygame.sprite.Group()
        self.key_lock = False

        # tile stuff
        self.tiles_w = self.screen.get_width() // TILES_X - TILE_SPACING  # tile width
        self.tiles_h = self.screen.get_height() // TILES_Y - TILE_SPACING  # tile height
        self.dirt_img = pygame.transform.scale(pygame.image.load("Images/path_tile.png"), (self.tiles_w, self.tiles_h))
        self.tiles_path = pygame.sprite.Group()  # dirt tiles, non collideable
        self.tiles_snow = pygame.sprite.Group()  # snow tiles, collideable
        self.tiles_snow_like = pygame.sprite.Group()  # snow-looking tiles, non collideable
        self.tiles_path_like = pygame.sprite.Group()  # dirt-looking tiles, but collideable

        # snowball stuff
        self.snowballs = pygame.sprite.Group()
        self.snowballs_list = []  # in order of big-medium-small
        self.ball_tiles_list = []  # tiles that snowballs are on
        self.first_ball = None   # which ball to select first
        self.current_ball = None   # which ball is currently selected

        # snowman stuff
        self.big_ball_rad = [55, 75]   # min/max radius of bottom ball on snowman
        self.med_ball_rad = [40, 55]   # min/max rad of second ball
        self.small_ball_rad = [25, 40]   # min/max rad of top ball

        # Level 1
        self.snowman_tile1 = [[10, 3]]   # tile that snowman is on
        self.rock_tiles1 = [[4, 8], [6, 8], [7, 7], [8, 8], [9, 8], [10, 8], [11, 7], [10, 4], [9, 5],
                            [14, 3], [14, 4], [13, 2],
                            [1, 3], [2, 3], [1, 4], [2, 2]]   # tile(s) that rocks are on
        self.ball_tiles_list1 = [[7, 9], [15, 6], [5, 2]]   # tiles that snowballs start on
        self.level1_stuff = [['snowball', self.ball_tiles_list1], ['snowman', self.snowman_tile1], ['rock', self.rock_tiles1]]

        # level 2
        self.snowman_tile2 = [[16, 3]]
        self.rock_tiles2 = [[8, 4], [9, 4], [10, 4], [11, 5], [12, 4], [8, 3],
                            [10, 6], [11, 6], [9, 8], [9, 9], [10, 8], [6, 7], [10, 1], [11, 1],
                            [15, 5], [16, 6],
                            [2, 2], [2, 1], [1, 3], [12, 0]]
        self.ball_tiles_list2 = [[3, 2], [5, 3], [15, 6]]
        self.level2_stuff = [['snowball', self.ball_tiles_list2], ['snowman', self.snowman_tile2], ['rock', self.rock_tiles2]]

        # level 3
        self.snowman_tile3 = [[3, 3]]
        self.rock_tiles3 = [[13, 1], [13, 2], [12, 2], [11, 3], [11, 4], [9, 4], [8, 5], [8, 6], [7, 8], [9, 7],
                            [8, 4], [10, 7], [12, 0], [11, 1], [10, 1],
                            [5, 6], [5, 5], [6, 4], [4, 6],
                            [4, 2], [3, 2],
                            [16, 6], [16, 7], [14, 8], [13, 8], [14, 6], [15, 5], [16, 5]]
        self.ball_tiles_list3 = [[13, 3], [8, 8], [5, 2]]
        self.level3_stuff = [['snowball', self.ball_tiles_list3], ['snowman', self.snowman_tile3], ['rock', self.rock_tiles3]]

        self.level_start()

    def run(self):
        for event in pygame.event.get():  # event handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.QUIT:
                    pygame.quit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    self.key_down(event)

        if self.level_num > 3 or self.is_passed:
            return False

        self.update()
        self.screen.fill(BACKGROUND)
        self.display()

        if self.rewind:  # restarts the level
            self.rewind = False
            if self.level_num > 0:
                self.level_num -= 1
                self.level_start()
        return True

    def level_start(self):
        # level stuff
        self.level_num += 1
        self.snowman_step = 0

        # object stuff
        self.current_snowman.empty()
        self.current_objects.empty()

        # tile stuff
        self.tiles_path.empty()
        self.tiles_snow.empty()
        self.tiles_snow_like.empty()
        self.tiles_path_like.empty()
        self.ball_tiles_list = []

        self.generate_tiles()

        # snowball stuff
        self.snowballs.empty()
        self.snowballs_list = []

        self.level_setup()

    def level_setup(self):
        """Set up variables and objects for the current level."""
        if self.level_num == 1:
            self.current_level_stuff = self.level1_stuff
            self.ball_tiles_list = self.ball_tiles_list1
        elif self.level_num == 2:
            self.current_level_stuff = self.level2_stuff
            self.ball_tiles_list = self.ball_tiles_list2
        elif self.level_num == 3:
            self.current_level_stuff = self.level3_stuff
            self.ball_tiles_list = self.ball_tiles_list3

        # make all the snowballs
        for tile in self.ball_tiles_list:
            ball = SnowBall(self, tile)
            self.snowballs.add(ball)
            self.snowballs_list.append(ball)

        # make the selected ball a special colour
        self.current_ball = self.snowballs_list[0]
        self.current_ball.image = pygame.transform.scale(BALL_IMG_ON, (self.current_ball.radius*2, self.current_ball.radius*2))

        # make current level things (rocks, snowman)
        for thing in self.current_level_stuff:
            for tile in thing[1]:
                # make snowman
                if thing[0] == 'snowman':
                    sprite = Object(self, tile, 'snowman')
                    self.current_snowman.add(sprite)
                    self.current_objects.add(sprite)
                if thing[0] == 'rock':
                    # make rock(s)
                    sprite = Object(self, tile, 'rock')
                    self.current_objects.add(sprite)

    def generate_tiles(self):
        """Create all the tile sprites using the Tile class."""
        for i in range(TILES_Y):
            for j in range(TILES_X):
                tile = Tile(self, self.tiles_w * j + TILE_SPACING / 2 + TILE_SPACING * j, self.tiles_h * i +
                            TILE_SPACING / 2 + TILE_SPACING * i, self.tiles_w, self.tiles_h, [j, i])
                self.tiles_snow.add(tile)

    def check_ball_completed(self):
        """Handle what happens when the snowball reaches the snowman's tile, and the player
        presses the space bar."""
        # sets up conditions for each of the snowman's balls
        big_ball_complete = (self.snowman_step == 0 and self.big_ball_rad[0] < self.current_ball.radius <
                             self.big_ball_rad[1] and self.current_ball.current_tile_id == self.current_level_stuff[1][
                                 1][0])
        med_ball_complete = (self.snowman_step == 1 and self.med_ball_rad[0] < self.current_ball.radius <
                             self.med_ball_rad[1] and self.current_ball.current_tile_id == self.current_level_stuff[1][
                                 1][0])
        small_ball_complete = (self.snowman_step == 2 and self.small_ball_rad[0] < self.current_ball.radius <
                               self.small_ball_rad[1] and self.current_ball.current_tile_id == self.current_level_stuff[
                                   1][1][0])

        if big_ball_complete or med_ball_complete or small_ball_complete or self.snowman_step == 3:
        # if True:   # SWITCH FOR TESTING
            for snowman in self.current_snowman:
                if hasattr(snowman, 'progress'):  # just making sure
                    # update the snowman's image and/or go to the next level
                    snowman.progress()
            for tile in self.tiles_path_like:
                if tile.tile_ID == self.current_level_stuff[1][1][0]:
                    # make the snowman's tile fresh snow (so the next ball can roll on it)
                    self.tiles_path_like.remove(tile)
                    self.tiles_snow.add(tile)

            # switch the selected snowball to the next on the list and remove the current ball
            self.switch_balls()

    def switch_balls(self):
        """Switch the selected snowball to the next on the list."""
        # find the current ball on the list and get the next one
        self.current_ball.image = pygame.transform.scale(BALL_IMG_OFF, (self.current_ball.radius*2,
                                                                        self.current_ball.radius*2))
        if self.current_ball not in self.snowballs_list:
            self.is_passed = True
            return None
        if self.snowman_step != 0:  # remove finished snowball
            self.snowballs_list.remove(self.current_ball)
            self.current_ball.kill()
        if self.snowballs_list:
            self.current_ball = self.snowballs_list[0]    # switch current ball
        self.current_ball.image = pygame.transform.scale(BALL_IMG_ON, (self.current_ball.radius*2, self.current_ball.radius*2))

    def key_down(self, event):
        """Handle movement and actions done using keys."""
        if not self.key_lock:
            if event.key == pygame.K_LEFT:
                result = self.current_ball.check_surrounding_tiles("L")
                if result is not None:
                    self.current_ball.go_left = True
                    self.key_lock = True
            if event.key == pygame.K_RIGHT:
                result = self.current_ball.check_surrounding_tiles("R")
                if result is not None:
                    self.current_ball.go_right = True
                    self.key_lock = True
            if event.key == pygame.K_DOWN:
                result = self.current_ball.check_surrounding_tiles("D")
                if result is not None:
                    self.current_ball.go_down = True
                    self.key_lock = True
            if event.key == pygame.K_UP:
                result = self.current_ball.check_surrounding_tiles("U")
                if result is not None:
                    self.current_ball.go_up = True
                    self.key_lock = True
            if event.key == pygame.K_SPACE:
                self.check_ball_completed()
            if event.key == pygame.K_d:
                self.rewind = True

    def update(self):
        """Update things in the level (only the snowballs, nothing else moves)."""
        self.snowballs.update()

    def display(self):
        """Blit dirt tiles, objects, and snowballs onto the screen."""
        for tile in self.tiles_path:
            self.screen.blit(tile.image, tile.rect)
        for tile in self.tiles_path_like:
            self.screen.blit(tile.image, tile.rect)
        for thing in self.current_objects:
            if hasattr(thing, 'type'):  # just making sure
                if not thing.type == 'snowman':
                    self.screen.blit(thing.image, thing.rect)
        for thing in self.current_objects:
            if hasattr(thing, 'type'):  # just making sure
                if thing.type == 'snowman':
                    self.screen.blit(thing.image, thing.rect)
        for ball in self.snowballs:
            if not ball == self.current_ball:
                self.screen.blit(ball.image, ball.rect)
        for ball in self.snowballs:  # currently selected one always on top
            if ball == self.current_ball:
                self.screen.blit(ball.image, ball.rect)


class Tile(pygame.sprite.Sprite):
    def __init__(self, level, left, top, width, height, tile_id):
        super().__init__()

        self.level = level
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)
        self.tile_ID = tile_id
        self.ball_bottom = self.rect.bottom - self.rect.height // 5   # sets position for objects

    def make_path(self):
        self.image = self.level.dirt_img


class SnowBall(pygame.sprite.Sprite):
    def __init__(self, level, start_coords):
        super().__init__()

        # constants for later
        self.level = level
        self.distance = 0

        # find starting tile
        self.start_tile_id = start_coords
        self.start_tile = None

        for tile in self.level.tiles_snow:
            if tile.tile_ID == self.start_tile_id:
                self.start_tile = tile
                self.level.tiles_snow.remove(tile)
                if tile in self.level.tiles_snow:
                    self.level.tiles_snow.remove(tile)
                tile.make_path()   # make the snowball's starting tiles into path like tiles
                self.level.tiles_path_like.add(tile)

        # variables for toggled movement
        self.go_up = False
        self.go_down = False
        self.go_left = False
        self.go_right = False
        self.current_tile = None
        self.current_tile_id = self.start_tile_id
        # tiles directly up, down, left, right of current tile
        self.up_tile = None
        self.down_tile = None
        self.left_tile = None
        self.right_tile = None

        # set up snowball image and rect
        self.radius = START_RAD
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(ALPHA_COL)
        self.image.set_colorkey(ALPHA_COL)
        self.rect = self.image.get_rect()
        self.rect.bottom = self.start_tile.ball_bottom
        self.rect.centerx = self.start_tile.rect.centerx

        self.on = False   # basically None, stores the snowball's colour (selected/not)
        self.image = pygame.transform.scale(BALL_IMG_OFF, (self.radius*2, self.radius*2))

        # sets how fast the ball grows as it moves (smaller num is faster)
        self.change_size_speed = 30

        # set speed vector for ball (bigger is faster)
        self.speed = 4

    def check_surrounding_tiles(self, direction):
        """Find the closest left, right, up, down tiles."""
        for tile in self.level.tiles_snow:
            if direction == "L":   # closest left tile
                if tile.tile_ID == [self.current_tile_id[0] - 1, self.current_tile_id[1]]:
                    self.left_tile = tile
                    return self.left_tile
                else:
                    self.left_tile = None
            if direction == "R":   # closest right tile
                if tile.tile_ID == [self.current_tile_id[0] + 1, self.current_tile_id[1]]:
                    self.right_tile = tile
                    return self.right_tile
                else:
                    self.right_tile = None
            if direction == "U":   # closest up tile
                if tile.tile_ID == [self.current_tile_id[0], self.current_tile_id[1] - 1]:
                    self.up_tile = tile
                    return self.up_tile
                else:
                    self.up_tile = None
            if direction == "D":   # closest down tile
                if tile.tile_ID == [self.current_tile_id[0], self.current_tile_id[1] + 1]:
                    self.down_tile = tile
                    return self.down_tile
                else:
                    self.down_tile = None

    def fix_ball_pos(self, next_tile, xy):
        """Finish movement by forcing the ball to be in position at the next tile."""
        if xy == "y":   # if moving on the y axis
            # check if near proper position
            if next_tile.ball_bottom + 5 > self.rect.bottom > next_tile.ball_bottom - 5:
                self.rect.bottom = next_tile.ball_bottom  # snap into position
                next_tile.make_path()  # fill with colour but don't make non-collideable
                self.level.key_lock = False   # let player press next key

                self.level.tiles_snow.remove(self.current_tile)
                self.current_tile.make_path()  # make old tile non-collideable
                self.level.tiles_path.add(self.current_tile)
                return True
            else:
                return False
        elif xy == "x":   # if moving on x axis
            if next_tile.rect.centerx + 5 > self.rect.centerx > next_tile.rect.centerx - 5:
                self.rect.centerx = next_tile.rect.centerx
                next_tile.make_path()
                self.level.key_lock = False

                self.level.tiles_snow.remove(self.current_tile)
                self.current_tile.make_path()  # make old tile non-collideable
                self.level.tiles_path.add(self.current_tile)
                return True
            else:
                return False

    def move(self):
        """Move the ball to the next tile."""
        for tile in self.level.tiles_path_like:
            if tile.tile_ID == self.current_tile_id:
                self.current_tile = tile   # store current tile for use

        # check if next tile, then move ball towards next tile
        if self.go_up or self.go_down or self.go_left or self.go_right:
            # move up if tile available
            if self.go_up and self.up_tile:
                self.rect.y -= self.speed
                self.distance += self.speed

                if self.fix_ball_pos(self.up_tile, "y"):  # if ball reaches end position
                    self.go_up = False   # stop moving up
                    self.level.tiles_path_like.remove(self.current_tile)
                    self.level.tiles_path.add(self.current_tile)
                    self.current_tile_id = self.up_tile.tile_ID   # update current tile
                    self.level.tiles_snow.remove(self.up_tile)
                    self.up_tile.make_path()
                    self.level.tiles_path_like.add(self.up_tile)

            # move down if tile available
            if self.go_down and self.down_tile:
                self.rect.y += self.speed
                self.distance += self.speed

                if self.fix_ball_pos(self.down_tile, "y"):
                    self.go_down = False
                    self.level.tiles_path_like.remove(self.current_tile)
                    self.level.tiles_path.add(self.current_tile)
                    self.current_tile_id = self.down_tile.tile_ID  # update current tile
                    self.level.tiles_snow.remove(self.down_tile)
                    self.down_tile.make_path()
                    self.level.tiles_path_like.add(self.down_tile)

            # move left if tile available
            if self.go_left and self.left_tile:
                self.rect.x -= self.speed
                self.distance += self.speed

                if self.fix_ball_pos(self.left_tile, "x"):
                    self.go_left = False
                    self.level.tiles_path_like.remove(self.current_tile)
                    self.level.tiles_path.add(self.current_tile)
                    self.current_tile_id = self.left_tile.tile_ID  # update current tile
                    self.level.tiles_snow.remove(self.left_tile)
                    self.left_tile.make_path()
                    self.level.tiles_path_like.add(self.left_tile)

            # move right if tile available
            if self.go_right and self.right_tile:
                self.rect.x += self.speed
                self.distance += self.speed

                if self.fix_ball_pos(self.right_tile, "x"):
                    self.go_right = False
                    self.level.tiles_path_like.remove(self.current_tile)
                    self.level.tiles_path.add(self.current_tile)
                    self.current_tile_id = self.right_tile.tile_ID  # update current tile
                    self.level.tiles_snow.remove(self.right_tile)
                    self.right_tile.make_path()
                    self.level.tiles_path_like.add(self.right_tile)

            return True
        else:
            return False

    def update(self):
        """Select/deselect snowball and move/change size if necessary."""
        if self.level.current_ball == self:
            self.on = True
            moved = self.move()
            self.change_size(moved)
        else:
            self.on = False

    def change_size(self, moved):
        """Update snowball's size if moved. Can also shrink the ball (not fully coded)."""
        if moved:
            # update radius based on distance travelled
            self.radius = START_RAD + round(self.distance / self.change_size_speed)

        center = self.rect.center   # store current rect positions
        ball_bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.center = center   # re-position rect
        self.rect.bottom = ball_bottom

        if self.on:
            self.image = pygame.transform.scale(BALL_IMG_ON, (self.radius*2, self.radius*2))
        elif not self.on:
            self.image = pygame.transform.scale(BALL_IMG_OFF, (self.radius*2, self.radius*2))


class Object(pygame.sprite.Sprite):
    def __init__(self, level, object_tile, object_type):
        super().__init__()

        self.level = level
        self.current_tile = None
        self.type = object_type

        images_dict = {'snowman': "snowman-step0.png", 'rock': 'Images/rock_small.png'}
        self.image = pygame.image.load(images_dict[object_type])  # load correct image file
        if object_type == 'snowman':   # transform images to correct size
            self.image = pygame.transform.scale(self.image, [26*5, 60*5])
        if object_type == 'rock':
            self.image = pygame.transform.scale(self.image, [32*2, 32*2])

        self.rect = self.image.get_rect()
        for tile in level.tiles_snow:
            if tile.tile_ID == object_tile:
                self.rect.bottom = tile.ball_bottom   # position object on tile
                self.rect.centerx = tile.rect.centerx
                self.current_tile = tile
                # extra stuff for each type of object
                if object_type == 'rock':   # make rock non-collideable but on snow (not brown)
                    self.level.tiles_snow.remove(tile)
                    self.level.tiles_snow_like.add(tile)

    def progress(self):
        """Handle completion of a step of making the snowman (change image, pass level if step 3)."""
        if self.level.snowman_step < 3:
            self.level.snowman_step += 1
            current_xy = self.rect.topleft   # store current position
            self.image = pygame.transform.scale(pygame.image.load('snowman-step' +   # load new image
                                                                  str(self.level.snowman_step) +
                                                                  '.png'), [26*5, 60*5])
            self.rect = self.image.get_rect()
            self.rect.topleft = current_xy   # restore position
        elif self.level.snowman_step == 3 and self.level.level_num < 3:
            self.level.level_start()
