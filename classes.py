
# collecting all squares in a set is a win
winner_combos = (
        {"a1", "a2", "a3"},
        {"b1", "b2", "b3"},
        {"c1", "c2", "c3"},
        {"a1", "b1", "c1"},
        {"a2", "b2", "c2"},
        {"a3", "b3", "c3"},
        {"a1", "b2", "c3"},
        {"a3", "b2", "c1"}
    )

# squares bordering the center
edges = {"a2", "b1", "b3", "c2"}
# squares bordered by two edge squares.
corners = {"a1", "a3", "c1", "c3"}

# Keeps track of game grid, players marked fields, ai strategy
class Grid:
    def __init__(self):
        self.player_symbol = None
        self.second_player_symbol = None
        # fields
        self.fields = {
            "a1": "_",
            "a2": "_",
            "a3": "_",
            "b1": "_",
            "b2": "_",
            "b3": "_",
            "c1": "_",
            "c2": "_",
            "c3": "_",
        }
        # grid visual representation
        self.grid_visual()
        # self.player_fields = set()
        # self.ai_fields = set()
        self.ai_strategy = None

    def get_fields(self):
        return list(self.fields.keys())

    def get_field_values(self):
        return list(self.fields.values())

    def mark_field(self, field, symbol):
        self.fields[field] = symbol
        # update board
        self.grid_visual()

    def choose_player_symbol(self):
        '''assign X or O symbol to Player and AI'''
        symbol_signs = ("x", "o")
        # assign player symbol
        while self.player_symbol not in symbol_signs or self.player_symbol is None:
            self.player_symbol = str(input("Choose X or O: ").lower())
        # assign ai symbol
        self.second_player_symbol = symbol_signs[int(symbol_signs.index(self.player_symbol) - 1)]

    def grid_visual(self):
        # grid visual representation
        return \
            f'''
                A   B   C
            1 |_{list(self.fields.values())[0]}_|_{list(self.fields.values())[3]}_|_{list(self.fields.values())[6]}_|
            2 |_{list(self.fields.values())[1]}_|_{list(self.fields.values())[4]}_|_{list(self.fields.values())[7]}_|
            3 |_{list(self.fields.values())[2]}_|_{list(self.fields.values())[5]}_|_{list(self.fields.values())[8]}_|
            '''

    def show_grid(self):
        print(self.grid_visual())

# Store data about score and players
class ScoreTable:
    def __init__(self):
        self.player = "player"
        self.second_player = "player2"
        self.table = {str(self.player): 0, str(self.second_player): 0}
        # self.player = list(self.table.keys())[0]
        # self.second_player = list(self.table.keys())[1]
        self.current_player = None
        self.game_versus_human = None

    def add_point(self, player_name):
        self.table[player_name] += 1

    def choose_player_name(self):
        self.player = str(input("What's your name? ").title())
        if self.player == "":
            self.player = "player"

    def play_versus_human(self):
        versus_ai = str(input("Do you want to play against AI? (Y/N): ").strip().upper())
        if versus_ai not in ("Y", "N"):
            print("Command not recognized. Try again. N - for other human player, Y - for AI")
            self.play_versus_human()
        elif versus_ai == "N":
            self.second_player = str(input("What's your opponent name? ").title())
            if self.second_player == "":
                self.second_player = "player2"
            self.game_versus_human = True
        else:
            self.second_player = "ai"
            self.game_versus_human = False
