import re

asm_tokens = [
    { 'type': 'T_LABEL', 'pattern': r'[\d\w]+:' },
    { 'type': 'T_COMMAND', 'pattern': r'(SYS|CLS|RET|JMP|CALL|'
                                 'SE|SNE|LD|ADD|OR|AND|'
                                 'XOR|SUB|SHR|SUBC|SHL|SNE|'
                                 'LDI|RND|DRW|SKP|SKNP|STR|'
                                 'FIL)' },
    { 'type': 'T_MEMORY', 'pattern': r'0x[\dA-F]+' },
    { 'type': 'T_CONSTANT', 'pattern': r'#[\dA-F]+' },
    { 'type': 'T_REGISTER', 'pattern': r'V[\dA-F]{1}' },
    { 'type': 'T_DELAY', 'pattern': r'DT' },
    { 'type': 'T_SOUND', 'pattern': r'ST' },
    { 'type': 'T_BINARY', 'pattern': r'B' },
    { 'type': 'T_FONT', 'pattern': r'F' },
    { 'type': 'T_REGISTER_I', 'pattern': r'I' },
    { 'type': 'T_WHITESPACE', 'pattern': r'\s' },
    { 'type': 'T_COMMA', 'pattern': r',' },
    { 'type': 'T_EOL', 'pattern': r'\n' },
    { 'type': 'T_UNKNOW', 'pattern': r'[\d\w]+' }
]


class UnknowTokenError(Exception):
    pass


class Token(object):

    def __init__(self, type='T_EOL', value='\n'):
        self.type = type
        self.value = value


def tokenize(code):
    tokens = []
    line, column = (1, 1)
    while len(code) > 0:
        for token in asm_tokens:
            match = re.match(token['pattern'], code, re.S)
            if match:
                if token['type'] == 'T_UNKNOW':
                    raise UnknowTokenError("Token not found: %s" % (match.group(0), ))
                tokens.append(Token(type=token['type'], 
                                value=match.group(0)))
                code = code[len(match.group(0)):]
                break
    return tokens
