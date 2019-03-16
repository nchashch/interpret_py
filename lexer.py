#!/bin/python
from collections import OrderedDict
import re

class Lexer:
    def __init__(self, terminals):
        assert type(terminals) == OrderedDict
        self._terminals = terminals

    def next_token(self, text):
        acc = []
        terms_c0 = list()
        terms_c1 = list()
        c1 = ''
        for i, c0 in enumerate(text[:-1]):
            if c0 != '\n':
                acc.append(c0)
            acc_str = ''.join(acc)
            c1 = text[i+1]
            terms_c0.clear()
            terms_c1.clear()
            # reversed in order to make terminals
            # further up have higher priority
            for t in reversed(self._terminals):
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
    terminals = OrderedDict([
        ('ADD', '^\+$'),
        ('SUB', '^\-$'),
        ('MUL', '^\*$'),
        ('DIV', '^\/$'),
        ('MOD', '^\%$'),

        ('LT', '^<$'),
        ('GT', '^>$'),
        ('LE', '^<=$'),
        ('GE', '^>=$'),
        ('EQ', '^==$'),
        ('NEQ', '^!=$'),
        ('ASSIGN', '^=$'),

        ('AND', '^&&$'),
        ('OR', '^\|\|$'),
        ('NOT', '^!$'),

        ('L_CB', '^{$'),
        ('R_CB', '^}$'),

        ('PRINT_KW', '^print$'),
        ('WHILE_KW', '^while$'),
        ('IF_KW', '^if$'),
        ('NUM', '^0$|^([1-9][0-9]{0,})$'),
        ('IDENT', '^[a-zA-Z]+[a-zA-Z0-9]*$'),
    ])
    # var reg = /^(o|$)(n|$)(e|$)(\s|$)$/;

    lex = Lexer(terminals)

    # if 1 == 1 || 1 >= 10 {
    #     A = 1 + 2;
    #     print A;
    # }

    text = '''
    while cat <= 10 && cat >= 0 {
        A = 1;
        cat = cat + A;
        print A;
        print cat;
    }
    '''
    print(text + '\n')
    for token in lex.tokenize(text):
        print(token)
