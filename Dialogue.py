import pygame as pygame

PARA_COL = (255, 255, 255)
TITLE_COL = (200, 200, 200)


class Dialogue(pygame.sprite.Sprite):
    def __init__(self, screen, planet, idx=0):
        super().__init__()

        self.all_text = {'Earth': ['Earth.txt']}  # add all files
        self.line_counter = 0   # every 4 lines of a person's dialogue
        self.line_part_counter = 0   # every chunk of each person's dialogue
        self.current_file = (self.all_text[planet])[idx]
        self.output_lines = []
        self.input_lines = None
        self.screen = screen

        # create the text box
        self.textbox = pygame.image.load('text_box.png')
        self.image = pygame.Surface([(1700/1920)*screen.get_width(), (400/1080)*screen.get_height()], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((self.screen.get_width() - self.image.get_width())//2, self.screen.get_height() -
                             self.image.get_height() - 50)

        # initialize font
        self.font_size = 50*(self.screen.get_width()/1920)
        self.font = pygame.font.Font('SpaceGrotesk-Medium.ttf', int(self.font_size))

        self.set_up()  # prep text file

    def set_up(self):
        # -- set up text (split by line and by hashtag/spacer) -- #
        with open(self.current_file) as file:  # open file for certain amount of time
            self.input_lines = [line.rstrip() for line in file]  # var declaration - is this a bad idea?

        for line in self.input_lines:
            # example line: "Anna:#Do I know you? I haven't#seen you before." (bigger chunks though - about 60-65 chars)
            # only 4 chunks per line - if a character says more, start a new line
            self.output_lines.append(line.split('#'))  # split the name from dialogue, + dialogue into chunks to be blit

    def make_font(self, words, top_left, type_num=0):
        """Render font and blit it to the screen."""
        if type_num == 0:
            text_img = self.font.render(words, True, PARA_COL)
        else:
            text_img = self.font.render(words, True, TITLE_COL)
        self.image.blit(text_img, top_left)

    def next_text(self):  # called when space bar is pressed
        """Blits a character name and up to 4 lines of dialogue into the text box."""

        self.image.blit(pygame.transform.scale(self.textbox, self.rect.size), (0, 0))
        if self.line_counter >= len(self.output_lines):  # if no more lines
            self.kill()  # doesn't really work, idk how to get rid of the dialogue box once done
        else:
            self.make_font(self.output_lines[self.line_counter][0], (40, 20), 1)  # blit the character name
            for i in range(4):  # then blit up to 4 lines of text
                if len(self.output_lines[self.line_counter]) > (i + 1):
                    self.make_font(self.output_lines[self.line_counter][i+1], (40, int(80 + 1.2*(self.font_size*i))))
            self.line_counter += 1
            self.screen.blit(self.image, self.rect)  # make everything show up

    def switch_dialogue(self, planet, idx):
        self.line_counter = 0
        self.line_part_counter = 0
        self.current_file = (self.all_text[planet])[idx]
        self.output_lines = []
        self.input_lines = None

        self.set_up()
