from select import select
from datetime import datetime
from pygame import event, mouse, quit
from pygame import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE
from src.player import Player
from src.screens import Screens
from src.acts import Acts

LEFT_CLICK = 1


class Client:
    def __init__(self):
        # Init screen
        self.player = Player()
        self.player.connect_play()
        self.screen = Screens()
        self.acts = Acts()
        self.quit = False

    def did_quit(self, event, color=False):
        # Check if player quit
        if event.type == QUIT:
            if color:
                self.player.send_act("quit " + self.player.color)
            else:
                self.player.send_act("quit")
            self.quit = True
            return True
        return False

    def did_click(self, event, button=None):
        # Check if player click the mouse on button
        if button:
            return event.type == MOUSEBUTTONDOWN \
                and event.button == LEFT_CLICK \
                and button.collidepoint(mouse.get_pos())
        return event.type == MOUSEBUTTONDOWN \
            and event.button == LEFT_CLICK

    def open_screen(self):
        # Start a game/ get the instructions/ quit
        players2_button, players4_button, ins_button = self.screen.show_open()
        while not self.quit:
            for e in event.get():
                self.did_quit(e)
                if self.did_click(e, players2_button):
                    self.players_screen(2)
                elif self.did_click(e, players4_button):
                    self.players_screen(4)
                elif self.did_click(e, ins_button):
                    self.ins_screen()
        quit()

    def ins_screen(self):
        # Read instruction/ go back to the open screen/ quit
        back_button = self.screen.show_inc()
        while not self.quit:
            for e in event.get():
                self.did_quit(e)
                if self.did_click(e, back_button):
                    self.open_screen()

    def players_screen(self, num_players):
        # Chose your player color
        taken_colors = []
        self.screen.show_players(self.acts.x_arrow, taken_colors)
        while not self.quit:
            rlist, w, x = select([self.player.p_socket], [], [], 1)
            change_pic = False
            for e in event.get():
                if e.type == KEYDOWN:
                    if e.key == K_LEFT \
                            or e.key == K_RIGHT:
                        self.acts.move_arrow(e)
                        change_pic = True
                    if e.key == K_SPACE:  # select color
                        color, x_pic = self.acts.selected_player(e)
                        if color not in taken_colors:
                            # set color to player
                            self.player.send_act("color " + color)
                            self.player.set_color(color)
                            self.screen.show_your_player(x_pic)
                            change_pic = True
            for message in rlist:
                taken_colors.append(self.player.get_act())
                change_pic = True
            if change_pic:
                self.screen.show_players(self.acts.x_arrow, taken_colors)
                if self.player.color is not None:
                    self.screen.show_your_player(x_pic)
            if self.player.color is not None \
                    and len(taken_colors) == num_players-1:
                # start game
                taken_colors.append(self.player.color)
                self.game_screen(taken_colors)

    def game_screen(self, players_colors):
        # Play against other players
        player_bomb_time = []  # the bombs that current player put
        bombs_position = {}
        explosions_position = {}
        players_position = self.screen.show_game(self.player, players_colors)
        while not self.quit:
            rlist, w, x = select([self.player.p_socket], [], [], 0.1)
            if self.acts.check_bombs(self.player, bombs_position,
                                     explosions_position, player_bomb_time):
                self.screen.present_game_board(players_position,
                                               bombs_position,
                                               explosions_position)

            for e in event.get():
                self.did_quit(e, True)
                if e.type == KEYDOWN:
                    self.acts.move_player(e, self.player, bombs_position,
                                          player_bomb_time)
            for message in rlist:
                act = self.player.get_act()
                if act:
                    list_act = act.split()
                    if list_act[0] == "move":
                        # change the player position
                        players_position[list_act[1]] = ((int(list_act[2]),
                                                          int(list_act[3])
                                                          ), list_act[4])
                        self.screen.present_game_board(players_position,
                                                       bombs_position,
                                                       explosions_position)
                    elif list_act[0] == "bomb":
                        # add bomb
                        bombs_position[datetime.now()] = (int(list_act[1]),
                                                          int(list_act[2]))
                        self.screen.present_game_board(players_position,
                                                       bombs_position,
                                                       explosions_position)
                    elif list_act[0] == "heart":
                        # change the player hearts, check if the player died
                        if int(list_act[2]) == 0:  # dead
                            if self.player.color == list_act[1]:
                                self.end_screen(len(players_position))
                            else:
                                self.screen.present_hearts(list_act[1],
                                                           100 + len
                                                           (players_position))
                                players_position.pop(list_act[1])
                                if len(players_position) == 1:
                                    self.end_screen(1)
                        else:
                            self.screen.present_hearts(list_act[1],
                                                       int(list_act[2]))
                    elif list_act[0] == "quit":
                        players_position.pop(list_act[1])
                        if len(players_position) == 1:
                            self.end_screen(1)
                        else:
                            self.screen.present_hearts(list_act[1], 200)

    def end_screen(self, place):
        # Quit/ go back to the open screen
        back_button = self.screen.show_end(place)
        while not self.quit:
            for e in event.get():
                self.did_quit(e, True)
                if self.did_click(e, back_button):
                    self.player.reset()
                    self.open_screen()


def main():
    Client().open_screen()


if __name__ == '__main__':
    main()
