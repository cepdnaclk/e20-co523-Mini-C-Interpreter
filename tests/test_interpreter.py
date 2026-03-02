import unittest

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_program(source):
    tokens = Lexer(source).scan()
    parser = Parser(tokens)
    ast = parser.parse_program()
    interpreter = Interpreter()
    interpreter.visit(ast)
    return interpreter


class InterpreterTests(unittest.TestCase):
    def test_interpreter_executes_branches_and_printf(self):
        source = """
        int x;
        int y;
        x = 1 + 2 * 3;
        y = 4;
        if (x >= 7 && !(y < 3)) {
            printf(x);
            x = x - 2;
        } else {
            x = x + 100;
        }
        printf(x == 5);
        printf(x >= y);
        """
        interpreter = run_program(source)

        self.assertEqual(interpreter.symbol_table['x'], 5)
        self.assertEqual(interpreter.symbol_table['y'], 4)
        self.assertEqual(interpreter.output, ['7', 'True', 'True'])


if __name__ == "__main__":
    unittest.main()
