# nonogen
Anna-Samsara Daefler (avd2131)

## Lexical Grammar
The following list provides a lexical specification of rules in order of priority.

1) ('NEW', r'new')
2) ('SPECIFIER', r'design|random')
3) ('FUNCTION', r'print|play')
4) ('METHOD', r'title|hint')
5) ('GRID_SPECIFIER', r'\.|#')
6) ('EQUALS', r'=')
7) ('TIMES', r'x')
8) ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9]*')
9) ('INTEGER', r'\d+')
10) ('STRING', r'".*"')
11) ('LBRACE', r'{')
12) ('RBRACE', r'}') 
13) ('LPAREN', r'\(')
14) ('RPAREN', r'\)')
15) ('WHITESPACE', r'\s+')