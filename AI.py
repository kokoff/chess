import chess
import chess.pgn
from chess import polyglot
from random import randint
import sys
import timeit
import os
from collections import deque


class RandomAI:
    def __init__(self, board):
        self.board = board

    def GetNextMove(self):
        stop = randint(0, len(self.board.legal_moves) - 1)
        count = 0

        for mv in self.board.legal_moves:
            if stop == count:
                return mv
            count += 1

        return chess.Move.null()


class Node:
    def __init__(self, data):
        self.data = data
        self.nextNode = None
        self.prevNode = None


class FIFO:
    def __init__(self):
        self.head = None
        self.tail = self.head

    def push(self, data):
        node = Node(data)
        node.nextNode = self.head
        self.head = node

    def pop(self):
        data = self.tail.data
        self.tail = self.tail.prevNode
        self.tail.nextNode = None
        return data


class TranspositionTable:
    def __init__(self, capacity):
        self.table = {}
        self.access_list = FIFO()
        self.capacity = capacity

    def add(self, hash, score, ply):
        tup = (score, ply)

        self.table[hash] = tup
        self.access_list.push(tup)

        if len(self.table) >= self.capacity:
            temp = self.access_list.pop()
            if temp in self.table:
                self.table.pop(temp)

    def lookup(self, hash, ply):
        if hash in self.table and self.table[hash][1] >= ply:
            return self.table[hash][0]
        else:
            return None

    def __contains__(self, item):
        return item in self.table

class AI:
    MIN_INT = - sys.maxint - 1
    MAX_INT = sys.maxint

    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.ply = 4
        self.GetNextMove = self.getOpening
        self.table = TranspositionTable(1000000)

    def getOpening(self):
        path = os.path.join('data', 'komodo.bin')
        reader = polyglot.MemoryMappedReader(path)
        self.GetNextMove = self.getMinimaxMove
        return reader.weighted_choice(self.board).move()

    def getMinimaxMove(self):
        bestMove = chess.Move.null()
        bestScore = AI.MIN_INT

        for move in self.board.legal_moves:
            self.board.push(move)
            hash = self.board.zobrist_hash()
            if hash in self.table:
                score = self.table.lookup(hash, self.ply)
            else:
                score = self.minimax(self.board, self.ply, AI.MIN_INT, AI.MAX_INT)
                self.table.add(hash, score, self.ply)
            self.board.pop()
            if bestScore <= score:
                bestMove = move
                bestScore = score

        assert (bestMove != chess.Move.null())
        return bestMove

    def minimax(self, board, ply, alpha, beta):
        maxplayer = board.turn == self.player

        if ply == 0:
            if maxplayer:
                return self.heuristic(board)
            else:
                return -self.heuristic(board)
        else:
            bestScore = AI.MIN_INT if maxplayer else AI.MAX_INT

            if maxplayer:
                for mv in board.legal_moves:
                    board.push(mv)
                    hash = board.zobrist_hash()
                    if hash in self.table:
                        bestScore = self.table.lookup(hash, ply - 1)
                    else:
                        bestScore = max(bestScore, self.minimax(board, ply - 1, alpha, beta))
                        self.table.add(hash, bestScore, ply - 1)
                    board.pop()
                    alpha = max(alpha, bestScore)
                    if alpha >= beta:
                        break
            else:
                for mv in board.legal_moves:
                    board.push(mv)
                    hash = board.zobrist_hash()
                    if hash in self.table:
                        bestScore = self.table.lookup(hash, ply - 1)
                    else:
                        bestScore = min(bestScore, self.minimax(board, ply - 1, alpha, beta))
                        self.table.add(hash, bestScore, ply - 1)
                    board.pop()
                    beta = min(beta, bestScore)
                    if alpha >= beta:
                        break

            return bestScore

    def heuristic(self, board):
        score = 0
        for piece in chess.PIECE_TYPES:
            score += (len(board.pieces(piece, self.player)) - len(board.pieces(piece, not self.player))) * piece
        return score


if __name__ == '__main__':
    board = chess.Board()

    ai = AI(board, chess.WHITE)
    ai1 = AI(board, chess.BLACK)

    average = 0
    for i in range(10):
        start = timeit.default_timer()
        mv = ai.GetNextMove()
        end = timeit.default_timer() - start
        average += end
        print mv, end

        board.push(mv)

        start = timeit.default_timer()
        mv = ai1.GetNextMove()
        end = timeit.default_timer() - start
        print mv, end
        average += end
        board.push(mv)

    print board
    print average / 20
