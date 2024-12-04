import tkinter as tk
import numpy as np

class Application(tk.Tk):
    def __init__(self, grid_size, design):
        self.grid_size = grid_size
        self.board = []
        self.design = design
        self.scoring = np.zeros(grid_size)

        super().__init__()
        self.title("nonogram")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        board = tk.Frame(self)
        board.grid(row=0, column=0, stick="news")

        board.rowconfigure(tuple(range(self.grid_size[0] + 1)), weight=1)
        board.columnconfigure(tuple(range(self.grid_size[1] + 1)), weight=1)

        # create grid of buttons
        # TODO: calculate & print hints for each row / col
        for i in range(self.grid_size[0] + 1):
            for j in range(self.grid_size[1] + 1):
                if i == 0 and j == 0:
                    continue
                if j == 0:
                    lbl = tk.Label(board, text="hint")
                    lbl.grid(row=i, column=j, sticky="news")
                elif i == 0:
                    lbl = tk.Label(board, text="hint")
                    lbl.grid(row=i, column=j, sticky="news")
                else:
                    btn = tk.Button(board, command=lambda row=i, col=j: self.select(row, col))
                    btn.grid(row=i, column=j, sticky="news")
                    self.board.append(btn)
        submit = tk.Button(board, command=self.check, text='Submit')
        submit.grid(row=0, column=0, sticky="news")


    def select(self, row, col):
        row, col = row - 1, col - 1
        btn = self.board[row * self.grid_size[1] + col]
        if btn["text"]:
            btn.config(text="")
            self.scoring[row, col] = 0
        else:
            btn.config(text="X")
            self.scoring[row, col] = 1

    def check(self):
        # TODO: add logic for game complete / wrong
        print(np.array_equal(self.scoring, self.design))
