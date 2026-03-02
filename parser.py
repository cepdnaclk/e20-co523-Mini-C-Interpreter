# abstract syntax tree (AST) node classes
class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"Program(declarations={self.declarations}, statements={self.statements})"


class Declaration(ASTNode):
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier

    def __repr__(self):
        return f"Declaration(type={self.type}, identifier={self.identifier})"


class Assignment(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"Assignment(identifier={self.identifier}, expression={self.expression})"


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class IfStatement(ASTNode):
    def __init__(self, condition, statement, else_statement=None):
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, statement={self.statement}, else_statement={self.else_statement})"


class Expression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Expression(left={self.left}, operator={self.operator}, right={self.right})"


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier(name={self.name})"


class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number(value={self.value})"


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block(statements={self.statements})"


# parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = 0
        self.advance()

    def advance(self):
        """Move to the next token."""
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            self.position += 1
        else:
            self.current_token = None

    def expect(self, token_type, value=None):
        """Ensure the current token matches the expected type (and optional value)."""
        if self.current_token and self.current_token.type == token_type and (value is None or self.current_token.value == value):
            self.advance()
        else:
            expected = f"{token_type}{' ' + value if value else ''}"
            raise SyntaxError(f"Expected {expected}, but got {self.current_token}")

    def parse_program(self):
        """Parse the entire program (declarations and statements)."""
        declarations = self.parse_declarations()
        statements = self.parse_statements()
        return Program(declarations, statements)

    def parse_declarations(self):
        """Parse variable declarations."""
        declarations = []
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value in ['int', 'float']:
            declarations.append(self.parse_declaration())
        return declarations

    def parse_declaration(self):
        """Parse a single variable declaration."""
        type_token = self.current_token.value
        self.advance()  # Move past the type token (int, float)
        identifier = self.current_token.value
        self.advance()  # Move past the identifier token
        self.expect('SYMBOL', ';')  # Expect the semicolon
        return Declaration(type_token, identifier)

    def parse_statements(self):
        """Parse statements in the program."""
        statements = []
        while self.current_token and self.current_token.type != 'EOF' and self.current_token.value != '}':
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        """Parse a single statement."""
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            return self.parse_if_statement()
        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment()
        elif self.current_token.type == 'SYMBOL' and self.current_token.value == '{':
            return self.parse_block()
        else:
            raise SyntaxError(f"Unexpected statement: {self.current_token}")

    def parse_if_statement(self):
        """Parse an if-else statement."""
        self.advance()  # Move past 'if'
        self.expect('SYMBOL', '(')  # Expect '('
        condition = self.parse_expression()
        self.expect('SYMBOL', ')')  # Expect ')'
        statement = self.parse_statement()
        else_statement = None
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.advance()  # Move past 'else'
            if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
                else_statement = self.parse_if_statement()
            else:
                else_statement = self.parse_statement()
        return IfStatement(condition, statement, else_statement)

    def parse_assignment(self):
        """Parse an assignment statement."""
        identifier = self.current_token.value
        self.advance()  # Move past the identifier
        self.expect('OPERATOR', '=')  # Expect '='
        expression = self.parse_expression()
        self.expect('SYMBOL', ';')  # Expect the semicolon
        return Assignment(identifier, expression)

    def parse_block(self):
        """Parse a brace-wrapped block of statements."""
        self.expect('SYMBOL', '{')
        statements = self.parse_statements()
        self.expect('SYMBOL', '}')
        return Block(statements)

    def parse_expression(self):
        """Parse expressions with logical OR precedence."""
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '||':
            operator = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            left = Expression(left, operator, right)
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '&&':
            operator = self.current_token.value
            self.advance()
            right = self.parse_equality()
            left = Expression(left, operator, right)
        return left

    def parse_equality(self):
        left = self.parse_relational()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['==', '!=']:
            operator = self.current_token.value
            self.advance()
            right = self.parse_relational()
            left = Expression(left, operator, right)
        return left

    def parse_relational(self):
        left = self.parse_additive()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['<', '>', '<=', '>=']:
            operator = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = Expression(left, operator, right)
        return left

    def parse_additive(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-']:
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = Expression(left, operator, right)
        return left

    def parse_term(self):
        """Parse terms (left operator right)."""
        left = self.parse_factor()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
            operator = self.current_token.value
            self.advance()  # Move past the operator
            right = self.parse_factor()
            left = Expression(left, operator, right)
        return left

    def parse_factor(self):
        """Parse factors (variables, numbers, or parentheses)."""
        if self.current_token.type == 'OPERATOR' and self.current_token.value in ['-', '!']:
            operator = self.current_token.value
            self.advance()
            right = self.parse_factor()
            return Expression(Number(0), operator, right) if operator == '-' else Expression(None, operator, right)
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return Number(value)
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        elif self.current_token.type == 'SYMBOL' and self.current_token.value == '(':
            self.advance()  # Move past '('
            expression = self.parse_expression()
            self.expect('SYMBOL', ')')  # Expect ')'
            return expression
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
