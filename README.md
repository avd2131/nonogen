# nonogen
Anna-Samsara Daefler (avd2131)

## Lexical Analysis
I developed a scanner that processes NonoGen source code and outputs a list of tokens. My scanner shows state
transitions with finite automata. Lexical errors in the input program are handled by the parser printing a message
to stderr and advancing to the next character, such that the user can view and correct all lexical errors in one pass.

### Lexical Grammar
The following list provides a lexical specification of rules in order of priority.

1) ('NEW', r'new')
2) ('SPECIFIER', r'design|random')
3) ('FUNCTION', r'print|play')
4) ('METHOD', r'title|hint')
5) ('GRID_SPECIFIER', r'\.|#')
6) ('ARROW', r'->')
7) ('EQUALS', r'=')
8) ('TIMES', r'x')
9) ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9]*')
10) ('INTEGER', r'\d+')
11) ('STRING', r'".*"')
12) ('LBRACE', r'{')
13) ('RBRACE', r'}') 
14) ('LPAREN', r'\(')
15) ('RPAREN', r'\)')
16) ('WHITESPACE', r'\s+')

### Executing Lexer
Use the shell script scan.sh to execute the lexer. Please make sure the system has Python3.

```./scan.sh <input_file>```

### Input Programs
Sample input programs can be found under samples/input_programs/ with their corresponding
expected token outputs under samples/outputs/. 

* Programs 1, 2, and 3 demonstrate different types of token parsing for valid input programs.
* Program 4 contains the illegal character '@'. The parser will handle this by skipping the character and printing a
message to the user that there is an unexpected character at the given position. 
* Program 5 has a string that is not terminated. The parser does not know where the string ends, so it prints a message
to the user that there is an unterminated string beginning at a certain position.