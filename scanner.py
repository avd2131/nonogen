import sys

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string.replace("\n", "!")
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
                if self.current_char.isspace():
                    # ignore whitespace
                    self.advance()
                elif self.current_char == 'n':
                    self.tokens.append(('NEW', self.match_keyword('new')))
                elif self.current_char in ('d', 'r'):
                    self.tokens.append(self.specifier())
                elif self.current_char == 'p':
                    self.tokens.append(self.function())
                elif self.current_char in ('t', 'h'):
                    self.tokens.append(self.method())
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
                elif self.current_char.isalpha():
                    self.tokens.append(self.identifier())
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
                elif self.current_char == "!":
                    if self.tokens[-1][0] == 'GRID_SPECIFIER':
                        self.tokens[-1] = ('GRID_SPECIFIER', self.tokens[-1][1] + "!")
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

    # handle DFA state for recognizing keywords
    def match_keyword(self, keyword):
        for c in keyword:
            if self.current_char != c:
                raise ValueError(f"Unexpected character {self.current_char} in position {self.position}.")
            self.advance()
        return keyword

    # handle DFA state for recognizing specifier token
    def specifier(self):
        if self.current_char == 'd':
            keyword = 'design'
        elif self.current_char == 'r':
            keyword = 'random'

        return ('SPECIFIER', self.match_keyword(keyword))

    # handle DFA state for recognizing function token
    def function(self):
        self.advance()
        if self.current_char == 'r':
            match = 'print'
        elif self.current_char == 'l':
            match = 'play'
        else:
            raise ValueError(f"Unexpected character {self.current_char} in position {self.position}.")

        for c in match[1:]:
            if self.current_char != c:
                raise ValueError(f"Unexpected character {self.current_char} in position {self.position}.")
            self.advance()
        return ('FUNCTION', match)

    # handle DFA state for recognizing method token
    def method(self):
        if self.current_char == 't':
            keyword = 'title'
        elif self.current_char == 'h':
            keyword = 'hint'

        return ('METHOD', self.match_keyword(keyword))

    # handle DFA state for recognizing an identifier token
    def identifier(self):
        identifier_str = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
            identifier_str += self.current_char
            self.advance()
        return ('IDENTIFIER', identifier_str)

    # handle DFA state for recognizing an integer token
    def integer(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return ('INTEGER', num_str)

    # handle DFA state for recognizing a string token
    def string(self):
        start_pos = self.position
        str = ''
        self.advance()
        while self.current_char != '"':
            if self.current_char is None:
                raise ValueError(f"String beginning at position {start_pos} is not terminated.")
            str += self.current_char
            self.advance()
        self.advance()
        return ('STRING', str)

    # return list of tokens
    def get_tokens(self):
        return self.tokens