#!/bin/python3
import sys
import os
import chess
import time
from threading import Thread
import logging
from weight_generation import WEIGHTS
import time
import sys
import copy

if not os.path.exists("log"):
    os.makedirs("log")
logging.basicConfig(filename=f"./log/bengine_{time.time()}.log", filemode='w', level=logging.DEBUG)

# TODO: Do this in a more OOP way


def evaluate(board):
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

def negamax(board, depth, alpha, beta, color):
    if depth == 0:
        result = evaluate(board)
        return color* result[0], result[1]
    time.sleep(0)
    maximum = -sys.maxsize
    best_move = None
    potential_moves = list(board.legal_moves)

    for move in potential_moves:
        board.push(move)
        result = negamax(board, depth - 1, -beta, -alpha, -color)
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

def calculate(board, result_holder):
    depth = 1
    start_time = time.time()

    while True:
        # Perform search operation for the current depth
        # Replace this with your actual search algorithm
        logging.debug(f"Performing search at depth {depth}")
        result = negamax(copy.deepcopy(board), depth, -sys.maxsize, sys.maxsize,-1+2*int(board.turn))        
        # Store the result in the shared variable
        result_holder["result"] = result
        
        # Check if 3 seconds have passed, and stop the search
        if time.time() - start_time >= 3:
            logging.debug("Time limit reached. Stopping search.")
            break
        
        depth += 1
 
def search(board):    
    # Shared variable to hold the search result
    result_holder = {"result": None}
    
    # Create a thread for iterative deepening search
    search_thread = Thread(target=calculate, args=(board, result_holder))
    search_thread.start()
    
    time.sleep(3)
    print(f"bestmove {result_holder['result'][1]}")
    sys.stdout.flush()

    logging.info(f"OUT: bestmove {result_holder['result'][1]}")

    if search_thread.is_alive():
        search_thread.join()  # wait for child to return itself before returning this one
     


def main():

    board = chess.Board()

    tasks = []

    while True:

        msg = input()

        if not msg:
            break
    
        msg = msg.strip()
        tokens = msg.split(" ")
        while "" in tokens:
            tokens.remove("")

        logging.info(f"IN: {msg}")
        
        if msg == "quit":
            break

        if msg == "uci":
            print("id name Bengine")
            logging.info("OUT: id name Bengine")
            print("id author Ben Dunk")
            logging.info("OUT: author Ben Dunk")
            print("uciok")
            logging.info("OUT: uciok")

            continue

        if msg == "isready":
            print("readyok")
            logging.info("OUT: readyok")
            continue

        if msg == "ucinewgame":
            continue

        if msg.startswith("position"):
            if len(tokens) < 2:
                continue

            if tokens[1] == "startpos":
                board.reset()
                moves_start = 2
            elif tokens[1] == "fen":
                fen = " ".join(tokens[2:8])
                board.set_fen(fen)
                moves_start = 8
            else:
                continue

            if len(tokens) <= moves_start or tokens[moves_start] != "moves":
                continue

            for move in tokens[(moves_start+1):]:
                board.push_uci(move)

        if msg[0:2] == "go":
            task = Thread(target=search, args=[board])
            task.start()
            tasks.append(task)
            
            continue
    for t in tasks:
        t.join()
    sys.exit()

if __name__ == '__main__':

    main()