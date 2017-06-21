#! /usr/bin/env python
"""
 Project: Python Chess
 File name: PythonChessMain.py
 Description:  Chess for player vs. player, player vs. AI, or AI vs. AI.
	Uses Tkinter to get initial game parameters.  Uses Pygame to draw the 
	board and pieces and to get user mouse clicks.  Run with the "-h" option 
	to get full listing of available command line flags.  
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 *******
 This program is free software; you can redistribute it and/or modify 
 it under the terms of the GNU General Public License as published by 
 the Free Software Foundation; either version 2 of the License, or 
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
 for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 *******
 Version history:

 v 0.7 - 27 April 2009.  Dramatically lowered CPU usage by using 
   "pygame.event.wait()" rather than "pygame.event.get()" in
   ChessGUI_pygame.GetPlayerInput().
 
 v 0.6 - 20 April 2009.  Some compatibility fixes: 1) Class: instead of 
   Class(), 2) renamed *.PNG to *.png, 3) rendered text with antialias flag on.  
   Also changed exit() to sys.exit(0). (Thanks to tgfcoder from pygame website 
   for spotting these errors.)
 
 v 0.5 - 16 April 2009.  Added new AI functionality - created 
   "ChessAI_defense" and "ChessAI_offense."  Created PythonChessAIStats 
   class for collecting AI vs. AI stats.  Incorporated Python module 
   OptionParser for better command line parsing.
   
 v 0.4 - 14 April 2009.  Added better chess piece graphics from Wikimedia
   Commons.  Added a Tkinter dialog box (ChessGameParams.py) for getting
   the game setup parameters.  Converted to standard chess notation for 
   move reporting and added row/col labels around the board.
 
 v 0.3 - 06 April 2009.  Added pygame graphical interface.  Includes
   addition of ScrollingTextBox class.
   
 v 0.2 - 04 April 2009.  Broke up the program into classes that will
   hopefully facilitate easily incorporating graphics or AI play.
 
 v 0.1 - 01 April 2009.  Initial release.  Draws the board, accepts
   move commands from each player, checks for legal piece movement.
   Appropriately declares player in check or checkmate.

 Possible improvements:
   - Chess Rules additions, ie: Castling, En passant capture, Pawn Promotion
   - Better AI
   - Network play
   
"""

from ChessBoard import ChessBoard
from ChessAI import ChessAI_random, ChessAI_defense, ChessAI_offense
from ChessPlayer import ChessPlayer
from ChessGUI_text import ChessGUI_text
from ChessGUI_pygame import ChessGUI_pygame
from ChessRules import ChessRules
from ChessGameParams import TkinterGameSetupParams

from optparse import OptionParser
import time
import chess
from AI import RandomAI, AI
from utils import PIECE_NAMES


class PythonChessMain:
    def __init__(self, options):
        self.board = chess.Board()

        self.Gui = ChessGUI_pygame(1)
        self.ai_players = {}

    def SetUp(self):
        game_params = TkinterGameSetupParams()
        (player1Type, player1Depth, player2Type, player2Depth) = game_params.GetGameSetupParams()

        # print (player1Type, player1Depth, player2Type, player2Depth)
        # print player1Type is 'AI'

        if player1Type == 'AI':
            # print 'HIS'
            if player1Depth > 0:
                self.ai_players[chess.WHITE] = AI(self.board, chess.WHITE, player1Depth)
            else:
                self.ai_players[chess.WHITE] = RandomAI()

        if player2Type == 'AI':
            if player2Depth > 0:
                self.ai_players[chess.BLACK] = AI(self.board, chess.BLACK, player2Depth)
            else:
                self.ai_players[chess.BLACK] = RandomAI(self.board)

        print self.ai_players

    def MainLoop(self):
        while not self.board.is_game_over():
            board = self.board
            player = "WHITE" if board.turn else "BLACK"
            # hardcoded so that player 1 is always white
            self.Gui.PrintMessage("")
            baseMsg = "TURN %s - %s" % (board.fullmove_number, player)
            self.Gui.PrintMessage("-----%s-----" % baseMsg)
            self.Gui.Draw(board)
            if board.is_check():
                self.Gui.PrintMessage("Warning... " + player + " is in check!")

            # Get move from player
            if board.turn in self.ai_players:
                move = self.ai_players[board.turn].GetNextMove()
            else:
                move = self.Gui.GetPlayerInput(board)
                if board.piece_type_at(move.from_square) is chess.PAWN and move.to_square in chess.SquareSet(
                        chess.BB_RANK_8):
                    move.promotion = chess.QUEEN

            # Indicate if piece was captured
            if board.is_capture(move):
                self.Gui.PrintMessage(
                    PIECE_NAMES[board.piece_at(move.from_square).piece_type] + ' ' +
                    str(move) + '    ' + PIECE_NAMES[board.piece_at(move.to_square).piece_type] + ' was captured')
            else:
                self.Gui.PrintMessage(PIECE_NAMES[board.piece_at(move.from_square).piece_type] + ' '
                                      + str(move))

            board.push(move)

        # Check for end game conditions
        if board.is_game_over():
            self.Gui.PrintMessage('')
            winner = 'Black' if board.turn else 'White'
            draw_message = 'The game is a draw!'
            if board.is_checkmate():
                self.Gui.PrintMessage("Checkmate!")
                self.Gui.PrintMessage(winner + " won the game!")
            elif board.is_stalemate():
                self.Gui.PrintMessage("Stalemate!")
                self.Gui.PrintMessage(draw_message)
            elif board.is_insufficient_material():
                self.Gui.PrintMessage("Insufficient Material!")
                self.Gui.PrintMessage(draw_message)
            elif board.is_fivefold_repetition():
                self.Gui.PrintMessage("Fivefold Repetition!")
                self.Gui.PrintMessage(draw_message)
            elif board.is_seventyfive_moves():
                self.Gui.PrintMessage("Seventy Five Move Rule!")
                self.Gui.PrintMessage(draw_message)
            self.Gui.PrintMessage('Result: ' + board.result())
            self.Gui.EndGame(board)


parser = OptionParser()
parser.add_option("-s", dest="skip_setup",
                  action="store_true", default=False, help="Skip setup screen")

(options, args) = parser.parse_args()

game = PythonChessMain(options)
print options.skip_setup
if not options.skip_setup:
    game.SetUp()
else:
    game.ai_players[chess.BLACK] = AI(game.board, chess.BLACK)
game.MainLoop()
