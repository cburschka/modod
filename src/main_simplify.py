from modod.dre import DRE
import argparse

def main():
    parser = argparse.ArgumentParser(description="This tool will simplify an deterministic regular expression.")
    parser.add_argument("expressions",help="The expressions to simplify",nargs="*")
    parser.add_argument("-v","--verbose",help="Print the parsed expressions",action="store_true")
    parser.add_argument("--graph",metavar="DOT_FILE", help="Dump the graphs in DOT format into DOT_FILE.n.(in|out).dot")
    args=parser.parse_args()
    def lineReader():
        try:
            while True:
                yield input()
        except EOFError:
            pass
    expressions = map(DRE.fromString, args.expressions or lineReader())
    f = ['{b}', '{a} -> {b}'][args.verbose]
    for i,a in enumerate(expressions):
        b = a.splitTerminals().simplify().joinTerminals()
        print (f.format(a=a.toString(), b=b.toString()))
        if args.graph:
            x = open('{0}.{1}.in.dot'.format(args.graph, i+1), 'w+')
            y = open('{0}.{1}.out.dot'.format(args.graph, i+1), 'w+')
            x.write(a.toDOTString())
            y.write(b.toDOTString())
            x.close()
            y.close()

