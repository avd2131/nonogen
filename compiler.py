import sys

from parser import Parser
from scanner import Lexer

file_path = sys.argv[1]
with open(file_path) as file:
    input_expression = file.read()

    print("LEXICAL ANALYSIS")
    lexer_dfa = Lexer(input_expression)
    lexer_dfa.run()
    tokens = lexer_dfa.get_tokens()

    if lexer_dfa.success:
        for token in tokens:
            print(f"<{token[0]}, '{token[1]}'>")
    else:
        print("Parsing was not successful.")
        sys.exit(1)
    print("")

    print("SYNTACTIC ANALYSIS")
    parser = Parser(tokens)
    parser.run()
    derivation = parser.get_derivation()
    print(derivation)
    print("")
