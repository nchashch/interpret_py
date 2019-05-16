#!/bin/python
from lexer import Lexer
from terminals import terminals

'''
Regular grammar
Finite Automata
'''
class Parser:
    def print(self, parsed, indent=0):
        pad = '  '
        for p in parsed:
            if p[0] == 'while_stmt':
                print(pad*indent, p[0])
                print(pad*indent, 'condition: {}'.format(p[1][0]))
                print(pad*indent, 'body: ')
                while_body = p[1][1]
                self.print(while_body, indent+1)
            elif p[0] == 'arith_stmt':
                print(pad*indent, p)
    def parse(self, tokens):
        return self._lang(tokens)
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
                return ast, rest
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
            ast = arith_ast
            rest = arith_rest
            label = 'arith_stmt'
        else:
            while_ast, while_rest = self._while(tokens)
            if while_ast:
                ast = while_ast
                rest = while_rest
                label  = 'while_stmt'
            else:
                return [], tokens
        return [(label, ast)], rest

    # arith_stmt -> IDENT ASSIGN arith_expr SEMICOLON
    def _arith_stmt(self, tokens):
        lhs = None
        rhs = None
        # Copy?
        rest = tokens
        hash_map_ast, hash_map_rest = self._hash_map(rest)
        if hash_map_ast:
            lhs = hash_map_ast[0]
            rest = hash_map_rest
        else:
            IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
            if IDENT_ast:
                lhs = IDENT_ast[0]
                rest = IDENT_rest
            else:
                return [], rest
        ASSIGN_ast, ASSIGN_rest = self._terminal('ASSIGN', rest)
        if ASSIGN_ast:
            # ast += ASSIGN_ast
            rest = ASSIGN_rest
        else:
            return [], rest
        arith_ast, arith_rest = self._arith_expr(rest)
        if arith_ast:
            rhs = arith_ast
            rest = arith_rest
        else:
            return [], rest
        SEMICOLON_ast, SEMICOLON_rest = self._terminal('SEMICOLON', rest)
        if SEMICOLON_ast:
            # ast += SEMICOLON_ast
            rest = SEMICOLON_rest
        else:
            return [], rest
        return (lhs, rhs), rest

    # arith_expr -> NUM | IDENT | hash_map | arith_expr arith_op arith_expr
    def _arith_expr(self, tokens):
        ast = []
        rest = tokens
        NUM_ast, NUM_rest = self._terminal('NUM', tokens)
        if NUM_ast:
            ast += NUM_ast
            rest = NUM_rest
        else:
            hash_map_ast, hash_map_rest = self._hash_map(tokens)
            if hash_map_ast:
                ast += hash_map_ast
                rest = hash_map_rest
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
        return ast, rest

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
        rest = tokens
        while_ast, while_rest = self._terminal('WHILE_KW', rest)
        if while_ast:
            rest = while_rest
            compar_ast, compar_rest = self._compar_expr(rest)
            if compar_ast:
                condition = compar_ast
                rest = compar_rest
                lcb_ast, lcb_rest = self._terminal('L_CB', rest)
                if lcb_ast:
                    rest = lcb_rest
                    body_ast, body_rest = self._while_body(rest)
                    if body_ast:
                        rest = body_rest
                        rcb_ast, rcb_rest = self._terminal('R_CB', rest)
                        if rcb_ast:
                            # ast += rcb_ast
                            rest = rcb_rest
                            return (condition, body_ast), rest
        return [], tokens
    def _while_body(self, tokens):
        return self._lang(tokens)
    # compar_expr -> arith_expr compar_op arith_expr
    def _compar_expr(self, tokens):
        ast = []
        rest = tokens
        l_operand_ast, l_operand_rest = self._arith_expr(rest)
        rest = l_operand_rest
        if l_operand_ast:
            ast += l_operand_ast
            op_ast, op_rest = self._compar_op(rest)
            if op_ast:
                ast += op_ast
                rest = op_rest
                r_operand_ast, r_operand_rest = self._arith_expr(rest)
                if r_operand_ast:
                    ast += r_operand_ast
                    rest = r_operand_rest
                    return ast, rest
        return [], tokens
    # compar_op -> GT | GE | EQ | LE | LT
    def _compar_op(self, tokens):
        ast = []
        rest = tokens
        terminals = ['GT', 'GE', 'EQ', 'LE', 'LT']
        for t in terminals:
            term_ast, term_rest = self._terminal(t, rest)
            if term_ast:
                return term_ast, term_rest
        return None, rest
    # def _bool_expr(self, tokens):
    #     return self._compar_expr(tokens)
    def _bool_bin_op(self, tokens):
        pass
    def _bool_un_op(self, tokens):
        pass
    def _list(self, tokens):
        pass
    def _list_content(self, tokesn):
        pass
    # hash_map -> IDENT L_SB arith_expr R_SB
    def _hash_map(self, tokens):
        ast = []
        rest = tokens
        IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
        if IDENT_ast:
            ast += IDENT_ast
            rest = IDENT_rest
            L_SB_ast, L_SB_rest = self._terminal('L_SB', rest)
            if L_SB_ast:
                ast += L_SB_ast
                rest = L_SB_rest
                index_ast, index_rest = self._arith_expr(rest)
                if index_ast:
                    ast += index_ast
                    rest = index_rest
                    R_SB_ast, R_SB_rest = self._terminal('R_SB', rest)
                    if R_SB_ast:
                        ast += R_SB_ast
                        rest = R_SB_rest

                        ident = IDENT_ast[0][1]
                        index = index_ast

                        return [('HASH_MAP', (ident, index))], rest
        return [], rest

if __name__ == '__main__':
    lex = Lexer(terminals)
    text = '''
    a[10] = 1 + 123;
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
