import sys

class LexicalError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.lookahead = tokens[self.position] if tokens else None
        self.terminals = []
        self.derivation = ""
        self.level = 0
        self.success = True

    def advance(self):
        self.position += 1
        if self.position >= len(self.tokens):
            self.lookahead = None
        else:
            self.lookahead = self.tokens[self.position]

    def run(self):
        while self.lookahead is not None:
            try:
                self.S()
            except LexicalError as e:
                self.success = False
                print(e)
                # resume parsing with next statement
                while self.lookahead is not None and self.lookahead not in ["IDENTIFIER", "FUNCTION"]:
                    self.advance()

    def term(self, terminal):
        if self.lookahead[0] == terminal:
            self.terminals.append(self.lookahead)
            self.derivation += '\t' * self.level + self.lookahead[0] + '\n'
            self.advance()
            return True
        return False

    def S(self):
        self.derivation += "S\n"
        self.level += 1
        if self.term("IDENTIFIER"):
            self.A()
        elif self.term("FUNCTION") and self.term("LPAREN") and self.term("IDENTIFIER") and self.term("RPAREN"):
            pass
        else:
            raise LexicalError(f"Unexpected {self.lookahead[0]} '{self.lookahead[1]}' at position {self.position}.\n"
                               f"Expected statement to start with IDENTIFIER or FUNCTION.")
        self.level -= 1

    def A(self):
        self.derivation += '\t' * self.level + "A\n"
        self.level += 1
        if self.term("EQUALS") and self.term("NEW") and self.term("SPECIFIER") and self.term("LBRACE"):
            self.B()
            self.term("RBRACE")
        elif self.term("ARROW") and self.term("METHOD") and self.term("LPAREN"):
            self.D()
            self.term("RPAREN")
        else:
            raise LexicalError(f"Unexpected {self.lookahead[0]} '{self.lookahead[1]}' at position {self.position}.\n"
                               f"Expected IDENTIFIER to be followed by EQUALS or ARROW.")
        self.level -= 1

    def B(self):
        self.derivation += '\t' * self.level + "B\n"
        self.level += 1
        if self.term("GRID_SPECIFIER"):
            while self.term("GRID_SPECIFIER"):
                pass
        elif self.term("INTEGER") and self.term("TIMES") and self.term("INTEGER"):
            pass
        else:
            raise LexicalError(f"Unexpected {self.lookahead[0]} '{self.lookahead[1]}' at position {self.position}.\n"
                               f"Expected GRID_SPECIFIER or grid size (INTEGER TIMES INTEGER) following creation of game object.")
        self.level -= 1

    def D(self):
        self.derivation += '\t' * self.level + "D\n"
        self.level += 1
        if self.term("STRING") or self.term("INTEGER"):
            pass
        else:
            raise LexicalError(f"Unexpected {self.lookahead[0]} '{self.lookahead[1]}' at position {self.position}.\n"
                               f"Expected STRING or INTEGER as argument for method.")
        self.level -= 1

    def get_terminals(self):
        return self.terminals

    def get_derivation(self):
        return self.derivation