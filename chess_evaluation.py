import chess

# Purpose is to give value to pieces irregardless of their position.
def piece_evaluation(fen, coefficient_list = [1, 1, 1, 1, 1]):
    pawn = coefficient_list[0] * 100
    knight = coefficient_list[1] * 300
    bishop = coefficient_list[2] * 300
    rook = coefficient_list[3] * 500
    queen = coefficient_list[4] * 900

    score = 0
    for letter in fen:
        match letter:
            case " ":
                break
            case "p":
                score -= pawn
            case "P":
                score += pawn
            case "n":
                score -= knight
            case "N":
                score += knight
            case "b":
                score -= bishop
            case "B":
                score += bishop
            case "r":
                score -= rook
            case "R":
                score += rook
            case "q":
                score -= queen
            case "Q":
                score += queen
    return score

# We will use the definition of the endgame starting when both players have less 
# than or equal to 3 non-pawn pieces
def is_endgame(fen):
    lst = ["P", "p", "k", "K", "/"]
    black_count = 0
    white_count = 0
    for char in fen:
        if char not in lst:
            if char == char.lower():
                black_count += 1
            else:
                white_count += 1
    if white_count <= 3 and black_count <= 3:
        return True
    return False

pawn_matrix = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
]

knight_matrix = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

bishop_matrix = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

rook_matrix = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
]

queen_matrix = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

king_matrix = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

endgame_king_matrix = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

def piece_position_evaluation(fen, coefficient_list = [1, 1, 1, 1, 1, 1]):
    row = 0
    column = 0
    score = 0
    in_endgame = is_endgame(fen)
    for char in fen:
        match char:
            case "p":
                score -= pawn_matrix[7 - row][column] * coefficient_list[0]
            case "P":
                score += pawn_matrix[row][column] * coefficient_list[0]
            case "n":
                score -= knight_matrix[7 - row][column] * coefficient_list[1]
            case "N":
                score += knight_matrix[row][column] * coefficient_list[1]
            case "b":
                score -= bishop_matrix[7 - row][column] * coefficient_list[2]
            case "B":
                score += bishop_matrix[row][column] * coefficient_list[2]
            case "r":
                score -= rook_matrix[7 - row][column] * coefficient_list[3]
            case "R":
                score += rook_matrix[row][column] * coefficient_list[3]
            case "q":
                score -= queen_matrix[7 - row][column] * coefficient_list[4]
            case "Q":
                score += queen_matrix[row][column] * coefficient_list[4]
            case "k":
                if in_endgame:
                    score -= endgame_king_matrix[7 - row][column] * coefficient_list[5]
                else:
                    score -= king_matrix[7 - row][column] * coefficient_list[5]
            case "K":
                if in_endgame:
                    score += endgame_king_matrix[row][column] * coefficient_list[5]
                else:
                    score += king_matrix[row][column] * coefficient_list[5]
            case "/":
                column = -1
                row += 1
            case _:
                column += int(char) - 1
        column += 1

# Evaluate position using helper functions
def evaluate(board, coefficient_list, is_whites_turn):
    long_fen = board.fen()
    # Recheck this logic
    if board.is_checkmate():
        for i in range(len(long_fen)):
            if long_fen[i] == " ":
                if long_fen[i + 1] == "w":
                    return -100000
                return 100000
    elif board.is_game_over() or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves():
        return 0

    fen = board.board_fen()
    score = 0
    score += piece_evaluation(fen, coefficient_list)
    score += piece_position_evaluation(fen, coefficient_list[5:])
    return score