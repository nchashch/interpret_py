from collections import OrderedDict
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

    ('L_P', '^\($'),
    ('R_P', '^\)$'),

    ('SEMICOLON', '^;$'),

    ('PRINT_KW', '^print$'),
    ('WHILE_KW', '^while$'),
    ('IF_KW', '^if$'),
    ('NUM', '^0$|^([1-9][0-9]{0,})$'),
    ('IDENT', '^[a-zA-Z]+[a-zA-Z0-9]*$'),
])
