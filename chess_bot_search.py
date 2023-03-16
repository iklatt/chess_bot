import chess
import chess_evaluation
import time

def alpha_beta_pruning(board, coefficient_list, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over():
        return chess_evaluation.evaluate(board, coefficient_list)
    if maximizingPlayer:
        value = float("-inf")
        all_possible_moves = board.legal_moves
        for move in all_possible_moves:
            board.push(move)
            value = max(value, alpha_beta_pruning(board, coefficient_list, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            board.pop()
            if alpha >= beta:
                break
        return value
    else:
        value = float("inf")
        all_possible_moves = board.legal_moves
        for move in all_possible_moves:
            board.push(move)
            value = min(value, alpha_beta_pruning(board, coefficient_list, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            board.pop()
            if beta <= alpha:
                break
        return value
    
def move_search(board, coefficient_list, depth, is_white):
    all_possible_moves = board.legal_moves
    max = float("-inf")
    max_move = None
    min = float("inf")
    min_move = None
    for move in all_possible_moves:
        board.push(move)
        new_value = alpha_beta_pruning(board, coefficient_list, depth - 1, float("-inf"), float("inf"), is_white)
        board.pop()
        if new_value > max:
            max = new_value
            max_move = move
        if new_value < min:
            min = new_value
            min_move = move
    if is_white:
        return max_move
    return min_move

def iterative_deepening(max_time_to_start, board, coefficient_list, is_white):
    depth = 1
    move = None
    start_time = time.time()
    current_time = start_time
    while current_time - start_time < max_time_to_start:
        move = move_search(board, coefficient_list, depth, is_white)
        depth += 1
        current_time = time.time()
    end_time = time.time()
    print("Took", end_time - start_time, "seconds to finish.  Went to depth", depth - 1)
    return move

if __name__ == "__main__":
    board = chess.Board()
    coefficient_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    move = iterative_deepening(1, board, coefficient_list, True)
    print(move)