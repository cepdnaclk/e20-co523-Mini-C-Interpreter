# C-Lite Interpreter

Minimal interpreter for a C-like toy language with lexer → parser → AST → interpreter. Supports int/float decls, arithmetic, comparisons, logical ops, if/else, and `printf(expr);`.

## Project structure

- lexer.py — converts source code to tokens (keywords/operators/symbols/numbers) and emits EOF
- parser.py — recursive-descent parser building AST nodes (Program, Declaration, Assignment, If/else, Block, Expression, Boolean, Number, Identifier, Printf)
- interpreter.py — walks AST, maintains symbol table, evaluates expressions/control flow, captures printf output
- clite_token.py — Token class (renamed to avoid stdlib shadowing)
- main.py — demo program wiring lexer → parser → interpreter
- tests/ — unittest suites for lexer, parser, interpreter behavior

## Requirements

- Python 3.11+ (tested with Python 3.13)

## Running the demo

```bash
python main.py
```

Outputs the final symbol table and any `printf` results.

## Running tests

```bash
python -m unittest discover -s tests
```

## Usage notes

- `printf` is a statement: `printf(expr);` prints the expression (newline) and also records it in `Interpreter.output`.
- Logical ops: `&&`, `||`, `!`; comparisons: `== != < <= > >=`; arithmetic: `+ - * /`.
- Booleans use `true`/`false`; numbers are int or float; identifiers use letters/digits/underscore.
