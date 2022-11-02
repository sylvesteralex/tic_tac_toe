from random import choice
from classes import Grid, ScoreTable, winner_combos


def app():
    # =======================================
    # =========== SETTING GAME ==============
    # =======================================
    # set score table
    score = ScoreTable()
    # player name
    score.choose_player_name()
    # play with human or AI -- work in progress
    score.play_versus_human()
    # start new grid
    grid = Grid()
    # player symbol
    grid.choose_player_symbol()
    print(f"You chose: {grid.player_symbol}")

    # print game grid
    grid.show_grid()

    # store occupied fields
    player_fields = set()
    ai_fields = set()

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
            if combo == player_fields:
                # add point for the player
                print(f"{score.player} wins")
                score.add_point(score.player)
                should_game_go_on = False
                break
            # game is settled, second player wins
            elif combo == ai_fields:
                # add point for the player
                print(f"{score.second_player} wins")
                score.add_point(score.second_player)
                should_game_go_on = False
                break
            else:
                continue

        return should_game_go_on

    def check_if_move_possible(player_or_ai, current_move):
        # ==== Player move
        if player_or_ai == "player":
            # check if move is correct
            if current_move not in grid.get_fields():
                print("choose only fields from the board: A1, B2 etc.")
                move = player_move_input()
                check_if_move_possible(player_or_ai="player", current_move=move)

            # check if field is free
            if current_move in player_fields or current_move in ai_fields:
                print("this field is already taken")
                move = player_move_input()
                check_if_move_possible(player_or_ai="player", current_move=move)

        # ==== AI move
        elif player_or_ai == "ai":
            if current_move in player_fields or current_move in ai_fields:
                # if chosen field not available, get any free square
                move = choice(grid.get_fields())
                # move = ai_move()
                check_if_move_possible(player_or_ai="ai", current_move=move)

    def ai_behavior(current_turn):
        if current_turn == 0:
            move = "b2"
            return move
        elif current_turn == 1:
            move = choice(grid.get_fields())
            return move
        else:
            # who moved first? who has more fields occupied?
            # if len(ai_fields) > len(player_fields):
                # ai is close to win,
                # ai_move should go for a win
                # (winning_combo - current_ai_fields)-> combo with 1 el. left if the field is free should be the move
            for combo in winner_combos:
                ai_chance = (combo - ai_fields)
                if ai_chance.issubset(combo) and len(ai_chance) == 1:
                    # print("ai fields", ai_chance)
                    move = next(iter(ai_chance))
                    if move in player_fields or move in ai_fields:
                        continue
                    else:
                        return move
                else:
                    # player is close to win,
                    # ai_move should stop the player
                    for combo in winner_combos:
                        ai_stops_player = (combo - player_fields)
                        if ai_stops_player.issubset(combo) and len(ai_stops_player) == 1:
                            # print("plr fields", ai_stops_player)
                            move = next(iter(ai_stops_player))
                            if move in player_fields or move in ai_fields:
                                continue
                            else:
                                return move

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
        if current_player == score.player:
            player_move = player_move_input()
            check_if_move_possible(player_or_ai="player", current_move=player_move)

            # store the move
            player_fields.add(player_move)

            # mark the field with symbol
            for field in player_fields:
                if field in grid.get_fields():
                    grid.mark_field(field, grid.player_symbol)

            # show current board
            grid.show_grid()
            # switch players
            score.current_player = score.second_player

        # human player 2 or AI moves
        else:
            if score.game_versus_human:
                # game versus human/player2
                player_move = player_move_input()
                check_if_move_possible(player_or_ai="player", current_move=player_move)

                # store the move
                ai_fields.add(player_move)

                # mark the field with symbol
                for field in ai_fields:
                    if field in grid.get_fields():
                        grid.mark_field(field, grid.second_player_symbol)

                # show current board
                grid.show_grid()
                # switch players
                score.current_player = score.player
            # AI moves
            else:
                ai_move = ai_behavior(current_turn)
                # print("ai supposed move", ai_move)
                # check if field is free
                check_if_move_possible(player_or_ai="ai", current_move=ai_move)
                # print("ai actual move", ai_move)

                # store the move
                ai_fields.add(ai_move)

                # mark the field with symbol
                for field in ai_fields:
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
        print("we have a winner")

    print("end")
    print(score.table)


if __name__ == '__main__':
    app()
