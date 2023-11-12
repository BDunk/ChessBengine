#!/bin/python3
import sys
import os
import chess
import time
import argparse
import logging
from weight_generation import WEIGHTS
import asyncio
import time
import sys

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

async def negamax(board, depth, alpha, beta, color):
    if depth == 0:
        result = evaluate(board)
        return color* result[0], result[1]
    maximum = -sys.maxsize
    best_move = None
    potential_moves = list(board.legal_moves)

    for move in potential_moves:
        board.push(move)
        result = await negamax(board, depth - 1, -beta, -alpha, -color)
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

async def calculate(board, callback):

    result = None

    start_time = asyncio.get_event_loop().time()

    depth = 1

    while True:

        if asyncio.get_event_loop().time() - start_time >= 4:
            break
        logging.debug(f"running for depth {depth}")

        try:

            # Attempt to get a result within the remaining time

            remaining_time = 4 - (asyncio.get_event_loop().time() - start_time)

            result = await asyncio.wait_for(negamax(board, depth, -sys.maxsize, sys.maxsize,-1+2*int(board.turn)), timeout=remaining_time)
            logging.debug(f"ran at depth {depth}, result {result}")
            depth = depth+1

        except asyncio.TimeoutError:

            # If do_stuff doesn't complete within the remaining time, move on

            pass

    callback(result[1])
    logging.info(f"OUT: bestmove {result[1]}")
    return
 



async def main():

    board = chess.Board()

    tasks = []

    while True:

        msg = await asyncio.to_thread(sys.stdin.readline)

        if not msg:
            break
    
        msg = msg.strip()
        tokens = msg.split(" ")
        while "" in tokens:
            tokens.remove("")

        logging.info(f"IN: {msg}")
        
        if msg == "quit":
            sys.exit()

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
            task = asyncio.create_task(calculate(board, lambda x: print(f"bestmove {x}")))
            tasks.append(task)
            
            continue

        

    await asyncio.gather(*tasks)
 

if __name__ == '__main__':

    asyncio.run(main())