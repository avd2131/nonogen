class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.position = 0
        self.current_char = input_string[self.position] if input_string else None
        self.tokens = []
        self.success = True

    # advance position pointer and update current character
    def advance(self):
        self.position += 1
        if self.position >= len(self.input_string):
            # end of input
            self.current_char = None
        else:
            self.current_char = self.input_string[self.position]

    # run DFA to tokenize input string
    def run(self):
        while self.current_char is not None:
            try:
                if self.current_char == "\n":
                    if self.tokens[-1][0] == 'GRID_SPECIFIER':
                        self.tokens[-1] = ('GRID_SPECIFIER', self.tokens[-1][1] + "\\n")
                    self.advance()
                elif self.current_char.isspace():
                    # ignore whitespace
                    self.advance()
                elif self.current_char.isalpha():
                    self.tokens.append(self.alpha())
                elif self.current_char in ('.', '#'):
                    self.tokens.append(('GRID_SPECIFIER', self.current_char))
                    self.advance()
                elif self.current_char == '-':
                    self.tokens.append(self.arrow())
                elif self.current_char == '=':
                    self.tokens.append(('EQUALS', '='))
                    self.advance()
                elif self.current_char == 'x':
                    self.tokens.append(('TIMES', 'x'))
                    self.advance()
                elif self.current_char.isdigit():
                    self.tokens.append(self.integer())
                elif self.current_char == '"':
                    self.tokens.append(self.string())
                elif self.current_char == '{':
                    self.tokens.append(('LBRACE', '{'))
                    self.advance()
                elif self.current_char == '}':
                    self.tokens.append(('RBRACE', '}'))
                    self.advance()
                elif self.current_char == '(':
                    self.tokens.append(('LPAREN', '('))
                    self.advance()
                elif self.current_char == ')':
                    self.tokens.append(('RPAREN', ')'))
                    self.advance()
                else:
                    raise ValueError(f"Unexpected character {self.current_char} in position {self.position}.")
            except ValueError as e:
                self.success = False
                print(e)
                self.advance()

    # handle DFA state for recognizing arrow token
    def arrow(self):
        self.advance()
        if self.current_char == '>':
            self.advance()
            return ('ARROW', '->')
        else:
            raise ValueError(f"Unexpected character {self.current_char} in position {self.position}.")

    # handle DFA state for recognizing alphanumeric tokens
    def alpha(self):
        token = ""
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
            token += self.current_char
            self.advance()

            if token == 'new':
                return self.tokens.append(('NEW', token))
            elif token in ('design', 'random'):
                return self.tokens.append(('SPECIFIER', token))
            elif token in ('print', 'play'):
                return self.tokens.append(('FUNCTION', token))
            elif token in ('title', 'hints'):
                return self.tokens.append(('ATTRIBUTE', token))

        return ('IDENTIFIER', token)

    # handle DFA state for recognizing an integer token
    def integer(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return 'INTEGER', num_str

    # handle DFA state for recognizing a string token
    def string(self):
        start_pos = self.position
        s = ''
        self.advance()
        while self.current_char != '"':
            if self.current_char is None:
                raise ValueError(f"String beginning at position {start_pos} is not terminated.")
            s += self.current_char
            self.advance()
        self.advance()
        return 'STRING', s

    # return list of tokens
    def get_tokens(self):
        return self.tokens
