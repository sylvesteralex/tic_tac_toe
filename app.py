from random import choice
from helpers import winner_combos
from setup import score, grid, setup_new_grid
from ai_player import ai_behavior


def app():
    # =======================================
    # =========== SETTING GAME ==============
    # =======================================
    setup_new_grid()

    # print game grid
    grid.show_grid()

    # =========================================
    # =========== GAME FUNCTIONS ==============
    # =========================================
    def player_move_input():
        move = str(input("What's your move? (e.g. A1): ").lower())
        return move

    def is_game_not_settled():
        should_game_go_on = True
        for combo in winner_combos:
            # game is settled, player wins
            if combo == grid.player_fields:
                # add point for the player
                print(f"{score.player} wins")
                score.add_point(score.player)
                should_game_go_on = False
                break
            # game is settled, second player wins
            elif combo == grid.second_player_fields:
                # add point for the player
                print(f"{score.second_player} wins")
                score.add_point(score.second_player)
                should_game_go_on = False
                break
            else:
                continue

        return should_game_go_on

    def move_not_possible(player_or_ai, current_move) -> bool:
        # ==== Player move
        if player_or_ai == "player":
            # check if move is correct
            if current_move not in grid.get_fields():
                print("choose only fields from the board: A1, B2 etc.")
                return True

            # check if field is free
            if current_move in grid.player_fields or current_move in grid.second_player_fields:
                print("this field is already taken")
                return True

        # ==== AI move
        elif player_or_ai == "ai":
            if current_move in grid.player_fields or current_move in grid.second_player_fields:
                # if chosen field not available, get any free square
                return True
            elif current_move == None:
                return True
        else:
            return False

    # ====================================
    # =========== EACH TURN ==============
    # ====================================
    def turn(current_turn):

        # if first game turn
        if current_turn == 0:
            # randomly choose first player
            current_player = choice([score.player, score.second_player])
            # store current player in score object
            score.current_player = current_player
        else:
            # if game continues get current player from score object
            current_player = score.current_player

        # current_player = score.player
        print(f"It's now {current_player} move")

        # player moves
        # ============
        if current_player == score.player:
            player_move = player_move_input()
            while move_not_possible(player_or_ai="player", current_move=player_move):
                player_move = player_move_input()

            # store the move
            grid.player_fields.add(player_move)

            # mark the field with symbol
            for field in grid.player_fields:
                if field in grid.get_fields():
                    grid.mark_field(field, grid.player_symbol)

            # show current board
            grid.show_grid()
            # switch players
            score.current_player = score.second_player

        # human player 2 or AI moves
        # ==========================
        else:
            # game versus human/player2
            # =========================
            if score.game_versus_human:
                player_move = player_move_input()
                while move_not_possible(player_or_ai="player", current_move=player_move):
                    player_move = player_move_input()

                # store the move
                grid.second_player_fields.add(player_move)

                # mark the field with symbol
                for field in grid.second_player_fields:
                    if field in grid.get_fields():
                        grid.mark_field(field, grid.second_player_symbol)

                # show current board
                grid.show_grid()
                # switch players
                score.current_player = score.player

            # game versus AI
            # ==============
            else:
                ai_move = ai_behavior(current_turn)
                # check if move is possible
                if move_not_possible(player_or_ai="ai", current_move=ai_move):
                    # fallback: choose random field if move not possible or returned None
                    ai_move = choice(list(set(grid.get_fields()) - grid.second_player_fields - grid.player_fields))

                # store the move
                grid.second_player_fields.add(ai_move)

                # mark the field with symbol
                for field in grid.second_player_fields:
                    if field in grid.get_fields():
                        grid.mark_field(field, grid.second_player_symbol)

                # show current board
                grid.show_grid()
                # switch players
                score.current_player = score.player

    # ====================================
    # =========== GAME FLOW ==============
    # ====================================
    no_winner = True
    turn_count = 0  # there is 9 fields, hence if there is now winner until 8 turn, it's a tie

    while no_winner:
        print("turn:", turn_count)
        if turn_count > 8:
            print("It's a tie")
            break
        turn(turn_count)
        no_winner = is_game_not_settled()
        turn_count += 1
    else:
        print("We have a winner!")

    print("Game end")
    print(score.table)


if __name__ == '__main__':
    app()
