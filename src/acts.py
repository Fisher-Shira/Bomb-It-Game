from pygame import K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN
from datetime import datetime
from src.squares import Squares
from src.color import Color


class Acts:
    def __init__(self):
        self.x_arrow = Color.select_pos["pink"]

    def move_arrow(self, event):
        # change the arrow position
        if event.key == K_LEFT:
            # move the arrow left
            if self.x_arrow == Color.select_pos["pink"]:
                self.x_arrow = Color.select_pos["green"]
            else:
                self.x_arrow -= Color.pos_dif
        elif event.key == K_RIGHT:
            # move the arrow right
            if self.x_arrow == Color.select_pos["green"]:
                self.x_arrow = Color.select_pos["pink"]
            else:
                self.x_arrow += Color.pos_dif

    def selected_player(self, event):
        # check and return the selected color
        if event.key == K_SPACE:
            if self.x_arrow == Color.select_pos["pink"]:
                return "pink", self.x_arrow
            if self.x_arrow == Color.select_pos["yellow"]:
                return "yellow", self.x_arrow
            if self.x_arrow == Color.select_pos["blue"]:
                return "blue", self.x_arrow
            return "green", self.x_arrow

    def move_player(self, event, player, bombs_position, player_bomb_time):
        # move the player/ put bomb
        # return did the payer moved (if available) or not
        change_direction = False
        clear_squares = Squares.clear_squares
        if event.key == K_LEFT and (player.column-1, player.raw) \
            in clear_squares and not (player.column-1, player.raw) \
                in bombs_position.values():
            player.direction = "l"
            player.column -= 1
            change_direction = True
        elif event.key == K_RIGHT and (player.column+1, player.raw) \
            in clear_squares and not (player.column+1, player.raw) \
                in bombs_position.values():
            player.direction = "r"
            player.column += 1
            change_direction = True
        elif event.key == K_UP and (player.column, player.raw-1) \
            in clear_squares and not (player.column, player.raw-1) \
                in bombs_position.values():
            player.direction = "u"
            player.raw -= 1
            change_direction = True
        elif event.key == K_DOWN and (player.column, player.raw+1) \
            in clear_squares and not (player.column, player.raw+1) in \
                bombs_position.values():
            player.direction = "d"
            player.raw += 1
            change_direction = True
        if change_direction:
            player.send_act(("move " + player.color + ' ' + str(player.column)
                             + ' ' + str(player.raw) + ' ' + player.direction))
        # Bomb
        if event.key == K_SPACE and player.bombs < 2:
            player.bombs += 1
            player_bomb_time.append(datetime.now())
            player.send_act("bomb " + str(player.column) + ' '
                            + str(player.raw))

    def check_bombs(self, player, bombs_position, explosions_position,
                    player_bomb_time):
        change = False
        temp = {}
        # check if bomb need to explode
        for time in bombs_position:
            temp[time] = bombs_position[time]
        for time in temp:
            if (datetime.now() - time).seconds >= 3:
                explosions_position[datetime.now()] = (temp[time], [])
                bombs_position.pop(time)
                change = True
        temp = {}
        # check if bomb need to stop exploding
        for time in explosions_position:
            temp[time] = explosions_position[time]
        for time in temp:
            if (datetime.now() - time).seconds >= 1:
                # add all the new clear positions
                places = [(temp[time][0][0]+1, temp[time][0][1]),
                          (temp[time][0][0]-1, temp[time][0][1]),
                          (temp[time][0][0], temp[time][0][1]+1),
                          (temp[time][0][0], temp[time][0][1]-1)]
                for place in places:
                    if place not in Squares.clear_squares \
                            and place not in Squares.block_squares \
                            and place not in Squares.statue_squares:
                        Squares.clear_squares.append(place)
                explosions_position.pop(time)
                change = True
            # check if bomb heart player
            else:
                explosion_column = explosions_position[time][0][0]
                explosion_raw = explosions_position[time][0][1]
                if player.color not in explosions_position[time][1]:
                    full_positions = [(explosion_column, explosion_raw),
                                      (explosion_column + 1, explosion_raw),
                                      (explosion_column - 1, explosion_raw),
                                      (explosion_column, explosion_raw + 1),
                                      (explosion_column, explosion_raw - 1)]
                    if (player.column, player.raw) in full_positions:
                        explosions_position[time][1].append(player.color)
                        player.hearts -= 1
                        player.send_act("heart " + player.color + ' ' +
                                        str(player.hearts))
        # check if my bomb explode
        for player_time in player_bomb_time:
            if (datetime.now() - player_time).seconds >= 3:
                player.bombs -= 1
                player_bomb_time.remove(player_time)
        return change
