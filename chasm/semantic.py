
rules = {
    'SYS': [('T_COMMAND', 'T_ADDR')],
    'CLS': [('T_COMMAND',)],
    'RET': [('T_COMMAND',)],
    'JMP': [('T_COMMAND', 'T_ADDR'),
            ('T_COMMAND', 'T_ADDR', 'T_COMMA', 'T_REGISTER')],
    'CALL': [('T_COMMAND', 'T_ADDR')],
    'SE': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE')],
    'SNE': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'ADD': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'OR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'AND':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'XOR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SUB':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SHR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SUBC':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SHL':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'LDI': [('T_COMMAND', 'T_ADDR')],
    'RND': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE')],
    'DRW': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER',
             'T_COMMA', 'T_NIBBLE')],
    'SKP': [('T_COMMAND', 'T_REGISTER')],
    'SKNP': [('T_COMMAND', 'T_REGISTER')],
    'STR': [('T_COMMAND', 'T_REGISTER')],
    'FILL': [('T_COMMAND', 'T_REGISTER')],
    'LD': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_DELAY'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_KEYBOARD'),
           ('T_COMMAND', 'T_DELAY', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_SOUND', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_FONT', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_BINARY', 'T_COMMA', 'T_REGISTER')]
}


class InvalidInstructionError(Exception):
    pass

class InvalidMemoryAddressError(Exception):
    pass


def analyze(ast):
    for node in ast.nodes:
        is_valid_instruction(node)
        is_valid_memory_address(node)
    return True


def is_valid_instruction(node):
    instruction = tuple([t['type'] for t in node])
    rule = rules[node[0]['value']]
    if not instruction in rule:
        instruction = ' '.join(map(lambda t: t['value'], node))
        raise InvalidInstructionError("Invalid instruction: %s" % (instruction, ))
    return True


def is_valid_memory_address(node):
    addr = filter(lambda t: t['type'] == 'T_ADDR', node)
    if addr and addr[0]['value'] < '0x200':
        raise InvalidMemoryAddressError("Invalid memory address: %s" % (addr[0]['value'],))
    return True