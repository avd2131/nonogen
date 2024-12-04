import numpy as np

class GenerationError(Exception):
    pass

class Generator:
    def __init__(self, ast):
        self.design = None
        self.grid_size = None
        self.ast = ast
        self.symbol_table = {}
        self.generated_code = ""

    def extract_value(self, node):
        return node.split("[")[1].split("]")[0]

    def run(self):
        nodes = self.ast.split("\n")
        nodes = [node for node in nodes if len(node.strip()) != 1]
        i = 0

        while i < len(nodes):
            if "IDENTIFIER" in nodes[i]:
                id_name = self.extract_value(nodes[i])
                i += 1
                if "EQUALS" in nodes[i]:
                    self.symbol_table[id_name] = {}
                    i += 4
                    if "GRID_SPECIFIER" in nodes[i]:
                        design = []
                        rows = 0
                        rows_counted = False
                        while "GRID_SPECIFIER" in nodes[i]:
                            if not rows_counted:
                                rows += 1
                                if "!" in nodes[i]:
                                    rows_counted = True
                            design.append(self.extract_value(nodes[i]))
                            i += 1
                        cols = len(design) // rows
                        self.design = np.zeros((rows, cols))
                        for j, x in enumerate(design):
                            if "#" in x:
                                self.design[j // cols, j % cols] = 1
                        self.grid_size = rows, cols
                        i += 1
                    elif "INTEGER" in nodes[i]:
                        self.symbol_table[id_name]["design"] = "random"
                        rows = nodes[i]
                        i += 2
                        cols = nodes[i]
                        self.symbol_table[id_name]["grid_size"] = (rows, cols)
                        i += 2
                elif "ARROW" in nodes[i]:
                    i += 1
                    method_name = self.extract_value(nodes[i])
                    i += 2
                    argument = self.extract_value(nodes[i])
                    if method_name == "title":
                        self.symbol_table[id_name]["title"] = argument
                    elif method_name == "hint":
                        self.symbol_table[id_name]["hint"] = argument
                    i += 2
            elif "FUNCTION" in nodes[i]:
                function_name = self.extract_value(nodes[i])
                i += 2
                id_name = self.extract_value(nodes[i])
                i += 2
                if function_name == "print":
                    continue
                elif function_name == "play":
                    i += 3
            else:
                raise GenerationError()

    def get_design(self):
        return self.design

    def get_grid_size(self):
        return self.grid_size

