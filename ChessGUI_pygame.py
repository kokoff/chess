#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessGUI_pygame.py
 Description:  Uses pygame (http://www.pygame.org/) to draw the
	chess board, as well as get user input through mouse clicks.
	The chess tile graphics were taken from Wikimedia Commons, 
	http://commons.wikimedia.org/wiki/File:Chess_tile_pd.png
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

import os
import sys

import chess
import pygame
from pygame.locals import *

from ScrollingTextBox import ScrollingTextBox


class ChessGUI_pygame:
    def __init__(self, graphicStyle=1):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # should center pygame window on the screen
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((850, 500))
        self.boardStart_x = 50
        self.boardStart_y = 50
        pygame.display.set_caption('Python Chess')

        self.textBox = ScrollingTextBox(self.screen, 525, 825, 50, 450)
        self.LoadImages(graphicStyle)
        # pygame.font.init() - should be already called by pygame.init()
        self.fontDefault = pygame.font.Font(None, 20)

    def LoadImages(self, graphicStyle):
        if graphicStyle == 0:
            self.square_size = 50  # all images must be images 50 x 50 pixels
            self.white_square = pygame.image.load(os.path.join("images", "white_square.png")).convert()
            self.brown_square = pygame.image.load(os.path.join("images", "brown_square.png")).convert()
            self.cyan_square = pygame.image.load(os.path.join("images", "cyan_square.png")).convert()
            # "convert()" is supposed to help pygame display the images faster.  It seems to mess up transparency - makes it all black!
            # And, for this chess program, the images don't need to change that fast.
            self.black_pawn = pygame.image.load(os.path.join("images", "blackPawn.png"))
            self.black_rook = pygame.image.load(os.path.join("images", "blackRook.png"))
            self.black_knight = pygame.image.load(os.path.join("images", "blackKnight.png"))
            self.black_bishop = pygame.image.load(os.path.join("images", "blackBishop.png"))
            self.black_king = pygame.image.load(os.path.join("images", "blackKing.png"))
            self.black_queen = pygame.image.load(os.path.join("images", "blackQueen.png"))
            self.white_pawn = pygame.image.load(os.path.join("images", "whitePawn.png"))
            self.white_rook = pygame.image.load(os.path.join("images", "whiteRook.png"))
            self.white_knight = pygame.image.load(os.path.join("images", "whiteKnight.png"))
            self.white_bishop = pygame.image.load(os.path.join("images", "whiteBishop.png"))
            self.white_king = pygame.image.load(os.path.join("images", "whiteKing.png"))
            self.white_queen = pygame.image.load(os.path.join("images", "whiteQueen.png"))
        elif graphicStyle == 1:
            self.square_size = 50
            self.white_square = pygame.image.load(os.path.join("images", "white_square.png")).convert()
            self.brown_square = pygame.image.load(os.path.join("images", "brown_square.png")).convert()
            self.cyan_square = pygame.image.load(os.path.join("images", "cyan_square.png")).convert()

            self.black_pawn = pygame.image.load(os.path.join("images", "Chess_tile_pd.png")).convert()
            self.black_pawn = pygame.transform.scale(self.black_pawn, (self.square_size, self.square_size))
            self.black_rook = pygame.image.load(os.path.join("images", "Chess_tile_rd.png")).convert()
            self.black_rook = pygame.transform.scale(self.black_rook, (self.square_size, self.square_size))
            self.black_knight = pygame.image.load(os.path.join("images", "Chess_tile_nd.png")).convert()
            self.black_knight = pygame.transform.scale(self.black_knight, (self.square_size, self.square_size))
            self.black_bishop = pygame.image.load(os.path.join("images", "Chess_tile_bd.png")).convert()
            self.black_bishop = pygame.transform.scale(self.black_bishop, (self.square_size, self.square_size))
            self.black_king = pygame.image.load(os.path.join("images", "Chess_tile_kd.png")).convert()
            self.black_king = pygame.transform.scale(self.black_king, (self.square_size, self.square_size))
            self.black_queen = pygame.image.load(os.path.join("images", "Chess_tile_qd.png")).convert()
            self.black_queen = pygame.transform.scale(self.black_queen, (self.square_size, self.square_size))

            self.white_pawn = pygame.image.load(os.path.join("images", "Chess_tile_pl.png")).convert()
            self.white_pawn = pygame.transform.scale(self.white_pawn, (self.square_size, self.square_size))
            self.white_rook = pygame.image.load(os.path.join("images", "Chess_tile_rl.png")).convert()
            self.white_rook = pygame.transform.scale(self.white_rook, (self.square_size, self.square_size))
            self.white_knight = pygame.image.load(os.path.join("images", "Chess_tile_nl.png")).convert()
            self.white_knight = pygame.transform.scale(self.white_knight, (self.square_size, self.square_size))
            self.white_bishop = pygame.image.load(os.path.join("images", "Chess_tile_bl.png")).convert()
            self.white_bishop = pygame.transform.scale(self.white_bishop, (self.square_size, self.square_size))
            self.white_king = pygame.image.load(os.path.join("images", "Chess_tile_kl.png")).convert()
            self.white_king = pygame.transform.scale(self.white_king, (self.square_size, self.square_size))
            self.white_queen = pygame.image.load(os.path.join("images", "Chess_tile_ql.png")).convert()
            self.white_queen = pygame.transform.scale(self.white_queen, (self.square_size, self.square_size))

    def PrintMessage(self, message):
        # prints a string to the area to the right of the board
        self.textBox.Add(message)
        self.textBox.Draw()

    def ConvertToScreenCoords(self, chessSquare):
        # converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
        chessSquareTuple = (chess.square_file(chessSquare), chess.square_rank(chessSquare))
        (col, row) = chessSquareTuple
        col = col
        row = 7 - row
        screenX = self.boardStart_x + col * self.square_size
        screenY = self.boardStart_y + row * self.square_size
        return (screenX, screenY)

    def ConvertToChessCoords(self, screenPositionTuple):
        # converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
        # x is horizontal, y is vertical
        # (x=0,y=0) is upper-left corner of the screen
        (X, Y) = screenPositionTuple
        row = (Y - self.boardStart_y) / self.square_size
        col = (X - self.boardStart_x) / self.square_size
        return col, 7 - row

    def Draw(self, board, highlightSquares=[]):
        self.screen.fill((0, 0, 0))
        self.textBox.Draw()
        boardSize = 8  # board should be square.  boardSize should be always 8 for chess, but I dislike "magic numbers"

        # draw blank board
        brown = False
        for square in chess.SQUARES:
            (screenX, screenY) = self.ConvertToScreenCoords(square)
            if brown:
                self.screen.blit(self.brown_square, (screenX, screenY))

            else:
                self.screen.blit(self.white_square, (screenX, screenY))

            brown = not brown
            if (square + 1) % 8 == 0:
                brown = not brown

        # draw row/column labels around the edge of the board
        color = (255, 255, 255)  # white
        antialias = 1
        chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # top and bottom - display cols
        for c in range(boardSize):
            # render letters
            screenX = (c + 1) * self.square_size + self.square_size / 2
            screenY = self.square_size / 2
            renderedLine = self.fontDefault.render(chars[c], antialias, color)
            self.screen.blit(renderedLine, (screenX, screenY))
            screenY = (boardSize + 1) * self.square_size + self.square_size / 2
            renderedLine = self.fontDefault.render(chars[c], antialias, color)
            self.screen.blit(renderedLine, (screenX, screenY))

            # render numbers
            screenY = (c + 1) * self.square_size + self.square_size / 2
            screenX = self.square_size / 2
            renderedLine = self.fontDefault.render(str(8 - c), antialias, color)
            self.screen.blit(renderedLine, (screenX, screenY))
            screenX = (boardSize + 1) * self.square_size + self.square_size / 2
            renderedLine = self.fontDefault.render(str(8 - c), antialias, color)
            self.screen.blit(renderedLine, (screenX, screenY))

        # highlight squares if specified
        for square in highlightSquares:
            (screenX, screenY) = self.ConvertToScreenCoords(square)
            self.screen.blit(self.cyan_square, (screenX, screenY))

        # draw pieces
        for square in chess.SQUARES:
            (screenX, screenY) = self.ConvertToScreenCoords(square)
            piece = board.piece_at(square)
            if piece:
                if piece.color is chess.BLACK:
                    if piece.piece_type == chess.PAWN:
                        self.screen.blit(self.black_pawn, (screenX, screenY))
                    if piece.piece_type == chess.ROOK:
                        self.screen.blit(self.black_rook, (screenX, screenY))
                    if piece.piece_type == chess.KNIGHT:
                        self.screen.blit(self.black_knight, (screenX, screenY))
                    if piece.piece_type == chess.BISHOP:
                        self.screen.blit(self.black_bishop, (screenX, screenY))
                    if piece.piece_type == chess.QUEEN:
                        self.screen.blit(self.black_queen, (screenX, screenY))
                    if piece.piece_type == chess.KING:
                        self.screen.blit(self.black_king, (screenX, screenY))
                if piece.color == chess.WHITE:
                    if piece.piece_type == chess.PAWN:
                        self.screen.blit(self.white_pawn, (screenX, screenY))
                    if piece.piece_type == chess.ROOK:
                        self.screen.blit(self.white_rook, (screenX, screenY))
                    if piece.piece_type == chess.KNIGHT:
                        self.screen.blit(self.white_knight, (screenX, screenY))
                    if piece.piece_type == chess.BISHOP:
                        self.screen.blit(self.white_bishop, (screenX, screenY))
                    if piece.piece_type == chess.QUEEN:
                        self.screen.blit(self.white_queen, (screenX, screenY))
                    if piece.piece_type == chess.KING:
                        self.screen.blit(self.white_king, (screenX, screenY))

        pygame.display.flip()

    def EndGame(self, board):
        self.PrintMessage("Press any key to exit.")
        self.Draw(board)  # draw board to show end game status
        pygame.event.set_blocked(MOUSEMOTION)
        while 1:
            e = pygame.event.wait()
            if e.type is KEYDOWN:
                pygame.quit()
                sys.exit(0)
            if e.type is QUIT:
                pygame.quit()
                sys.exit(0)

    def GetPlayerInput(self, board):
        # returns ((from_row,from_col),(to_row,to_col))
        fromSquareChosen = 0
        toSquareChosen = 0
        while not fromSquareChosen or not toSquareChosen:
            squareClicked = -1
            pygame.event.set_blocked(MOUSEMOTION)
            e = pygame.event.wait()
            if e.type is KEYDOWN:
                if e.key is K_ESCAPE:
                    fromSquareChosen = 0
                    fromTuple = []
            if e.type is MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                coords = self.ConvertToChessCoords((mouseX, mouseY))
                if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
                    squareClicked = []  # not a valid chess square
                else:
                    squareClicked = chess.square(coords[0], coords[1])
            if e.type is QUIT:  # the "x" kill button
                pygame.quit()
                sys.exit(0)

            if not fromSquareChosen and not toSquareChosen:
                self.Draw(board)
                if squareClicked != -1:
                    allowedSquares = []
                    if board.piece_at(squareClicked) and board.turn == board.piece_at(squareClicked).color:
                        for move in board.legal_moves:
                            if move.from_square == squareClicked:
                                allowedSquares.append(move.to_square)
                        if len(allowedSquares) > 0:
                            fromSquareChosen = 1
                            fromSquare = squareClicked

            elif fromSquareChosen and not toSquareChosen:
                possibleDestinations = allowedSquares
                self.Draw(board, possibleDestinations)
                if squareClicked != -1:

                    if squareClicked in possibleDestinations:
                        toSquareChosen = 1
                        toSquare = squareClicked

                    elif board.piece_at(squareClicked) and board.turn == board.piece_at(squareClicked).color:
                        allowedDestinationSquares = []
                        for move in board.legal_moves:
                            if move.from_square == squareClicked:
                                allowedDestinationSquares.append(move.to_square)

                        if squareClicked == fromSquare:
                            fromSquareChosen = 0
                        elif len(allowedDestinationSquares) > 0:
                            fromSquareChosen = 1
                            fromSquare = squareClicked
                            possibleDestinations = allowedDestinationSquares
                            allowedSquares = allowedDestinationSquares
                            self.Draw(board, possibleDestinations)
                        else:
                            fromSquareChosen = 0  # piece is of own color, but no possible moves
                    else:  # blank square or opposite color piece not in possible destinations clicked
                        fromSquareChosen = 0

        return chess.Move(fromSquare, toSquare)

    def GetClickedSquare(self, mouseX, mouseY):
        # test function
        print "User clicked screen position x =", mouseX, "y =", mouseY
        row, col = self.ConvertToChessCoords((mouseX, mouseY))
        if col < 8 and col >= 0 and row < 8 and row >= 0:
            print "  Chess board units row =", row, "col =", col
            print "Square Number", chess.square(row, col)
            return chess.square(row, col)

    def TestRoutine(self, board):
        # test function
        pygame.event.set_blocked(MOUSEMOTION)
        while 1:
            e = pygame.event.wait()
            if e.type is QUIT:
                return
            if e.type is KEYDOWN:

                if e.key is K_ESCAPE:
                    pygame.quit()
                    return
            if e.type is MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # x is horizontal, y is vertical
                # (x=0,y=0) is upper-left corner of the screen
                self.GetClickedSquare(mouseX, mouseY)
                print "Piece", board.piece_at(self.GetClickedSquare(mouseX, mouseY))


if __name__ == "__main__":
    # try out some development / testing stuff if this file is run directly

    testBoard = chess.Board()

    validSquares = [(5, 2), (1, 1), (1, 5), (7, 6)]

    game = ChessGUI_pygame()
    game.Draw(testBoard)
    while 1:
        print game.GetPlayerInput(testBoard)
    game.TestRoutine(testBoard)
