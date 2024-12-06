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

    print("CODE GENERATION")
    generator = Generator(terminals)
    generator.run()
    if generator.success:
        function_calls = generator.get_function_calls()
        symbol_table = generator.get_symbol_table()
        for function_call in function_calls:
            if function_call[0] == "print":
                identifier = function_call[1]
                game_specs = symbol_table[identifier]
                print(identifier, "{")
                for key, value in symbol_table[identifier].items():
                    print(key, "\n", value)
                print("}\n")
            elif function_call[0] == "play":
                identifier = function_call[1]
                print(f"Game '{identifier}' should open in a new window.")
                game_specs = symbol_table[identifier]
                app = Application(game_specs)
                app.mainloop()
    else:
        print("Code generation was not successful.")
        sys.exit(1)