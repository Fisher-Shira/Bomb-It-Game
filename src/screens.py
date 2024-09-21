from pygame import display, draw, image, init
from src.squares import Squares
from src.color import Color

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WHITE = (255, 255, 255)
PLAYERS2_POS = (478, 121, 163, 44)
PLAYERS4_POS = (478, 212, 163, 44)
INS_POS = (476, 303, 167, 43)
BACK_INS_POS = (501, 42, 167, 44)
BACK_END_POS = (27, 419, 183, 40)


class Screens:
    def __init__(self):
        init()
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = display.set_mode(size)
        display.set_caption("Game")
        self.screen = screen  # the screen

    def show_open(self):
        # show the open screen
        # return the 2 players button, 4 players button, instruction button
        players2_button = draw.rect(self.screen, WHITE, PLAYERS2_POS)
        players4_button = draw.rect(self.screen, WHITE, PLAYERS4_POS)
        ins_button = draw.rect(self.screen, WHITE, INS_POS)
        img = image.load('src/Images/Main_Screens/open.jpg').convert()
        self.screen.blit(img, (0, 0))
        display.flip()
        return players2_button, players4_button, ins_button

    def show_inc(self):
        # show the instruction screen
        # return the back button
        back_button = draw.rect(self.screen, WHITE, BACK_INS_POS)
        img = image.load('src/Images/Main_Screens/instructions.jpg').convert()
        self.screen.blit(img, (0, 0))
        display.flip()
        return back_button

    def show_players(self, x_arrow, taken_colors):
        # show the players screen
        players_img = image.load('src/Images/Select_Players/players.jpg'
                                 ).convert()
        self.screen.blit(players_img, (0, 0))
        arrow_pic = image.load('src/Images/Select_Players/arrow.png').convert()
        arrow_pic.set_colorkey(WHITE)
        self.screen.blit(arrow_pic, (x_arrow, 50))
        self.show_taken(taken_colors)
        display.flip()

    def show_your_player(self, x_pic):
        # show "you" next to your selected player
        you_img = image.load('src/Images/Select_Players/you.png').convert()
        you_img.set_colorkey(WHITE)
        self.screen.blit(you_img, (x_pic, 262))
        display.flip()

    def show_taken(self, color_list):
        # show "taken" next to the colors that has been taken
        taken_img = image.load('src/Images/Select_Players/taken.png').convert()
        taken_img.set_colorkey(WHITE)
        for color in color_list:
            self.screen.blit(taken_img, (Color.select_pos[color], 262))
        display.flip()

    def show_game(self, current_player, players_colors):
        # show the start game screen
        # return the players_position list
        game_img = image.load('src/Images/Lives/hearts.jpg').convert()
        self.screen.blit(game_img, (0, 0))
        self.show_you(current_player)
        players_position = {}
        for color in players_colors:
            players_position[color] = ((Color.start_column[color],
                                        Color.start_raw[color]), "d")
            self.present_hearts(color, 3)
        self.present_game_board(players_position, {}, {})
        return players_position

    def show_you(self, player):
        # show "you" next to your player hearts_picture
        you_img = image.load('src/Images/Lives/you.png').convert()
        you_img.set_colorkey(WHITE)
        color = player.color
        self.screen.blit(you_img, (0, Color.select_pos[color] - 134))
        display.flip()

    def ij_to_xy(self, thing, ij_tuple):
        # change i_j tuple to x_y tuple and return it
        if thing == 'player':
            x = 192 + ij_tuple[0]*30
            y = ij_tuple[1]*30 - 20
        elif thing == 'explosion':
            x = 165 + ij_tuple[0]*30
            y = ij_tuple[1]*30 - 33
        else:  # bomb/ block/ clear (no changes)
            x = 195 + ij_tuple[0]*30
            y = ij_tuple[1]*30 - 3
        tup = (x, y)
        return tup

    def present_game_board(self, players_position, bombs_position,
                           explosions_position):
        # present the new picture of the board
        # board, big, bombs, explosions, players
        clear_squares = Squares.clear_squares
        game_img = image.load('src/Images/Board/game.jpg').convert()
        self.screen.blit(game_img, (200, 0))
        middle_img = image.load('src/Images/Board/statue.png').convert()
        middle_img.set_colorkey(WHITE)
        clear_img = image.load('src/Images/Board/clear.jpg').convert()
        if len(clear_squares) > 62:  # present the new clean squares
            for i in range(62, len(clear_squares)):
                self.screen.blit(clear_img, self.ij_to_xy('clear',
                                                          clear_squares[i]))
        self.present_explosions(explosions_position)
        self.screen.blit(middle_img, (439, 200))  # present the middle picture
        self.present_players(players_position)
        self.present_bombs(bombs_position)
        display.flip()

    def present_hearts(self, color, hearts):
        # present hearts/ place/ exit
        if hearts == 200:
            hearts_img = image.load('src/Images/Lives/quit.jpg').convert()
        elif hearts == 1 or hearts == 2 or hearts == 3:
            hearts_img = image.load(('src/Images/Lives/' + str(hearts)
                                     + '_hearts.jpg')).convert()
        else:
            hearts_img = image.load(('src/Images/Results/' + str(hearts-100)
                                     + '_place.jpg')).convert()
        self.screen.blit(hearts_img, (42, Color.y_hearts[color]))
        display.flip()

    def present_players(self, players_position):
        for player in players_position.keys():
            color_img = ('src/Images/Players/' + player + '_' +
                         players_position[player][1] + '.png')
            player_img = image.load(color_img).convert()
            player_img.set_colorkey(WHITE)
            self.screen.blit(player_img, self.ij_to_xy(
                'player', players_position[player][0]))

    def present_explosions(self, explosions_position):
        block_squares = Squares.block_squares
        brick_img = image.load('src/Images/Board/brick.jpg').convert()
        explosion_img = image.load('src/Images/Board/explosion.png').convert()
        explosion_img.set_colorkey(WHITE)
        for time in explosions_position:  # present the explosions
            explosion_ij = explosions_position[time][0]
            self.screen.blit(explosion_img, self.ij_to_xy('explosion',
                                                          explosion_ij))
            if (explosion_ij[0]-1, explosion_ij[1]) in block_squares:
                self.screen.blit(brick_img, self.ij_to_xy('block',
                                                          (explosion_ij[0]-1,
                                                           explosion_ij[1])))
            if (explosion_ij[0]+1, explosion_ij[1]) in block_squares:
                self.screen.blit(brick_img, self.ij_to_xy('block',
                                                          (explosion_ij[0]+1,
                                                           explosion_ij[1])))
            if (explosion_ij[0], explosion_ij[1]-1) in block_squares:
                self.screen.blit(brick_img, self.ij_to_xy('block',
                                                          (explosion_ij[0],
                                                           explosion_ij[1]-1)))
            if (explosion_ij[0], explosion_ij[1]+1) in block_squares:
                self.screen.blit(brick_img, self.ij_to_xy('block',
                                                          (explosion_ij[0],
                                                           explosion_ij[1]+1)))

    def present_bombs(self, bombs_position):
        bomb_img = image.load('src/Images/Board/bomb.png').convert()
        bomb_img.set_colorkey(WHITE)
        for time in bombs_position:
            self.screen.blit(bomb_img, self.ij_to_xy(
                'bomb', bombs_position[time]))

    def show_end(self, place):
        # show the end screen
        # return the back button
        back_button = draw.rect(self.screen, (0, 0, 0), BACK_END_POS)
        img = image.load('src/Images/Results/end.jpg').convert()
        self.screen.blit(img, (0, 0))
        img = image.load(('src/Images/Results/end_' + str(place)
                          + ".png")).convert()
        img.set_colorkey(WHITE)
        self.screen.blit(img, (119, 30))
        display.flip()
        return back_button
