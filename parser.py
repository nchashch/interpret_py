#!/bin/python
from lexer import Lexer
from terminals import terminals

'''
Regular grammar
Finite Automata
'''
class Parser:
    # lang -> stmt *
    def _lang(self, tokens):
        ast = []
        # Copy?
        rest = tokens
        while rest:
            stmt_ast, stmt_rest = self._stmt(rest)
            if stmt_ast:
                ast += stmt_ast
                rest = stmt_rest
            else:
                return [], tokens
        return ast, rest
    # stmt -> bool_stmt | arith_stmt | func_stmt | while
    def _stmt(self, tokens):
        ast = []
        # Copy?
        rest = tokens
        # bool_ast, bool_rest = self._bool_stmt(tokens)
        arith_ast, arith_rest = self._arith_stmt(tokens)
        # if bool_ast:
        #     ast.append(bool_ast)
        #     rest = bool_rest
        if arith_ast:
            ast += arith_ast
            rest = arith_rest
        else:
            while_ast, while_rest = self._while(tokens)
            if while_ast:
                ast += while_ast
                rest = while_rest
            else:
                return [], tokens
        return [('stmt', ast)], rest

    # arith_stmt -> IDENT ASSIGN arith_expr SEMICOLON
    def _arith_stmt(self, tokens):
        ast = []
        # Copy?
        rest = tokens
        IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
        if IDENT_ast:
            ast += IDENT_ast
            rest = IDENT_rest
        else:
            return [], rest
        ASSIGN_ast, ASSIGN_rest = self._terminal('ASSIGN', rest)
        if ASSIGN_ast:
            ast += ASSIGN_ast
            rest = ASSIGN_rest
        else:
            return [], rest
        arith_ast, arith_rest = self._arith_expr(rest)
        if arith_ast:
            ast += arith_ast
            rest = arith_rest
        else:
            return [], rest
        SEMICOLON_ast, SEMICOLON_rest = self._terminal('SEMICOLON', rest)
        if SEMICOLON_ast:
            ast += SEMICOLON_ast
            rest = SEMICOLON_rest
        else:
            return [], rest
        return ast, rest

    # arith_expr -> NUM | IDENT | arith_expr arith_op arith_expr
    def _arith_expr(self, tokens):
        ast = []
        rest = tokens
        NUM_ast, NUM_rest = self._terminal('NUM', tokens)
        if NUM_ast:
            ast += NUM_ast
            rest = NUM_rest
        else:
            IDENT_ast, IDENT_rest = self._terminal('IDENT', tokens)
            if IDENT_ast:
                ast += IDENT_ast
                rest = IDENT_rest
            else:
                return [], rest
        op_ast, op_rest = self._arith_op(rest)
        if op_ast:
            ast += op_ast
            rest = op_rest
            rhs_ast, rhs_rest = self._arith_expr(rest)
            if rhs_ast:
                ast += rhs_ast
                rest = rhs_rest
            else:
                return [], tokens
        return [('arith_expr', ast)], rest

    # arith_op -> ADD | SUB | MUL | DIV | MOD
    def _arith_op(self, tokens):
        ast = []
        rest = tokens
        terminals = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']
        for t in terminals:
            term_ast, term_rest = self._terminal(t, rest)
            if term_ast:
                return term_ast, term_rest
        return None, rest

    def _terminal(self, terminal, tokens):
        if not tokens:
            return None, tokens
        if tokens[0][0] == terminal:
            return [tokens[0]], tokens[1:]
        else:
            return None, tokens
    # while -> WHILE bool_expr L_CB while_body R_CB
    def _while(self, tokens):
        ast = []
        rest = tokens
        while_ast, while_rest = self._terminal('WHILE', rest)
        if while_ast:
            ast += while_ast
            rest = while_rest
            bool_ast, bool_rest = self._bool_expr(self, rest)
            if bool_ast:
                ast += bool_ast
                rest = bool_rest
                lcb_ast, lcb_rest = self._terminal('L_CB', rest)
                if lcb_ast:
                    ast += lcb_ast
                    rest = lcb_rest
                    body_ast, body_rest = self._while_body(rest)
                    if body_ast:
                        ast += body_ast
                        rest = body_rest
                        rcb_ast, rcb_rest = self._terminal('R_CB', rest)
                        if rcb_ast:
                            ast += rcb_ast
                            rest = rcb_rest
                            return ast, rest
            return [], tokens
    def _bool_expr(self, tokens):
        return [], tokens
    def _compar_expr(self, tokens):
        pass
    def _bool_bin_op(self, tokens):
        pass
    def _bool_un_op(self, tokens):
        pass
    def _while_body(self, tokens):
        return self._lang(tokens)

if __name__ == '__main__':
    lex = Lexer(terminals)
    text = '''
    cat = 10 + 15 - 15;
    dog = 2 % 1 + 16;
    foo = cat / dog;
    bar = foo % 10 + dog;
    '''
    print(text + '\n')
    tokens = lex.tokenize(text)
    parser = Parser()
    tokens = list(tokens)
    # for token in tokens:
    #     print(token)
    ast, rest = parser._lang(tokens)
    print()
    for node in ast:
        print(node)
        print()
    print(len(ast))
    print(rest)
