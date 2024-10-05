import sys

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.position = 0
        self.current_char = input_string[self.position] if input_string else None
        self.tokens = []

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
            # for debugging
            # print("current_char = ", self.current_char)
            if self.current_char.isspace():
                # ignore whitespace
                self.advance()
            elif self.current_char == 'n':
                self.tokens.append(self.new())
            elif self.current_char in ('d', 'r'):
                self.tokens.append(self.specifier())
            elif self.current_char == 'p':
                self.tokens.append(self.function())
            elif self.current_char in ('t', 'h'):
                self.tokens.append(self.method())
            elif self.current_char in ('.', '#'):
                self.tokens.append(('GRID_SPECIFIER', self.current_char))
                self.advance()
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
            else:
                raise ValueError(f"Unexpected character {self.current_char}")

    # handle DFA state for recognizing 'new' token
    def new(self):
        match = 'new'
        for c in match:
            if self.current_char != c:
                raise ValueError(f"Unexpected character {self.current_char}")
            self.advance()
        return ('NEW', match)

    # handle DFA state for recognizing specifier token
    def specifier(self):
        if self.current_char == 'd':
            match = 'design'
        elif self.current_char == 'r':
            match = 'random'
        else:
            raise ValueError(f"Unexpected character {self.current_char}")

        for c in match:
            if self.current_char != c:
                raise ValueError(f"Unexpected character {self.current_char}")
            self.advance()
        return ('SPECIFIER', match)

    # handle DFA state for recognizing function token
    def function(self):
        self.advance()
        if self.current_char == 'r':
            match = 'rint'
        elif self.current_char == 'l':
            match = 'lay'
        else:
            raise ValueError(f"Unexpected character {self.current_char}")

        for c in match:
            if self.current_char != c:
                raise ValueError(f"Unexpected character {self.current_char}")
            self.advance()
        return ('FUNCTION', match)

    # handle DFA state for recognizing method token
    def method(self):
        if self.current_char == 't':
            match = 'title'
        elif self.current_char == 'h':
            match = 'hint'
        else:
            raise ValueError(f"Unexpected character {self.current_char}")

        for c in match:
            if self.current_char != c:
                raise ValueError(f"Unexpected character {self.current_char}")
            self.advance()
        return ('METHOD', match)

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
        str = ''
        self.advance()
        while self.current_char != '"':
            if self.current_char is None:
                raise ValueError(f"String not terminated {str}")
            str += self.current_char
            self.advance()
        self.advance()
        return ('STRING', str)

    # return list of tokens
    def get_tokens(self):
        return self.tokens

file_path = sys.argv[1]
with open(file_path) as file:
    input_expression = file.read()
    lexer_dfa = Lexer(input_expression)
    lexer_dfa.run()
    tokens = lexer_dfa.get_tokens()
    for token in tokens:
        print(token)