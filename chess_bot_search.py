import chess
import chess_evaluation

# pseudocode:
# function alphabeta(node, depth, α, β, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
#             α := max(α, value)
#             if α ≥ β then
#                 break (* β cutoff *)
#         return value
#     else
#         value := +∞
#         for each child of node do
#             value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
#             β := min(β, value)
#             if β ≤ α then
#                 break (* α cutoff *)
#         return value

def alpha_beta_pruning(board, coefficient_list, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over():
        return chess_evaluation.evaluate(coefficient_list, board, maximizingPlayer)
    if maximizingPlayer:
        value = -999999999
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
        value = 999999999
        all_possible_moves = board.legal_moves
        for move in all_possible_moves:
            board.push(move)
            value = min(value, alpha_beta_pruning(board, coefficient_list, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            board.pop()
            if beta <= alpha:
                break
        return value