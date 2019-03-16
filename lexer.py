#!/bin/python
import re

class Lexer:
    def __init__(self, terminals):
        assert type(terminals) == dict
        self._terminals = terminals

    def next_token(self, text):
        acc = []
        for i, c0 in enumerate(text[:-1]):
            acc.append(c0)
            acc_str = ''.join(acc)
            terms_c0 = set()
            terms_c1 = set()
            c1 = text[i+1]
            for t in self._terminals:
                terminal = self._terminals[t]
                match0 = re.match(terminal, acc_str)
                match1 = re.match(terminal, acc_str + c1)
                if match0:
                    terms_c0.add(t)
                if match1:
                    terms_c1.add(t)
            if len(terms_c0) == 1 and len(terms_c1) == 0:
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

        # 'GR': '^\>$',
        # 'GE': '^\>\=$',
        # 'EQ': '^=(=|$)$',
        # 'LS': '^\<$',
        # 'LE': '^\<\=$',

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

        'NUM': '^0|([1-9][0-9]{0,})$',
        'PRINT_KW': '^print$',
        'WHILE_KW': '^while$',
        'IF_KW': '^if$',
        'IDENT': '^[A-Z]+[A-Z0-9]*$',
    }
    # var reg = /^(o|$)(n|$)(e|$)(\s|$)$/;

    lex = Lexer(terminals)
    text = '''
    if 1 == 1 || 1 >= 10 {
        A = 1 2 3 4 + +;
        print A;
    }

    while CAT <= 1 && CAT >= 0 {
        A = 1;
        CAT = CAT A +;
        print A;
        print CAT;
    }
    '''
    print(text + '\n')
    for token in lex.tokenize(text):
        print(token)
