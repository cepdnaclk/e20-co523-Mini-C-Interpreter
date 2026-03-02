# S.K.P. Methpura
# E/20/254
# Mini Project

from lexer import Lexer

source_code = """
int x;
x = 10;
if (x > 5) {
    printf(x);
}
"""

lexer = Lexer(source_code)
tokens = lexer.scan()

# Print all tokens
for token in tokens:
    print(token)