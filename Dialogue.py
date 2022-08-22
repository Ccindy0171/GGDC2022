PARA_COL = (255, 255, 255)
TITLE_COL = (200, 200, 200)


class Dialogue(pygame.sprite.Sprite):
    def __init__(self, screen, planet, idx=0):
        super().__init__()

        self.all_text = {'Earth': ['Earth.txt']}  # add all files
        self.images_dict = {'Earth': {'background': "earth-pix.png", "Surfer:": "can.png", "Rando:": "fuelcan.png"}}
        self.planet = planet
        self.line_counter = 0  # every 4 lines of a person's dialogue
        self.line_part_counter = 0  # every chunk of each person's dialogue
        self.current_file = (self.all_text[planet])[idx]
        self.output_lines = []
        self.input_lines = None
        self.screen = screen

        # set up images of speakers
        self.speaker = ""
        self.person1 = pygame.surface.Surface((self.screen.get_width(), self.screen.get_height()))
        self.person2 = pygame.surface.Surface((self.screen.get_width(), self.screen.get_height()))
        self.person1.set_colorkey((0, 255, 0))
        self.person2.set_colorkey((0, 255, 0))
        self.person1.fill((0, 255, 0))
        self.person2.fill((0, 255, 0))

        # create the text box
        self.textbox = pygame.image.load('text_box.png')
        self.textbox_img = pygame.Surface([(1700 / 1920) * screen.get_width(), (400 / 1080) * screen.get_height()],
                                          pygame.SRCALPHA)
        self.textbox_rect = self.textbox_img.get_rect()
        self.textbox_rect.topleft = ((self.screen.get_width() - self.textbox_img.get_width()) // 2,
                                     self.screen.get_height() - self.textbox_img.get_height() - 50)

        # initialize font
        self.text_size = 50 * (self.screen.get_width() / 1920)
        self.title_size = 50 * (self.screen.get_width() / 1920)
        self.text_font = pygame.font.Font('SpaceGrotesk-Medium.ttf', int(self.text_size))
        self.title_font = pygame.font.Font('SpaceGrotesk-Medium.ttf', int(self.title_size))

        self.set_up()  # prep text file
        self.bkgd_img = pygame.transform.scale(
            pygame.image.load("Images/" + str(self.images_dict[self.planet]['background'])),
            [self.screen.get_width(), self.screen.get_height()])  # load bkgd
        self.fox_img = pygame.image.load("Images/can.png")  # change 
        self.fox_img = pygame.transform.scale(self.fox_img,
                                              [int(self.fox_img.get_width() * (self.screen.get_height() / 1080)),
                                               int(self.fox_img.get_height() * (self.screen.get_height() / 1080))])

        # load all necessary characters for the planet
        for char in self.images_dict[self.planet]:
            if char != "background" and char != "Fox:":
                char_img = pygame.image.load('Images/' + self.images_dict[self.planet][char])
                char_img = pygame.transform.scale(char_img,
                                                  [int(char_img.get_width() * (self.screen.get_width() / 1920)),
                                                   int(self.fox_img.get_height() * (
                                                           self.screen.get_width() / 1080))])

                self.images_dict[self.planet].update({char: char_img})

    def set_up(self):
        # -- set up text (split by line and by hashtag/spacer) -- #
        with open(self.current_file) as file:  # open file for certain amount of time
            self.input_lines = [line.rstrip() for line in file]  # var declaration - is this a bad idea?

        for line in self.input_lines:
            # example line: "Anna:#Do I know you? I haven't#seen you before." (bigger chunks though - about 60-65 chars)
            # only 4 chunks per line - if a character says more, start a new line
            self.output_lines.append(line.split('#'))  # split the name from dialogue, + dialogue into chunks to be blit

    def setup_bg(self):
        """Call when you want to blit the background but not the text box."""
        
        self.screen.blit(self.bkgd_img, (0, 0))

    def make_font(self, words, top_left, type_num=0):
        """Render font and blit it to the screen."""

        if type_num == 0:
            text_img = self.text_font.render(words, True, PARA_COL)
        else:
            text_img = self.title_font.render(words, True, TITLE_COL)
        self.textbox_img.blit(text_img, top_left)

    def next_text(self):  # called when space bar is pressed
        """Blits speaking characters onto screen, plus speaker's name and up to 4 lines of dialogue into the text box."""

        # blit new speaking characters onto person1/2 surfaces
        if self.speaker != self.output_lines[self.line_counter][0]:  # if new speaker
            if self.output_lines[self.line_counter][0] == "Fox:":  # if new speaker is Fox
                self.person1.blit(self.fox_img, (self.screen.get_width() // 4 - self.fox_img.get_width() // 2,
                                                 int(self.screen.get_height() * 0.6) - self.fox_img.get_height()))
            else:
                self.person2.fill((0, 255, 0))  # in case there is a change in second character
                self.person2.blit(self.images_dict[self.planet][self.output_lines[self.line_counter][0]],
                                  (3 * (self.screen.get_width() // 4) - self.fox_img.get_width() // 2,
                                   int(self.screen.get_height() * 0.6) - self.fox_img.get_height()))

        # blit background and refresh textbox
        self.screen.blit(self.bkgd_img, (0, 0))
        self.textbox_img.blit(pygame.transform.scale(self.textbox, self.textbox_rect.size), (0, 0))

        # deal with text and blit it onto dialogue box
        if self.line_counter >= len(self.output_lines):  # if no more lines
            self.screen.blit(self.bkgd_img, (0, 0))  # change this if needed (to 'passed == True'? - add passed as a var)
        else:
            self.make_font(self.output_lines[self.line_counter][0], (40, 20), 1)  # blit the character name
            self.speaker = self.output_lines[self.line_counter][0]
            for i in range(4):  # then blit up to 4 lines of text
                if len(self.output_lines[self.line_counter]) > (i + 1):
                    self.make_font(self.output_lines[self.line_counter][i + 1],
                                   (40, int(125*self.screen.get_height()//1080 + 1.2 * (self.text_size * i))))
            self.line_counter += 1

            # blit character images
            if self.speaker == "Fox:":
                self.screen.blit(self.person1, (0, 0))
                self.screen.blit(self.person2, (0, 50))
            else:
                self.screen.blit(self.person2, (0, 0))
                self.screen.blit(self.person1, (0, 50))

            # finally, blit textbox
            self.screen.blit(self.textbox_img, self.textbox_rect)

    def switch_dialogue(self, planet, idx):
        """Refreshes all variables to prepare for alternate dialogue."""
        
        self.line_counter = 0
        self.line_part_counter = 0
        self.current_file = (self.all_text[planet])[idx]
        self.output_lines = []
        self.input_lines = None
        self.speaker = ""

        self.set_up()
        
