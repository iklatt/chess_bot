import chess
import chess_bot_search as search
import random

def game(coefficient_list, depth):
    is_players_turn = random.randint(0,1)
    ai_is_white = not is_players_turn
    board = chess.Board()
    while not board.is_game_over():
        print("\n", board)
        if is_players_turn:
            player_move = input("Enter your move in Short Algebraic Notation: ")
            try:
                board.push_san(player_move)
                is_players_turn = False
            except:
                print("Move you entered is invalid.  Please try again.")
        else:
            try:
                ai_move = search.move_search(board, coefficient_list, depth, ai_is_white)
                print(ai_move)
                board.push(ai_move)
                is_players_turn = True
            except:
                print("Something went wrong.")

if __name__ == "__main__":
    coefficient_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    game(coefficient_list, 2)