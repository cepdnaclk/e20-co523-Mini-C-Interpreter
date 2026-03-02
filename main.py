# S.K.P. Methpura
# E/20/254
# Mini Project

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

source_code = """
int x;
x = 10;
if (x > 5) {
    x = x - 1;
} else if (x == 5) {
    x = x + 2;
} else {
    x = x + 3;
}
printf(x);
"""
# initialize the lexer with source code
lexer = Lexer(source_code)
tokens = lexer.scan()

# initialize the parser with the list of tokens
parser = Parser(tokens)

# parse the tokens into as Abstract Syntax Tree (AST)
ast = parser.parse_program()

interpreter = Interpreter()
interpreter.visit(ast)

print("Symbol table:", interpreter.symbol_table)
print("Output:", interpreter.output)