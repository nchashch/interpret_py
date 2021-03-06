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
        arith_ast, arith_rest = self._arith_stmt(tokens)
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
                list_ast, list_rest = self._list_stmt(tokens)
                if list_ast:
                    ast = list_ast
                    rest = list_rest
                    label = 'list_stmt'
                else:
                    push_ast, push_rest = self._push_stmt(tokens)
                    if push_ast:
                        ast = push_ast
                        rest = push_rest
                        label = 'push_stmt'
                    else:
                        delete_ast, delete_rest = self._delete_stmt(tokens)
                        if delete_ast:
                            ast = delete_ast
                            rest = delete_rest
                            label = 'delete_stmt'
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

    # arith_expr -> NUM | IDENT | hash_map | get_expr | arith_expr arith_op arith_expr
    def _arith_expr(self, tokens):
        ast = []
        rest = tokens
        NUM_ast, NUM_rest = self._terminal('NUM', tokens)
        if NUM_ast:
            ast += NUM_ast
            rest = NUM_rest
        else:
            get_expr_ast, get_expr_rest = self._get_expr(tokens)
            if get_expr_ast:
                ast += get_expr_ast
                rest = get_expr_rest
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
    # list_stmt -> IDENT ASSIGN LIST L_P R_P SEMICOLON
    def _list_stmt(self, tokens):
        ast = []
        rest = tokens
        IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
        if IDENT_ast:
            rest = IDENT_rest
            ASSIGN_ast, ASSIGN_rest = self._terminal('ASSIGN', rest)
            if ASSIGN_ast:
                rest = ASSIGN_rest
                LIST_KW_ast, LIST_KW_rest = self._terminal('LIST_KW', rest)
                if LIST_KW_ast:
                    rest = LIST_KW_rest
                    L_P_ast, L_P_rest = self._terminal('L_P', rest)
                    if L_P_ast:
                        rest = L_P_rest
                        R_P_ast, R_P_rest = self._terminal('R_P', rest)
                        if R_P_ast:
                            rest = R_P_rest
                            SEMICOLON_ast, SEMICOLON_rest = self._terminal('SEMICOLON', rest)
                            if SEMICOLON_ast:
                                rest = SEMICOLON_rest
                                return ('NEW_LIST', IDENT_ast[0][1]), rest
        return [], rest
    # push_stmt -> PUSH_KW  L_P IDENT COMMA arith_expr R_P SEMICOLON
    def _push_stmt(self, tokens):
        ast = []
        rest = tokens
        PUSH_KW_ast, PUSH_KW_rest = self._terminal('PUSH_KW', rest)
        if PUSH_KW_ast:
            rest = PUSH_KW_rest
            L_P_ast, L_P_rest = self._terminal('L_P', rest)
            if L_P_ast:
                rest = L_P_rest
                IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
                if IDENT_ast:
                    rest = IDENT_rest
                    COMMA_ast, COMMA_rest = self._terminal('COMMA', rest)
                    if COMMA_ast:
                        rest = COMMA_rest
                        arith_expr_ast, arith_expr_rest = self._arith_expr(rest)
                        if arith_expr_ast:
                            rest = arith_expr_rest
                            R_P_ast, R_P_rest = self._terminal('R_P', rest)
                            if R_P_ast:
                                rest = R_P_rest
                                SEMICOLON_ast, SEMICOLON_rest = self._terminal('SEMICOLON', rest)
                                if SEMICOLON_ast:
                                    rest = SEMICOLON_rest
                                    return ('PUSH', IDENT_ast[0][1], arith_expr_ast), rest
        return [], rest
    # get_expr -> GET_KW L_P IDENT COMMA arith_expr R_P
    def _get_expr(self, tokens):
        ast = []
        rest = tokens
        GET_KW_ast, GET_KW_rest = self._terminal('GET_KW', rest)
        if GET_KW_ast:
            rest = GET_KW_rest
            L_P_ast, L_P_rest = self._terminal('L_P', rest)
            if L_P_ast:
                rest = L_P_rest
                IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
                if IDENT_ast:
                    rest = IDENT_rest
                    COMMA_ast, COMMA_rest = self._terminal('COMMA', rest)
                    if COMMA_ast:
                        rest = COMMA_rest
                        arith_expr_ast, arith_expr_rest = self._arith_expr(rest)
                        if arith_expr_ast:
                            rest = arith_expr_rest
                            R_P_ast, R_P_rest = self._terminal('R_P', rest)
                            if R_P_ast:
                                rest = R_P_rest
                                return [('GET', (IDENT_ast[0][1], arith_expr_ast))], rest
        return [], rest
    # delete_stmt -> DELETE_KW L_P IDENT COMMA arith_expr R_P SEMICOLON
    def _delete_stmt(self, tokens):
        ast = []
        rest = tokens
        DELETE_KW_ast, DELETE_KW_rest = self._terminal('DELETE_KW', rest)
        if DELETE_KW_ast:
            rest = DELETE_KW_rest
            L_P_ast, L_P_rest = self._terminal('L_P', rest)
            if L_P_ast:
                rest = L_P_rest
                IDENT_ast, IDENT_rest = self._terminal('IDENT', rest)
                if IDENT_ast:
                    rest = IDENT_rest
                    COMMA_ast, COMMA_rest = self._terminal('COMMA', rest)
                    if COMMA_ast:
                        rest = COMMA_rest
                        arith_expr_ast, arith_expr_rest = self._arith_expr(rest)
                        if arith_expr_ast:
                            rest = arith_expr_rest
                            R_P_ast, R_P_rest = self._terminal('R_P', rest)
                            if R_P_ast:
                                rest = R_P_rest
                                SEMICOLON_ast, SEMICOLON_rest = self._terminal('SEMICOLON', rest)
                                if SEMICOLON_ast:
                                    rest = SEMICOLON_rest
                                    return ('DELETE', IDENT_ast[0][1], arith_expr_ast), rest
        return [], rest

if __name__ == '__main__':
    lex = Lexer(terminals)
    text = '''
    c = list();
    push(c, 10+10);
    delete(c, 10);
    b = get(c, 0) + 100 - get(c, 100);
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
