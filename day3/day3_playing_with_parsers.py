from ply import lex
from ply import yacc
from functools import reduce
from operator import mul

tokens = (
    'COMMA',
    'NUMBER',
    'MUL',
    'LPAREN',
    'RPAREN'
)

t_COMMA = r','
t_MUL = r'mul'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    # print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def p_mul_list(p):
    '''
    mul_list : mul
             | mul_list mul
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_mul(p):
    '''
    mul : MUL LPAREN arg_list RPAREN
    '''
    p[0] = reduce(mul, p[3])
    print(p[0])

def p_arg_list(p):
    '''
    arg_list : NUMBER
             | arg_list COMMA NUMBER
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_mul_error(p):
    '''
    mul : MUL error
    '''
    print(f"Snytax erorr in mul")
    # parser.errok()

lexer = lex.lex()
parser = yacc.yacc()

def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()
    
file = 'day3/test-input.txt'
data = read_file(file)
# data = "mul(3,4)mul(4,4)"
print(data)

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

print(parser.parse(data))