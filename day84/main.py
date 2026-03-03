want_to_play = "y"

while want_to_play == "y":

    def display_board(board):
        print("\n")
        print(f" {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} ")
        print("\n")

    def display_positions():
        print("Position guide:")
        print(" 1 | 2 | 3 ")
        print("---+---+---")
        print(" 4 | 5 | 6 ")
        print("---+---+---")
        print(" 7 | 8 | 9 ")
        print("\n")

    def check_winner(board, player):
        winning_combinations = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in winning_combinations:
            if board[a] == board[b] == board[c] == player:
                return True
        return False

    def is_board_full(board):
        return " " not in board

    want_to_play = input("Do you want to play a game of Tic Tac Toe? Type 'y' or 'n': ")
    if want_to_play == "n":
        break

    board = [" "] * 9
    current_player = "X"
    game_over = False

    print("\nWelcome to Tic Tac Toe!")

    while game_over == False:
        display_positions()
        display_board(board)
        move = input(f"Player {current_player}, choose your move (1-9): ")

        if not move.isdigit():
            print("Please enter a number between 1 and 9.")
            continue

        position = int(move) - 1

        if position < 0 or position > 8:
            print("That position is out of range. Choose a number between 1 and 9.")
            continue

        if board[position] != " ":
            print("That position is already taken. Choose another one.")
            continue

        board[position] = current_player

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif is_board_full(board):
            display_board(board)
            print("It's a draw!")
            game_over = True
        else:
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"
