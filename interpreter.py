from parser import Program, Declaration, Assignment, IfStatement, Expression, Identifier, Number, Boolean, Printf, Block


class Interpreter:
    def __init__(self):
        self.symbol_table = {}  # initialize the symbol table
        self.output = []  # captured printf output

    def visit(self, node):
        """Dispatch method to call the appropriate visit method for each node."""
        if isinstance(node, Program):
            return self.visit_program(node)
        elif isinstance(node, Declaration):
            return self.visit_declaration(node)
        elif isinstance(node, Assignment):
            return self.visit_assignment(node)
        elif isinstance(node, IfStatement):
            return self.visit_if_statement(node)
        elif isinstance(node, Expression):
            return self.visit_expression(node)
        elif isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, Boolean):
            return self.visit_boolean(node)
        elif isinstance(node, Printf):
            return self.visit_printf(node)
        elif isinstance(node, Block):
            return self.visit_block(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def visit_program(self, node):
        """Evaluate the program (declarations + statements)."""
        for declaration in node.declarations:
            self.visit(declaration)
        for statement in node.statements:
            self.visit(statement)

    def visit_declaration(self, node):
        """Handle variable declarations."""
        # add the variable to the symbol table with an initial value of None
        self.symbol_table[node.identifier] = None

    def visit_assignment(self, node):
        """Handle variable assignment."""
        value = self.visit(node.expression)
        self.symbol_table[node.identifier] = value

    def visit_if_statement(self, node):
        """Handle if-else statement."""
        condition_value = self.visit(node.condition)
        if condition_value:  # if the condition evaluates to True
            self.visit(node.statement)
        elif node.else_statement:  # if there is an else block
            self.visit(node.else_statement)

    def visit_expression(self, node):
        """Evaluate expressions (like arithmetic and comparison)."""
        if node.operator == '!':
            right_value = self.visit(node.right)
            return not bool(right_value)

        left_value = self.visit(node.left) if node.left is not None else None

        if node.operator == '||':
            return bool(left_value) or bool(self.visit(node.right))
        if node.operator == '&&':
            return bool(left_value) and bool(self.visit(node.right))

        right_value = self.visit(node.right)

        if node.operator == '+':
            return left_value + right_value
        elif node.operator == '-':
            return left_value - right_value
        elif node.operator == '*':
            return left_value * right_value
        elif node.operator == '/':
            return left_value / right_value
        elif node.operator == '>':
            return left_value > right_value
        elif node.operator == '<':
            return left_value < right_value
        elif node.operator == '>=':
            return left_value >= right_value
        elif node.operator == '<=':
            return left_value <= right_value
        elif node.operator == '==':
            return left_value == right_value
        elif node.operator == '!=':
            return left_value != right_value
        else:
            raise ValueError(f"Unknown operator: {node.operator}")

    def visit_identifier(self, node):
        """Retrieve the value of a variable from the symbol table."""
        if node.name in self.symbol_table:
            return self.symbol_table[node.name]
        else:
            raise ValueError(f"Undefined variable: {node.name}")

    def visit_number(self, node):
        """Return the value of a number (literal)."""
        return node.value

    def visit_boolean(self, node):
        """Return boolean literal value."""
        return node.value

    def visit_printf(self, node):
        """Evaluate and print expression."""
        value = self.visit(node.expression)
        self.print_output(value)

    def visit_block(self, node):
        """Execute each statement in a block."""
        for stmt in node.statements:
            self.visit(stmt)

    def print_output(self, value):
        """Simulate the printf function."""
        self.output.append(str(value))
        print(value)