import tkinter as tk
import numpy as np
import random

def calc_label(row):
    label = ""
    count = 0

    for g in row:
        if g == 1:
            count += 1
        if g == 0 and count > 0:
            if label:
                label += ", "
            label += str(count)
            count = 0
    if count > 0:
        if label:
            label += ", "
        label += str(count)

    return label

class Application(tk.Tk):
    def __init__(self, game_specs):
        self.design, self.grid_size, self.game_title, self.hints = game_specs

        self.board = []
        self.scoring = np.zeros(self.grid_size)
        self.status = None

        super().__init__()
        self.title(self.game_title)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        board = tk.Frame(self)
        board.grid(row=0, column=0, stick="news")

        board.rowconfigure(tuple(range(self.grid_size[0] + 1)), weight=1)
        board.columnconfigure(tuple(range(self.grid_size[1] + 1)), weight=1)

        # create grid of buttons
        for i in range(self.grid_size[0] + 1):
            for j in range(self.grid_size[1] + 1):
                if i == 0 and j == 0:
                    continue
                if j == 0:
                    lbl = tk.Label(board, text=calc_label(self.design[i - 1]))
                    lbl.grid(row=i, column=j, sticky="news")
                elif i == 0:
                    lbl = tk.Label(board, text=calc_label(self.design[:, j - 1]))
                    lbl.grid(row=i, column=j, sticky="news")
                else:
                    btn = tk.Button(board, command=lambda row=i, col=j: self.select(row, col))
                    btn.grid(row=i, column=j, sticky="news")
                    self.board.append(btn)
        submit = tk.Button(board, command=lambda: self.check(board), text='Submit')
        submit.grid(row=0, column=0, sticky="news")

        # give number of requested hints
        if self.hints > 0:
            # randomly select n boxes to give as hints
            all = np.argwhere(self.design == 1).tolist()
            hints = random.sample(all, self.hints)
            print(hints)
            for h in hints:
                self.select(h[0] + 1, h[1] + 1)

    def select(self, row, col):
        if self.status and self.status["text"] == "Try again...":
            self.status.destroy()
            self.status = None

        row, col = row - 1, col - 1
        btn = self.board[row * self.grid_size[1] + col]
        if btn["text"]:
            btn.config(text="")
            self.scoring[row, col] = 0
        else:
            btn.config(text="X")
            self.scoring[row, col] = 1

    def check(self, board):
        if np.array_equal(self.scoring, self.design):
            self.status = tk.Label(board, text="Correct!", font=("Arial", 50))
            self.status.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.status = tk.Label(board, text="Try again...", font=("Arial", 50))
            self.status.place(relx=0.5, rely=0.5, anchor="center")
