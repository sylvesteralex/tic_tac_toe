from random import choice
from setup import grid
from helpers import winner_combos, edges, corners


def ai_behavior(current_turn):

    # strategies
    def ai_starts_first() -> str:
        '''random choice of any corner or the middle, returns field number as a string'''
        moves_first = choice(["a1", "a3", "b2", "c1", "c3"])
        return moves_first

    def ai_starts_second() -> str:
        '''random choice of any corner or middle depending on what the player did, returns field number as a string'''
        if grid.player_fields == "b2":
            moves_second = choice(["a1", "a3", "c1", "c3"])
        else:
            moves_second = "b2"
        return moves_second

    def ai_chooses_far_corner() -> str:
        '''random choice of opposite corner, returns field number as a string'''
        player_mistake = next(iter(grid.player_fields))
        # player's field second el. is '2' ('a' or 'c'), subtract 'a' or 'c' accordingly from corners,
        # and choose one of opposite corners -> 'a1', 'a3' or 'c1', 'c3'
        if str(player_mistake[1]) == "2":
            corner_move = choice(list(corners - {
                str(player_mistake[0] + "1"),
                str(player_mistake[0] + "3")
            }))
            return corner_move
        # player's field second el. is '1' or '3' ('b'), choose opposite corners,
        elif str(player_mistake[1]) == "1":
            corner_move = choice(["a3", "c3"])
            return corner_move
        else:
            corner_move = choice(["a1", "c1"])
            return corner_move

    def ai_chooses_diagonal_corner() -> str:
        player_corner = next(iter(grid.player_fields))

        if str(player_corner[0]) == "a":
            corner_move = "c"
        else:
            corner_move = "a"

        if str(player_corner[1]) == "1":
            corner_move += "3"
        else:
            corner_move += "1"

        return corner_move

    def ai_chooses_any_corner_left():
        corner_move = choice(list(corners - grid.second_player_fields - grid.player_fields))
        return corner_move

    def ai_chooses_randomly():
        random_move = choice(list(set(grid.get_fields()) - grid.second_player_fields - grid.player_fields))
        return random_move

    def ai_stops_player():
        for combo in winner_combos:
            stopping_player = (combo - grid.player_fields)
            if stopping_player.issubset(combo) and len(stopping_player) == 1:
                # print("plr fields", ai_stops_player)
                stop_move = next(iter(stopping_player))
                if stop_move in grid.player_fields or stop_move in grid.second_player_fields:
                    continue
                else:
                    return stop_move

    def ai_goes_for_win():
        for combo in winner_combos:
            going_for_win = (combo - grid.second_player_fields)
            if going_for_win.issubset(combo) and len(going_for_win) == 1:
                # print("ai fields", ai_goes_for_win)
                win_move = next(iter(going_for_win))
                if win_move in grid.player_fields or win_move in grid.second_player_fields:
                    continue
                else:
                    return win_move

    # move = ai_goes_for_win()
    # return move

    # scenarios
    # ==== SCENARIO 1 ==== AI starts the game first, turn_count == even
    if current_turn == 0:
        move = ai_starts_first()
        return move

    elif current_turn == 2:
        # did ai choose previously the middle?
        if "b2" in grid.second_player_fields:
            # did player make a mistake? (chose an edge)
            if grid.player_fields.issubset(edges):
                # choose one of the two corners furthest from the player's edge square.
                # player must block you or looses
                grid.ai_strategy = "ai_first_middle_player_edge"
                move = ai_chooses_far_corner()
                return move
            # player chose corner
            else:
                # choose the opposite corner to make diagonal line of all marks on the grid
                grid.ai_strategy = "ai_first_middle_player_corner"
                move = ai_chooses_diagonal_corner()
                return move
        # ai chose previously corner
        else:
            # TODO: improve ai strategies
            # for now goes random
            move = ai_chooses_randomly()
            return move

    elif current_turn == 4:
        if grid.ai_strategy == "ai_first_middle_player_edge":
            # player blocked you, now ai blocks player and sets a trap
            move = ai_stops_player()
            return move
        # grid.ai_strategy = "ai_first_middle_player_corner"
        else:
            # player chose edge (mistake), ai goes for any corner and goes for win
            if grid.player_fields.issubset(edges):
                grid.ai_strategy = "ai_first_middle_player_corner_edge"
                move = ai_chooses_any_corner_left()
                return move
            # player chose corner, ai must block player, will result in tie
            else:
                grid.ai_strategy = "ai_first_middle_player_corner_corner"
                move = ai_stops_player()
                return move

    elif current_turn == 6:
        if grid.ai_strategy == "ai_first_middle_player_corner_edge":
            # ai goes for win
            move = ai_goes_for_win()
            return move
        else:
            # ai goes for tie, no possibility of winning
            move = ai_stops_player()
            return move

    # ==== SCENARIO 2 ==== AI starts second, turn_count == odd
    elif current_turn == 1:
        move = ai_starts_second()
        return move

    elif current_turn == 3:
        # player made the best choice and placed move on diagonal corner
        if grid.player_fields:
            move = ai_chooses_any_corner_left()
            return move
        # player made another move
        else:
            # TODO: improve ai strategies
            # for now goes random
            move = ai_chooses_randomly()
            return move

    elif current_turn == 5:
        move = ai_stops_player()
        return move

    elif current_turn == 7:
        move = ai_stops_player()
        return move

    # ==== GO RANDOM ==== no way to win only tie, mark all the rest field until the game ends
    else:
        # ai go for tie and chooses randomly all fields that left
        move = ai_chooses_randomly()
        return move


if __name__ == '__main__':
    pass
