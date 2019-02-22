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
        'abcd': '^abcd$',
        'ABCD': '^ABCD$',
        'NUM': '^0|([1-9][0-9]{0,})$',
        'DIGIT': '^[0-9]$',
    }
    lex = Lexer(terminals)
    text = '1234 abcd abcd, ABCD, abcd, 1 23 2442'
    print(text + '\n')
    for token in lex.tokenize(text):
        print(token)
