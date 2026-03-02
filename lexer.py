import re
from token import Token # importing the token class from token.py

KEYWORDS = {'if', 'else', 'while', 'for', 'def', 'return', 'int', 'float', 'string', 'bool', 'true', 'false', 'and', 'or', 'not', 'printf'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!'}
SYMBOLS = {'(', ')', '{', '}', '[', ']', ';', ','}

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
    
    def advance(self):
        """Advances the position in the source code and updates current_char."""
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None  # End of input
    
    def skip_whitespace(self):
        """Skips whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def scan_identifier(self):
        """Scans an identifier (variable name)."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def scan_number(self):
        """Scans a number (integer or float)."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char == '.':  # check for float
            result += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return float(result)  # return float if it has a decimal point
        
        return int(result)  # return int if it doesn't have a decimal point
    
    def scan(self):
        """Main function that scans the code and returns a list of tokens."""
        tokens = []
        while self.current_char is not None:
            self.skip_whitespace()

            if self.current_char is None:  # reached EOF after skipping whitespace
                break

            if self.current_char.isalpha():  # check for keywords or identifiers
                value = self.scan_identifier()
                if value in KEYWORDS:
                    tokens.append(Token('KEYWORD', value))
                else:
                    tokens.append(Token('IDENTIFIER', value))

            elif self.current_char.isdigit():  # check for numbers
                value = self.scan_number()
                tokens.append(Token('NUMBER', value))

            elif self.current_char in OPERATORS:  # check for operators
                value = self.current_char
                tokens.append(Token('OPERATOR', value))
                self.advance()

            elif self.current_char in SYMBOLS:  # check for symbols
                value = self.current_char
                tokens.append(Token('SYMBOL', value))
                self.advance()

            else:
                raise Exception(f"Invalid character {self.current_char}")

        return tokens
