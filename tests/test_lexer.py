import unittest

from lexer import Lexer


def tokens_to_pairs(tokens):
    return [(tok.type, tok.value) for tok in tokens]


class LexerTests(unittest.TestCase):
    def test_lexer_tokenizes_keywords_identifiers_numbers_and_ops(self):
        source = """
        int x;
        float y;
        x = 5;
        if (x >= 5 && y != 0) {
            printf(x);
        } else {
            x = x + 1;
        }
        """
        lexer = Lexer(source)
        tokens = tokens_to_pairs(lexer.scan())

        expected = [
            ('KEYWORD', 'int'), ('IDENTIFIER', 'x'), ('SYMBOL', ';'),
            ('KEYWORD', 'float'), ('IDENTIFIER', 'y'), ('SYMBOL', ';'),
            ('IDENTIFIER', 'x'), ('OPERATOR', '='), ('NUMBER', 5), ('SYMBOL', ';'),
            ('KEYWORD', 'if'), ('SYMBOL', '('), ('IDENTIFIER', 'x'), ('OPERATOR', '>='), ('NUMBER', 5),
            ('OPERATOR', '&&'), ('IDENTIFIER', 'y'), ('OPERATOR', '!='), ('NUMBER', 0), ('SYMBOL', ')'),
            ('SYMBOL', '{'), ('KEYWORD', 'printf'), ('SYMBOL', '('), ('IDENTIFIER', 'x'), ('SYMBOL', ')'), ('SYMBOL', ';'),
            ('SYMBOL', '}'), ('KEYWORD', 'else'), ('SYMBOL', '{'),
            ('IDENTIFIER', 'x'), ('OPERATOR', '='), ('IDENTIFIER', 'x'), ('OPERATOR', '+'), ('NUMBER', 1), ('SYMBOL', ';'),
            ('SYMBOL', '}'),
            ('EOF', None),
        ]

        self.assertEqual(tokens, expected)


if __name__ == "__main__":
    unittest.main()
