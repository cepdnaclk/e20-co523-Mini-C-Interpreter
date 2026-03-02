import unittest

from lexer import Lexer
from parser import Parser, Program, Declaration, Assignment, IfStatement, Block, Printf, Identifier, Expression


class ParserTests(unittest.TestCase):
    def test_parser_builds_expected_ast_shape(self):
        source = """
        int x;
        int y;
        x = 3;
        y = 2;
        if (!(x < 2 || y >= 2)) {
            x = x + 10;
        } else if (x == 3) {
            printf(x + y);
        }
        printf(x);
        """
        tokens = Lexer(source).scan()
        ast = Parser(tokens).parse_program()

        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.declarations), 2)
        self.assertTrue(all(isinstance(d, Declaration) for d in ast.declarations))

        self.assertEqual(len(ast.statements), 4)
        self.assertIsInstance(ast.statements[0], Assignment)
        self.assertEqual(ast.statements[0].identifier, 'x')
        self.assertIsInstance(ast.statements[1], Assignment)

        if_stmt = ast.statements[2]
        self.assertIsInstance(if_stmt, IfStatement)
        self.assertIsInstance(if_stmt.condition, Expression)
        self.assertEqual(if_stmt.condition.operator, '!')
        inner_condition = if_stmt.condition.right
        self.assertIsInstance(inner_condition, Expression)
        self.assertEqual(inner_condition.operator, '||')
        self.assertIsInstance(if_stmt.statement, Block)
        self.assertIsInstance(if_stmt.else_statement, IfStatement)

        nested_else = if_stmt.else_statement
        self.assertIsInstance(nested_else.statement, Block)
        self.assertEqual(len(nested_else.statement.statements), 1)
        printf_call = nested_else.statement.statements[0]
        self.assertIsInstance(printf_call, Printf)
        self.assertIsInstance(printf_call.expression, Expression)

        self.assertIsInstance(ast.statements[3], Printf)
        self.assertIsInstance(ast.statements[3].expression, Identifier)


if __name__ == "__main__":
    unittest.main()
