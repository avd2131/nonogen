import numpy as np
import random


class GenerationError(Exception):
    pass


def extract_value(node):
    return node.split("[")[1].split("]")[0]


class Generator:
    def __init__(self, terminals):
        self.terminals = terminals
        self.symbol_table = {}
        self.function_calls = []
        self.success = True

    def run(self):
        i = 0

        try:
            while i < len(self.terminals):
                if self.terminals[i][0] == "IDENTIFIER":
                    identifier = self.terminals[i][1]
                    i += 1
                    if self.terminals[i][0] == "EQUALS":
                        i += 2
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

                            grid_size = rows, cols
                            design = np.zeros((rows, cols))
                            for j, gs in enumerate(grid_specifiers):
                                if "#" in gs:
                                    design[j // cols, j % cols] = 1
                            self.symbol_table[identifier] = {"design": design, "grid_size": grid_size, "title": "", "hints": 0}
                            i += 1
                        elif specifier == "random":
                            rows = int(self.terminals[i][1])
                            i += 2
                            cols = int(self.terminals[i][1])
                            grid_size = (rows, cols)
                            i += 2
                            # generate random design
                            design = np.zeros((rows, cols))
                            for r in range(rows):
                                for c in range(cols):
                                    if bool(random.getrandbits(1)):
                                        design[r, c] = 1
                            self.symbol_table[identifier] = {"design": design, "grid_size": grid_size, "title": "",
                                                             "hints": 0}
                    elif self.terminals[i][0] == "ARROW":
                        i += 1
                        attribute = self.terminals[i][1]
                        i += 2
                        try:
                            if attribute == "title":
                                if self.terminals[i][0] == "STRING":
                                    self.symbol_table[identifier]["title"] = self.terminals[i][1]
                                else:
                                    raise GenerationError("Title needs to be a string.")
                            elif attribute == "hints":
                                if self.terminals[i][0] == "INTEGER":
                                    self.symbol_table[identifier]["hints"] = int(self.terminals[i][1])
                                else:
                                    raise GenerationError("Number of hints needs to be an integer.")
                        except KeyError:
                            raise GenerationError("Identifier used without definition.")
                        i += 1
                elif self.terminals[i][0] == "FUNCTION":
                    function = self.terminals[i][1]
                    i += 2
                    identifier = self.terminals[i][1]
                    self.function_calls.append((function, identifier))
                    i += 2
        except GenerationError as e:
            self.success = False
            print(e)

    def get_symbol_table(self):
        return self.symbol_table

    def get_function_calls(self):
        return self.function_calls

