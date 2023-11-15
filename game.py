import chess
import chess.engine
from engines.human_player import HumanPlayer

def print_unicode_board(board, perspective=chess.WHITE):
    """Prints the position from a given perspective."""
    sc, ec = "\x1b[0;30;107m", "\x1b[0m"
    for r in range(8) if perspective == chess.BLACK else range(7, -1, -1):
        line = [f"{sc} {r+1}"]
        for c in range(8) if perspective == chess.WHITE else range(7, -1, -1):
            color = "\x1b[48;5;255m" if (r + c) % 2 == 1 else "\x1b[48;5;253m"
            if board.move_stack:
                if board.move_stack[-1].to_square == 8 * r + c:
                    color = "\x1b[48;5;153m"
                elif board.move_stack[-1].from_square == 8 * r + c:
                    color = "\x1b[48;5;153m"
            piece = board.piece_at(8 * r + c)
            line.append(
                color + (chess.UNICODE_PIECE_SYMBOLS[piece.symbol()] if piece else " ")
            )
        print(" " + " ".join(line) + f" {sc} {ec}")
    if perspective == chess.WHITE:
        print(f" {sc}   a b c d e f g h  {ec}\n")
    else:
        print(f" {sc}   h g f e d c b a  {ec}\n")

    
RANDOM_ENGINE = "/home/ben/src/ChessBengine/engines/dist/random_engine/random_engine"
BENGINE = "/home/ben/src/ChessBengine/engines/dist/bengine/bengine"
# white_player = HumanPlayer()
white_player = chess.engine.SimpleEngine.popen_uci(RANDOM_ENGINE)
black_player = chess.engine.SimpleEngine.popen_uci(BENGINE)
board = chess.Board()
while not board.is_game_over():
    print_unicode_board(board)
    if board.turn == chess.WHITE:
        result = white_player.play(board, chess.engine.Limit(time=5))
    else:
        result = black_player.play(board, chess.engine.Limit(time=5))

    board.push(result.move)

print_unicode_board(board)
print(board.result())

white_player.quit()
black_player.quit()