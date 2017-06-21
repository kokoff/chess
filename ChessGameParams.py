#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessGameParams.py
 Description:  Creates a Tkinter dialog window to get game
	parameters.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from Tkinter import *


# from Tkinter import Tk,Frame,Label,Entry,Radiobutton,Button,StringVar,ANCHOR

class TkinterGameSetupParams:
    def __init__(self):
        self.root = Tk()
        self.root.title("Welcome to Python Chess!")
        self.frame = Frame(self.root)
        self.frame.pack()

        self.instructionMessage = StringVar()
        Label(self.frame, textvariable=self.instructionMessage).grid(row=0)
        self.instructionMessage.set("Please enter game options.")


        Label(self.frame, text="Type").grid(row=1, column=2)
        Label(self.frame, text="Search Depth").grid(row=1, column=4)

        Label(self.frame, text="Player 1 (White)").grid(row=2, column=0)

        self.tk_player1Type = StringVar()
        Radiobutton(self.frame, text="Human", variable=self.tk_player1Type, value="human").grid(row=2, column=2)
        Radiobutton(self.frame, text="AI", variable=self.tk_player1Type, value="AI").grid(row=2, column=3)
        self.tk_player1Type.set("human")

        self.entry_player1Depth = Entry(self.frame)
        self.entry_player1Depth.grid(row=2, column=4)
        self.entry_player1Depth.insert(ANCHOR, 4)

        Label(self.frame, text="Player 2 (Black)").grid(row=3, column=0)

        self.tk_player2Type = StringVar()
        Radiobutton(self.frame, text="Human", variable=self.tk_player2Type, value="human").grid(row=3, column=2)
        Radiobutton(self.frame, text="AI", variable=self.tk_player2Type, value="AI").grid(row=3, column=3)
        self.tk_player2Type.set("AI")

        self.entry_player2Depth = Entry(self.frame)
        self.entry_player2Depth.grid(row=3, column=4)
        self.entry_player2Depth.insert(ANCHOR, 4)

        Label(self.frame, text="AI with search depth less \nthan 1 behaves randomly").grid(row=4, column=4)

        b = Button(self.frame, text="Start the Game!", command=self.ok)
        b.grid(row=5, column=1)

    def ok(self):
        # self.player1Name = self.entry_player1Name.get()
        # hardcoded so that player 1 is always white
        self.player1Type = self.tk_player1Type.get()
        self.player1Depth = int(self.entry_player1Depth.get())
        self.player2Type = self.tk_player2Type.get()
        self.player2Depth = int(self.entry_player2Depth.get())

        self.frame.destroy()

    def GetGameSetupParams(self):
        self.root.wait_window(self.frame)  # waits for frame to be destroyed
        self.root.destroy()  # noticed that with "text" gui mode, the tk window stayed...this gets rid of it.
        return self.player1Type, self.player1Depth, self.player2Type, self.player2Depth


if __name__ == "__main__":
    d = TkinterGameSetupParams()
    x = d.GetGameSetupParams()
    print x
