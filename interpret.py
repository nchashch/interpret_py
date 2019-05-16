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
        self.hash_maps  = dict()

    def interpret(self, text):
        tokens = list(self.lexer.tokenize(text))
        parsed, rest = self.parser.parse(tokens)
        if rest:
            print('Failed to parse')
            return
        # self.parser.print(parsed)
        # print()
        self._interpret(parsed)
        print(self.variables, self.hash_maps)

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
                    print(self.variables, self.hash_maps)
            elif p[0] == 'arith_stmt':
                arith_stmt = p[1]
                lhs = arith_stmt[0]
                rhs = arith_stmt[1]
                rpn_tokens = shunting_yard(rhs)
                result = rpn_eval(rpn_tokens, self.variables, self.hash_maps)
                if lhs[0] == 'IDENT':
                    self.variables[lhs[1]] = result
                elif lhs[0] == 'HASH_MAP':
                    ident, index = lhs[1]
                    if not self.hash_maps.get(ident):
                        self.hash_maps[ident] = dict()
                    self.hash_maps[ident][index] = result

    def _check_condition(self, condition):
        lhs_t = condition[0]
        op_t = condition[1]
        op = op_t[0]
        rhs_t = condition[2]
        if lhs_t[0] == 'NUM':
            lhs = int(lhs_t[1])
        elif lhs_t[0] == 'IDENT':
            lhs = self.variables[lhs_t[1]]
        elif lhs_t[0] == 'HASH_MAP':
            ident, index = lhs_t[1]
            lhs = self.hash_maps[ident][index]
        if rhs_t[0] == 'NUM':
            rhs = int(rhs_t[1])
        elif rhs_t[0] == 'IDENT':
            rhs = self.variables[rhs_t[1]]
        elif rhs_t[0] == 'HASH_MAP':
            ident, index = rhs_t[1]
            rhs = self.hash_maps[ident][index]
        result = {
            'GT': lhs > rhs,
            'GE': lhs >= rhs,
            'EQ': lhs == rhs,
            'NEQ': lhs != rhs,
            'LE': lhs <= rhs,
            'LT': lhs < rhs,
        }
        return result[op]
def main():
    interpreter = Interpreter()
    text = '''
    i[0] = 0;
    while  i[0] < 10 {
        i[0] = i[0] + 1;
    }
    '''
    interpreter.interpret(text)

if __name__ == '__main__':
    main()
