#!/bin/python
import re

class Lexer:
    def __init__(self, terminals):
        assert type(terminals) == dict
        self._terminals = terminals

    def next_token(self, text):
        acc = []
        for i, c0 in enumerate(text):
            acc.append(c0)
            for t in self._terminals:
                terminal = self._terminals[t]
                acc_str = ''.join(acc)
                if re.match(terminal, acc_str):
                    for c1 in text[i+1:]:
                        acc_str = ''.join(acc)
                        if re.match(terminal, acc_str + c1):
                            acc.append(c1)
                            acc_str = ''.join(acc)
                        else:
                            return t, acc_str
                    if re.match(terminal, acc_str):
                        return t, acc_str
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

        'NUM': '^0|([1-9][0-9]{0,})$',
        'PRINT_KW': '^print$',
        'WHILE_KW': '^while$',
        'IF_KW': '^if$',
        'IDENT': '^[A-Z]+[A-Z0-9]*$',
    }
    # var reg = /^(o|$)(n|$)(e|$)(\s|$)$/;

    lex = Lexer(terminals)
    text = '''
    if 1 == 1 {
        A = 1 2 3 4 + +;
        print A;
    }

    while CAT < 1 {
        A = 1;
        CAT = CAT A +;
        print A;
        print CAT;
    }
    '''
    print(text + '\n')
    for token in lex.tokenize(text):
        print(token)
