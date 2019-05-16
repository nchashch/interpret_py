from lexer import Lexer
from shuntingyard import shunting_yard
from terminals import terminals

def rpn_eval(rpn_tokens, variables, hash_maps):
    vals = ('NUM', 'IDENT')
    ops = ('ADD', 'SUB', 'MUL', 'DIV', 'MOD')
    stack = []
    for terminal, acc in rpn_tokens:
        t = terminal
        if t == 'NUM':
            val = int(acc)
        elif t == 'IDENT':
            val = variables[acc]
        elif t == 'HASH_MAP':
            ident = acc[0]
            index = acc[1]
            val = hash_maps[ident][index]
        else:
            r = stack.pop()
            l = stack.pop()
            result = {
                'ADD': l + r,
                'SUB': l - r,
                'MUL': l * r,
                'DIV': l // r,
                'MOD': l % r,
            }
            val = result[t]
        stack.append(val)
    return stack.pop()

if __name__ == '__main__':
    lex = Lexer(terminals)
    text = '''
    a * 13 + b * 100 / 10
    '''
    tokens = lex.tokenize(text)
    rpn_tokens = shunting_yard(tokens)
    accs = [acc for _, acc in rpn_tokens]
    result = rpn_eval(rpn_tokens, {'a': 10, 'b': 20})
    print('Input:', text)
    print('RPN:', ' '.join(accs))
    print()
    print('Result:', result)
    print()
    print('RPN tokens:')
    for t in rpn_tokens:
        print(t)
