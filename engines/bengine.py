#!/bin/python3
import sys
import os
import chess
import time
import argparse
import logging
from weight_generation import WEIGHTS

if not os.path.exists("log"):
    os.makedirs("log")
logging.basicConfig(filename=f"./log/bengine_{time.time()}.log", filemode='w', level=logging.DEBUG)

# TODO: Do this in a more OOP way


def evaluate(board):
    # TODO: Evaluate positions considering developement to be valuable
    value = 0

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            value =  -sys.maxsize
        else:
            value = sys.maxsize

    pieces = board.piece_map()

    for i in pieces:
        piece_value = WEIGHTS['PIECE'][pieces[i].symbol().upper()]

        if pieces[i].symbol().islower():
            piece_value = - piece_value
            piece_value = piece_value * WEIGHTS['LOCATION'][pieces[i].symbol().upper()][63-i]

        else:
            piece_value = piece_value * WEIGHTS['LOCATION'][pieces[i].symbol()][i]


        value = value + piece_value

    if board.is_stalemate():
        if value < 0:
            value = value + 0.5
        else:
            value = value - 0.5

    return value, board.peek()

def negamax(board, depth, alpha, beta, color, stop_time):
    # TODO: Make this behave async to avoid the weird stop_time check
    if time.time() > stop_time:
        return [None, None]
    if depth == 0:
        result = evaluate(board)
        return color* result[0], result[1]
    maximum = -sys.maxsize
    best_move = None
    potential_moves = list(board.legal_moves)

    for move in potential_moves:
        board.push(move)
        result = negamax(board, depth - 1, -beta, -alpha, -color, stop_time)
        if result == [None, None]:
            return [None, None]
        score = - result[0]
        if score > maximum:
            maximum = score
            best_move = move
        board.pop()
        alpha = max(alpha, maximum)
        if beta<=alpha:
            break
    return float(maximum), best_move


def next_move(depth, board):
    # TODO: solve issue with needing async calls here
    # TODO: Save the calcs we already did when we chose our last branch
    stop = time.time() + 3
    depth = 1
    best_move = None
    while True: 
        maximum, move = negamax(board, depth,-sys.maxsize, sys.maxsize, -1+2*int(board.turn), stop)
        if maximum == None:
            break
        best_move = move
        depth = depth + 1
    return best_move

def talk():
    # TODO: Make main loop be async
    board = chess.Board()
    depth = get_depth()

    while True:
        msg = input()
        command(depth, board, msg)


def command(depth: int, board: chess.Board, msg: str):
    # TODO: Make reading of the commands way more obvious
    logging.info(f"IN: {msg}")
    msg = msg.strip()
    tokens = msg.split(" ")
    while "" in tokens:
        tokens.remove("")

    if msg == "quit":
        sys.exit()

    if msg == "uci":
        print("id name Bengine")
        logging.info("OUT: id name Bengine")
        print("id author Ben Dunk")
        logging.info("OUT: author Ben Dunk")
        print("uciok")
        logging.info("OUT: uciok")

        return

    if msg == "isready":
        print("readyok")
        logging.info("OUT: readyok")
        return

    if msg == "ucinewgame":
        return

    if msg.startswith("position"):
        if len(tokens) < 2:
            return

        if tokens[1] == "startpos":
            board.reset()
            moves_start = 2
        elif tokens[1] == "fen":
            fen = " ".join(tokens[2:8])
            board.set_fen(fen)
            moves_start = 8
        else:
            return

        if len(tokens) <= moves_start or tokens[moves_start] != "moves":
            return

        for move in tokens[(moves_start+1):]:
            board.push_uci(move)

    if msg[0:2] == "go":
        _move = next_move(depth, board)
        print(f"bestmove {_move}")
        logging.info(f"OUT: bestmove {_move}")
        return

def get_depth() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", default=3, help="provide an integer (default: 3)")
    args = parser.parse_args()
    return max([1, int(args.depth)])

talk()