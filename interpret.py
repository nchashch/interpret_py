#!/bin/python
from lexer import Lexer
from parser import Parser
from terminals import terminals
from shuntingyard import shunting_yard
from rpn_eval import rpn_eval
from hash_map import HashMap
from linked_list import LinkedList

class Interpreter:
    def __init__(self):
        self.lexer = Lexer(terminals)
        self.parser = Parser()
        self._CAPACITY = 100
        self.variables = dict()
        self.hash_maps  = dict()
        self.lists = dict()

    def interpret(self, text):
        tokens = list(self.lexer.tokenize(text))
        parsed, rest = self.parser.parse(tokens)
        if rest:
            print('Failed to parse')
            return
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
                    print(self.variables, self.hash_maps, self.lists)
            elif p[0] == 'list_stmt':
                list_stmt = p[1]
                if list_stmt[0] == 'NEW_LIST':
                    self.lists[list_stmt[1]] = LinkedList()
            elif p[0] == 'push_stmt':
                push_stmt = p[1]
                if push_stmt[0] == 'PUSH':
                    name = push_stmt[1]
                    arith_expr = push_stmt[2]
                    tokens = shunting_yard(arith_expr)
                    result = rpn_eval(tokens, self.variables, self.hash_maps, self.lists)
                    self.lists[name].push(result)
            elif p[0] == 'delete_stmt':
                delete_stmt = p[1]
                if delete_stmt[0] == 'DELETE':
                    name = delete_stmt[1]
                    arith_expr = delete_stmt[2]
                    tokens = shunting_yard(arith_expr)
                    index = rpn_eval(index_tokens, self.variables, self.hash_maps, self.lists)
                    self.lists[name].delete(index)
            elif p[0] == 'arith_stmt':
                arith_stmt = p[1]
                lhs = arith_stmt[0]
                rhs = arith_stmt[1]
                rpn_tokens = shunting_yard(rhs)
                result = rpn_eval(rpn_tokens, self.variables, self.hash_maps, self.lists)
                if lhs[0] == 'IDENT':
                    self.variables[lhs[1]] = result
                elif lhs[0] == 'HASH_MAP':
                    ident, index_tokens = lhs[1]
                    index_tokens = shunting_yard(index_tokens)
                    index = rpn_eval(index_tokens, self.variables, self.hash_maps, self.lists)
                    if not self.hash_maps.get(ident):
                        self.hash_maps[ident] = HashMap(self._CAPACITY)
                    self.hash_maps[ident][index] = result

    def _get_token_value(self, token):
        if token[0] == 'NUM':
            return int(token[1])
        elif token[0] == 'IDENT':
            return self.variables[token[1]]
        elif token[0] == 'GET':
            ident, index_tokens = token[1]
            index_tokens = shunting_yard(index_tokens)
            index = rpn_eval(index_tokens, self.variables, self.hash_maps, self.lists)
            return self.lists[ident].get(index)
        elif token[0] == 'HASH_MAP':
            ident, index_tokens = token[1]
            index_tokens = shunting_yard(index_tokens)
            index = rpn_eval(index_tokens, self.variables, self.hash_maps, self.lists)
            return self.hash_maps[ident][index]

    def _check_condition(self, condition):
        lhs_t = condition[0]
        op_t = condition[1]
        op = op_t[0]
        rhs_t = condition[2]
        lhs = self._get_token_value(lhs_t)
        rhs = self._get_token_value(rhs_t)
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
    i = 0;
    c[0] = 0;
    b = list();
    push(b, 15);
    push(b, 14);
    c[1] = get(b, 0) + get(b, 1);
    while  i < get(b, 0) {
        i = i + 1;
        c[0] = i;
    }
    '''
    interpreter.interpret(text)

if __name__ == '__main__':
    main()
