import chess
import random

class Result:
    def __init__(self, move):
        self.move = move

class HumanPlayer:
    def __init__(self):
        pass
    def play(self, board, limit):
        return self.get_user_move(board)

    def quit(self):
        pass
    
    def get_user_move(self, board):
        # Get well-formated move
        move = None
        while move is None:
            san_option = random.choice([board.san(m) for m in board.legal_moves])
            uci_option = random.choice([m.uci() for m in board.legal_moves])
            uci = input(f"Your move (e.g. {san_option} or {uci_option}): ")
            if uci in ("quit", "exit"):
                return None

            for parse in (board.parse_san, chess.Move.from_uci):
                try:
                    move = parse(uci)
                except ValueError:
                    pass

        # Check legality
        if move not in board.legal_moves:
            print("Illegal move.")
            return self.get_user_move(board)

        return Result(move)