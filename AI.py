import chess
import chess.pgn
from chess import polyglot
from random import randint
import sys
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


class MoveTree:


# class MoveHeapList:
#     def __init__(self, ply):
#         self.ply = ply + 1
#         self.currentTree = {i: MoveHeap() for i in range(self.ply)}
#         self.nextTree = {i: MoveHeap() for i in range(self.ply)}
#
#     def add(self, move, score, ply):
#         self.dic[ply].insert(move, score)
#
#     def legal_moves(self, ply):
#         return self.dic[ply]
#
#     def reshufle(self, num=2):
#         i = self.ply
#         while i - num >= 0:
#             self.dic[i] = self.dic1[i - num]
#             self.dic1[i-num] = MoveHeap()
#             i -= 1
#
#         while i >= 0:
#             self.dic[i] = MoveHeap()
#             self.dic1[i] = MoveHeap()
#             i -= 1
#
#     def __str__(self):
#         temp = '[\n'
#         for i in range(self.ply):
#             temp += 'ply = ' + str(i) + ', ' + str(self.dic[i]) + '\n'
#         temp += ']\n'
#         temp += '[\n'
#         for i in range(self.ply):
#             temp += 'ply = ' + str(i) + ', ' + str(self.dic1[i]) + '\n'
#         temp += ']\n'
#         return temp


class AI:
    MIN_INT = - sys.maxint - 1
    MAX_INT = sys.maxint

    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.ply = 3
        self.GetNextMove = self.getOpening

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

        if ply == 0:
            if maxplayer:
                return self.heuristic(board)
            else:
                return -self.heuristic(board)
        else:
            bestScore = AI.MIN_INT if maxplayer else AI.MAX_INT

            legal_moves = board.legal_moves

            if maxplayer:
                for mv in legal_moves:
                    # evaluate best score
                    board.push(mv)
                    score = self.minimax(board, ply - 1, alpha, beta)
                    bestScore = max(bestScore, score)
                    board.pop()

                    # alpha beta pruning
                    alpha = max(alpha, bestScore)
                    if alpha >= beta:
                        break
            else:
                for mv in legal_moves:
                    # evaluate best score
                    board.push(mv)
                    score = self.minimax(board, ply - 1, alpha, beta)
                    bestScore = min(bestScore, score)
                    board.pop()

                    # alpha beta pruning
                    beta = min(beta, bestScore)
                    if alpha >= beta:
                        break
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

    # print board.fen()
    # board = chess.Board("2k5/8/8/8/3rrr2/8/4K3/8 w KQkq - 0 1")
    # print chess.WHITE
    # print board.result() == '1-0'
    # print ai.heuristic(board)
    # print ai1.heuristic(board)
    # sys.exit()

    for i in range(10):
        start = timeit.default_timer()
        mv = ai.GetNextMove()
        end = timeit.default_timer() - start
        print mv, end

        board.push(mv)

        start = timeit.default_timer()
        mv = ai1.GetNextMove()
        end = timeit.default_timer() - start
        print mv, end
        board.push(mv)

    print board

    # nullMove = chess.Move.null()
    # mvl = MoveHeapList(4)
    # mvl.add(nullMove, 1, 0)
    # mvl.add(nullMove, 1, 0)
    # mvl.add(nullMove, 2, 1)
    # mvl.add(nullMove, 2, 1)
    # mvl.add(nullMove, 3, 2)
    # mvl.add(nullMove, 3, 2)
    # mvl.add(nullMove, 4, 3)
    # mvl.add(nullMove, 4, 3)
    # print mvl
    # mvl.reshufle(1)
    #
    # print mvl
