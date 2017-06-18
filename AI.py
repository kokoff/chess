import chess
import chess.pgn
from chess import polyglot
from random import randint
import sys
import timeit
import os
import timeit


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


class RankedMove():
    def __init__(self, move, score):
        self.move = move
        self.score = score

    def __cmp__(self, other):
        return cmp(self.score, other.score)

    def __str__(self):
        return '(' + str(self.move) + ':' + str(self.score) + ')'

    def __repr__(self):
        return '(' + str(self.move) + ':' + str(self.score) + ')'


class MoveHeap:
    def __init__(self):
        self.heap = []

    def insert(self, move, score):
        temp = RankedMove(move, score)
        i = len(self.heap)
        self.heap.append(temp)

        while self.heap[i] > self.heap[i / 2]:
            self.heap[i] = self.heap[i / 2]
            i /= 2

        self.heap[i] = temp

    def __iter__(self):
        for x in self.heap:
            yield x.move

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        temp = '['
        for i in self.heap:
            temp += str(i) + ', '
        temp += ']'
        return str(self.heap)


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
        if self.head:
            self.head.prevNode = node
        else:
            self.tail = node
        self.head = node

    def pop(self):
        if self.is_empty():
            return None
        else:
            data = self.tail.data

            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.tail = self.tail.prevNode
                self.tail.nextNode = None

            return data

    def is_empty(self):
        return self.head is None and self.tail is None


class TranspositionTable:
    def __init__(self, capacity):
        self.table = {}
        self.access_list = FIFO()
        self.capacity = capacity

    def add(self, hash, score, current_ply):
        if hash in self.table and current_ply < self.table[hash][1]:
            pass
        else:
            tup = (score, current_ply)

            self.table[hash] = tup
            self.access_list.push(hash)

            if len(self.table) >= self.capacity:
                while not self.access_list.is_empty():
                    temp = self.access_list.pop()
                    if temp in self.table:
                        self.table.pop(temp)
                        break

    def lookup(self, hash, current_ply):
        if hash in self.table and self.table[hash][1] >= current_ply:
            return self.table[hash][0]
        else:
            return None

    def lookup_ply(self, hash):
        return self.table[hash][1]

    def __contains__(self, item):
        return item in self.table


class MoveHeap:
    def __init__(self):
        self.heap = []

    def insert(self, move, score):
        temp = RankedMove(move, score)
        i = len(self.heap)
        self.heap.append(temp)

        while self.heap[i] > self.heap[i / 2]:
            self.heap[i] = self.heap[i / 2]
            i /= 2

        self.heap[i] = temp

    def __iter__(self):
        for x in self.heap:
            yield x.move

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        temp = '['
        for i in self.heap:
            temp += str(i) + ', '
        temp += ']'
        return str(self.heap)


class MoveTable:
    def __init__(self, capacity):
        self.table = {}
        self.access_time = {}
        self.access_list = FIFO()
        self.capacity = capacity

    def add(self, hash, heap, ply):
        if not hash in self.table:
            self.table[hash] = (heap, ply)
            self.table[hash].insert(move, score)
            self.access_list.push(hash)
        else:
            self.table[hash].insert(move, score)

        if len(self.table) >= self.capacity:
            temp = self.access_list.pop()
            if temp in self.table:
                self.table.pop(temp)

    def moves(self, hash):
        if hash in self.table:
            return self.table[hash]
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
        self.ply = 3
        self.GetNextMove = self.getOpening
        self.trans_table = TranspositionTable(1000000)

    def getOpening(self):
        path = os.path.join('data', 'komodo.bin')
        reader = polyglot.MemoryMappedReader(path)
        self.GetNextMove = self.getMinimaxMove
        return reader.weighted_choice(self.board).move()

    def getMinimaxMove(self):
        bestMove = chess.Move.null()
        bestScore = AI.MIN_INT

        legal_moves = self.board.legal_moves

        for move in legal_moves:
            self.board.push(move)
            score = self.minimax(self.board, self.ply, AI.MIN_INT, AI.MAX_INT)
            self.board.pop()

            if bestScore <= score:
                bestMove = move
                bestScore = score

        assert (bestMove != chess.Move.null())
        return bestMove

    def minimax(self, board, ply, alpha, beta):
        maxplayer = board.turn == self.player
        hash = board.zobrist_hash()

        # Check if board already evaluated
        if hash in self.trans_table and self.trans_table.lookup_ply(hash) >= ply:
            return self.trans_table.lookup(hash, ply)

        elif ply == 0:
            if maxplayer:
                score = self.heuristic(board)
            else:
                score = -self.heuristic(board)

            return score
        else:
            bestScore = AI.MIN_INT if maxplayer else AI.MAX_INT

            legal_moves = board.legal_moves

            if maxplayer:
                for move in legal_moves:
                    board.push(move)
                    bestScore = max(bestScore, self.minimax(board, ply - 1, alpha, beta))
                    board.pop()

                    alpha = max(alpha, bestScore)
                    if alpha >= beta:
                        break
            else:
                for move in legal_moves:
                    board.push(move)
                    bestScore = min(bestScore, self.minimax(board, ply - 1, alpha, beta))
                    board.pop()

                    beta = min(beta, bestScore)
                    if alpha >= beta:
                        break

            # if there wasn't a prune add score to transposition table
            if alpha < beta:
                self.trans_table.add(hash, bestScore, ply)

            return bestScore

    def heuristic(self, board):
        score = 0
        for piece in chess.PIECE_TYPES:
            score += (len(board.pieces(piece, self.player)) - len(board.pieces(piece, not self.player))) * piece

        if board.is_game_over() and board.result() != '1/2-1/2':
            iwin = (board.result() is '1-0') is self.player
            score += 100 if iwin else -100
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
