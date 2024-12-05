import numpy as np


class GenerationError(Exception):
    pass


def extract_value(node):
    return node.split("[")[1].split("]")[0]


class Generator:
    def __init__(self, terminals):
        self.terminals = terminals

        self.design = None
        self.grid_size = None
        self.title = ""
        self.hints = 0

    def run(self):
        i = 0

        while i < len(self.terminals):
            if self.terminals[i][0] == "NEW":
                i += 1
                specifier = self.terminals[i][1]
                i += 2
                if specifier == "design":
                    rows_counted = False
                    rows = 0
                    grid_specifiers = []
                    while self.terminals[i][0] == "GRID_SPECIFIER":
                        if not rows_counted:
                            rows += 1
                            if self.terminals[i][1].endswith("\\n"):
                                rows_counted = True
                        grid_specifiers.append(self.terminals[i][1])
                        i += 1
                    cols = len(grid_specifiers) // rows

                    self.grid_size = rows, cols
                    self.design = np.zeros((rows, cols))
                    for j, gs in enumerate(grid_specifiers):
                        if "#" in gs:
                            self.design[j // cols, j % cols] = 1
                    i += 1
                elif specifier == "random":
                    rows = self.terminals[i][1]
                    i += 2
                    cols = self.terminals[i][1]
                    self.grid_size = (rows, cols)
                    i += 2
            elif self.terminals[i][0] == "ATTRIBUTE":
                attribute = self.terminals[i][1]
                i += 2
                if attribute == "title":
                    self.title = self.terminals[i][1]
                elif attribute == "hints":
                    self.hints = int(self.terminals[i][1])
                i += 1

    def get_game_specs(self):
        return self.design, self.grid_size, self.title, self.hints

