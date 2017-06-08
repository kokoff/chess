import chess
import chess.pgn
from chess import polyglot
from random import randint
import sys
import timeit
import os


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

        for move in self.board.legal_moves:
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

            if maxplayer:
                for mv in board.legal_moves:
                    board.push(mv)
                    bestScore = max(bestScore, self.minimax(board, ply - 1, alpha, beta))
                    board.pop()
                    alpha = max(alpha, bestScore)
                    if alpha >= beta:
                        break
            else:
                for mv in board.legal_moves:
                    board.push(mv)
                    bestScore = min(bestScore, self.minimax(board, ply - 1, alpha, beta))
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
