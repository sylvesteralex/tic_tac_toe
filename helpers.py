
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


if __name__ == '__main__':
    pass
