import lexer
import parser

def main():
    s = input().strip()
    #print(s)
    tokens = lexer.lex(s)
    #print(tokens)
    parsed = parser.parse(tokens)
    #print(parsed)
    tree = parsed.dre()
    print(tree)
    
    
main()
