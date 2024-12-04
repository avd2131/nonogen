import sys

from scanner import Lexer
from parser import Parser
from generator import Generator
from game import Application

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
        print("Scanning was not successful.")
        sys.exit(1)
    print("")

    print("SYNTACTIC ANALYSIS")
    parser = Parser(tokens)
    parser.run()
    derivation = parser.get_derivation()
    terminals = parser.get_terminals()

    if parser.success:
        print(derivation)
    else:
        print("Parsing was not successful.")
        sys.exit(1)
    print("")

    generator = Generator(terminals)
    generator.run()
    grid_size, design = generator.get_grid_size(), generator.get_design()
    app = Application(grid_size, design)
    app.mainloop()