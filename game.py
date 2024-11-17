import tkinter as tk
from tkinter import ttk

GRID_SIZE = (5, 5)


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.board = []

        super().__init__()
        self.title("nonogram")

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
                    lbl = tk.Label(board, text="hint")
                    lbl.grid(row=i, column=j, sticky="news")
                elif i == 0:
                    lbl = tk.Label(board, text="hint")
                    lbl.grid(row=i, column=j, sticky="news")
                else:
                    btn = tk.Button(board, command=lambda row=i, col=j: self.select(row, col))
                    btn.grid(row=i, column=j, sticky="news")
                    self.board.append(btn)


    def select(self, row, col):
        btn = self.board[(row - 1) * self.grid_size[1] + (col - 1)]
        if btn["text"]:
            btn.config(text="")
        else:
            btn.config(text="X")


if __name__ == "__main__":
    main()
