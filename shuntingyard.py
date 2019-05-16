from lexer import Lexer
from terminals import terminals

# TODO(Optional): Make this exception more informative
# TODO(Optional): Add exceptions for other failure modes
class MismatchedParens:
    pass

# TODO: Explain how this works in comments
def shunting_yard(tokens):
    output = []
    op_stack = []
    vals = ('NUM', 'IDENT', 'HASH_MAP')
    ops = ('ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'L_P', 'R_P')
    prec = {
        'ADD': 0,
        'SUB': 0,
        'MUL': 1,
        'DIV': 1,
        'MOD': 1,
        'L_P': 2,
        'R_P': 2,
    }
    for terminal, acc in tokens:
        t = terminal
        if t in vals:
            output.append((t, acc))
        elif t in ops:
            if not op_stack:
                op_stack.append((t, acc))
            else:
                op = op_stack[-1]
                while prec[op[0]] >= prec[t] and op[0] != 'L_P':
                    op = op_stack.pop()
                    output.append(op)
                    if not op_stack:
                        break
                    op = op_stack[-1]
                if t == 'R_P':
                    op = op_stack[-1]
                    while op[0] != 'L_P':
                        op = op_stack.pop()
                        output.append(op)
                        if not op_stack:
                            raise MismatchedParens
                        op = op_stack[-1]
                    if op[0] == 'L_P':
                        op_stack.pop()
                else:
                    op_stack.append((t, acc))
    while op_stack:
        op = op_stack.pop()
        if op == 'L_P' or op == 'R_P':
            raise MismatchedParens
        output.append(op)
    return output

if __name__ == '__main__':
    lex = Lexer(terminals)
    text = '''
    ((1 + 2) / (cat - dog)) * 10 / 7 + 1 + 2 + 3
    '''
    tokens = lex.tokenize(text)
    rpn_tokens = shunting_yard(tokens)
    accs = [acc for _, acc in rpn_tokens]
    print(' '.join(accs))
    print()
    for t in rpn_tokens:
        print(t)
