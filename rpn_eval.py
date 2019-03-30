from lexer import Lexer
from shuntingyard import shunting_yard
from terminals import terminals

def rpn_eval(rpn_tokens):
    vals = ('NUM', 'IDENT')
    ops = ('ADD', 'SUB', 'MUL', 'DIV', 'MOD')
    stack = []
    for terminal, acc in rpn_tokens:
        t = terminal
        if t == 'NUM':
            val = int(acc)
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
    (100 + 14) / 2 + 10
    '''
    tokens = lex.tokenize(text)
    rpn_tokens = shunting_yard(tokens)
    accs = [acc for _, acc in rpn_tokens]
    result = rpn_eval(rpn_tokens)
    print('Input:', text)
    print('RPN:', ' '.join(accs))
    print()
    print('Result:', result)
    print()
    print('RPN tokens:')
    for t in rpn_tokens:
        print(t)
