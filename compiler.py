import sys

from scanner import Lexer
from parser import Parser
from generator import Generator
from game import Application

file_path = sys.argv[1]
with open(file_path) as file:
    input_expression = file.read()

    lexer_dfa = Lexer(input_expression)
    lexer_dfa.run()
    tokens = lexer_dfa.get_tokens()

    if not lexer_dfa.success:
        print("Lexical analysis was not successful.")
        sys.exit(1)

    parser = Parser(tokens)
    parser.run()
    derivation = parser.get_derivation()
    terminals = parser.get_terminals()

    if not parser.success:
        print("Syntactic analysis was not successful.")
        sys.exit(1)

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