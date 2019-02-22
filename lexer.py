import re

class Lexer:
    def __init__(self, terminals):
        assert type(terminals) == dict
        self._terminals = terminals
        self._acc = []

    def next_token(self, text):
        self._acc = []
        for i, c in enumerate(text):
            self._acc.append(c)
            for t in self._terminals:
                terminal = self._terminals[t]
                acc = ''.join(self._acc)
                if re.match(terminal, acc):
                    return (t, acc)
        return '', ''

    def tokenize(self, text):
        tokens = []
        while text:
            t, acc = self.next_token(text)
            token = (t, acc)
            text = text[len(acc):]
            if len(acc) == 0:
                text = text[1:]
                continue
            tokens.append(token)
        return tokens

if __name__ == '__main__':
    terminals = {
        'abcd': 'abcd',
        'ABCD': 'ABCD',
        'DIGIT': '[0-9]',
    }
    lex = Lexer(terminals)
    text = '1234 abcd abcd, ABCD, abcd, 1 23 2442'
    print(lex.next_token(text))
    print(lex.tokenize(text))
