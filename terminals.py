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

    ('L_SB', '^\[$'),
    ('R_SB', '^\]$'),
    ('COMMA', '^\,$'),

    ('SEMICOLON', '^;$'),

    ('PRINT_KW', '^print$'),
    ('WHILE_KW', '^while$'),
    ('IF_KW', '^if$'),
    ('LIST_KW', '^list$'),
    ('PUSH_KW', '^push$'),
    ('GET_KW', '^get$'),
    ('DELETE_KW', '^delete$'),

    ('NUM', '^0$|^([1-9][0-9]{0,})$'),
    ('IDENT', '^[a-zA-Z]+[a-zA-Z0-9]*$'),
])
