from models import Grid, ScoreTable


# set score table
score = ScoreTable()
# start new grid
grid = Grid()

def setup_new_grid():
    # player name
    score.choose_player_name()
    # player symbol
    grid.choose_player_symbol()
    print(f"You chose: {grid.player_symbol}")
    # play with human or AI
    score.play_versus_human()


if __name__ == '__main__':
    pass
