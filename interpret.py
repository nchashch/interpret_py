#!/bin/python
from lexer import Lexer
from parser import Parser
from terminals import terminals
from shuntingyard import shunting_yard
from rpn_eval import rpn_eval

class Interpreter:
    def __init__(self):
        self.lexer = Lexer(terminals)
        self.parser = Parser()
        self.variables = dict()
    def interpret(self, text):
        tokens = list(self.lexer.tokenize(text))
        parsed, rest = self.parser.parse(tokens)
        if rest:
            print('Failed to parse')
            return
        # self.parser.print(parsed)
        # print()
        self._interpret(parsed)

    def _interpret(self, parsed):
        for p in parsed:
            if p[0] == 'while_stmt':
                condition = p[1][0]
                body = p[1][1]
                print(condition)
                print(self._check_condition(condition))
                print(self.variables)
                while self._check_condition(condition):
                    self._interpret(body)
                    print(self.variables)
            elif p[0] == 'arith_stmt':
                arith_stmt = p[1]
                ident = arith_stmt[0]
                expr = arith_stmt[1]
                rpn_tokens = shunting_yard(expr)
                result = rpn_eval(rpn_tokens, self.variables)
                self.variables[ident[1]] = result

    def _check_condition(self, condition):
        lhs_t = condition[0]
        op_t = condition[1]
        op = op_t[0]
        rhs_t = condition[2]
        if lhs_t[0] == 'NUM':
            lhs = int(lhs_t[1])
        elif lhs_t[0] == 'IDENT':
            lhs = self.variables[lhs_t[1]]
        if rhs_t[0] == 'NUM':
            rhs = int(rhs_t[1])
        elif rhs_t[0] == 'IDENT':
            rhs = self.variables[rhs_t[1]]
        result = {
            'GT': lhs > rhs,
            'GE': lhs >= rhs,
            'EQ': lhs == rhs,
            'LE': lhs <= rhs,
            'LT': lhs < rhs,
        }
        return result[op]
def main():
    interpreter = Interpreter()
    text = '''
    b = 5;
    a = 1;
    i = 0;
    k = 0;
    while i < b {
        i = i + 1;
        j = 0;
        while j < 2 {
            j = j + 1;
            a = a * 2;
            k = k + 1;
        }
    }
    '''
    interpreter.interpret(text)

if __name__ == '__main__':
    main()
