import chess
import chess.pgn
from random import randint

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

    def __init__(self, board, player):
        self.board = board
        self.game = chess.pgn.Game.from_board(board)
        self.player = player

    def GetNextMove(self):
        (move, score) = self.minimax(self.board, 2)
        return move

    def minimax(self, board, ply):
        if ply == 0:
            move = board.peek()
            score = self.heuristic(board)
            return move, score
        else:
            ply -= 1
            maxplayer = board.turn == self.player

            for mv in board.legal_moves:
                board.push(mv)
                (bestMove, bestScore) = self.minimax(board, ply)
                bestMove = mv
                bestMove = board.pop()

            for mv in board.legal_moves:
                board.push(mv)
                (move, score) = self.minimax(board, ply)
                move = board.pop()
                print "Thinking"

                if maxplayer and score >= bestScore:
                    bestScore = score
                    bestMove = move
                elif not maxplayer and score <= bestScore:
                    bestScore = score
                    bestMove = move

            return bestMove, bestScore

    def heuristic(self, board):
        score = 0
        for square in chess.SQUARES:
            if board.piece_at(square) and board.piece_at(square).color == self.player:
                score += board.piece_at(square).piece_type
            elif board.piece_at(square) and board.piece_at(square).color != self.player:
                score -= board.piece_at(square).piece_type
        return score

if __name__ == '__main__':
    board = chess.Board()
    game = chess.pgn.Game()

    ai = AI(board, chess.WHITE)
    x = ai.GetNextMove()

    print x
