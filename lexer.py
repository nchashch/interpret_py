#!/bin/python
import re

class Lexer:
    def __init__(self, terminals):
        assert type(terminals) == dict
        self._terminals = terminals

    def next_token(self, text):
        acc = []
        terms_c0 = list()
        terms_c1 = list()
        c1 = ''
        for i, c0 in enumerate(text[:-1]):
            acc.append(c0)
            acc_str = ''.join(acc)
            c1 = text[i+1]
            terms_c0.clear()
            terms_c1.clear()
            for t in self._terminals:
                terminal = self._terminals[t]
                match0 = re.match(terminal, acc_str)
                match1 = re.match(terminal, acc_str + c1)
                if match0:
                    terms_c0.append(t)
                if match1:
                    terms_c1.append(t)
            if len(terms_c0) != 0 and len(terms_c1) == 0:
                return terms_c0.pop(), acc_str
        if len(terms_c1) != 0:
                return terms_c1.pop(), acc_str + c1
        elif len(terms_c0) != 0:
                return terms_c0.pop(), acc_str
        return '', ''

    def tokenize(self, text):
        while text:
            t, acc = self.next_token(text)
            token = (t, acc)
            text = text[len(acc):]
            if len(acc) == 0:
                text = text[1:]
                continue
            yield token

if __name__ == '__main__':
    terminals = {
        'ADD': '^\+$',
        'SUB': '^\-$',
        'MUL': '^\*$',
        'DIV': '^\/$',
        'MOD': '^\%$',

        'LT': '^<$',
        'GT': '^>$',
        'LE': '^<=$',
        'GE': '^>=$',
        'EQ': '^==$',
        'NEQ': '^!=$',
        'ASSIGN': '^=$',

        'AND': '^&&$',
        'OR': '^\|\|$',
        'NOT': '^!$',

        'IDENT': '^[a-zA-Z]+[a-zA-Z0-9]*$',
        'NUM': '^0|([1-9][0-9]{0,})$',
        'PRINT_KW': '^print$',
        'WHILE_KW': '^while$',
        'IF_KW': '^if$',
    }
    # var reg = /^(o|$)(n|$)(e|$)(\s|$)$/;

    lex = Lexer(terminals)
    text = '''
    if 1 == 1 || 1 >= 10 {
        A = 1 2 3 4 + +;
        print A;
    }

    while cat <= 1 && cat >= 0 {
        A = 1;
        cat = cat A +;
        print A;
        print cat;
    }
    '''
    print(text + '\n')
    for token in lex.tokenize(text):
        print(token)
