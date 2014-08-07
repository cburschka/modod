import modod, modod.dre
import modod.dre as ext
from modod.dre import DRE
import argparse

def main():
    parser = argparse.ArgumentParser(description="This tool will simplify an deterministic regular expression.")
    parser.add_argument("expressions",help="The expressions to simplify",nargs="*")
    parser.add_argument("-v","--verbose",help="Print the parsed expressions",action="store_true")
    parser.add_argument("--graph",metavar="DOT_FILE", help="Dump the graphs in DOT format into DOT_FILE.n.(in|out).dot")
    parser.add_argument("--long", help="Sequences of symbols are interpreted as single letters; i. e., abc is a single letter, as is a1", action="store_false")
    parser.add_argument("--charset", help="Attempt to print single-letter choices as character sets.", choices=['none', 'complete', 'all'], default='complete')
    parser.add_argument("--join", help="Remove duplicate choice expressions", action="store_true")
    parser.add_argument("--steps", help="Print individual steps.", action="store_true")
    args=parser.parse_args()
    if args.long:
        modod._lexerExt.letters = True
        modod.dre.Concatenation._label = ''
    modod.charGroup = {
        'none': modod.CHARGROUP_NONE,
        'complete': modod.CHARGROUP_COMPLETE,
        'all': modod.CHARGROUP_PARTIAL
    }[args.charset]
    def lineReader():
        try:
            line = input().strip()
            while line:
                yield line
                line = input().strip()
        except EOFError:
            pass
        except KeyboardInterrupt:
            pass
    expressions = map(DRE.fromString, args.expressions or lineReader())
    f = ['{b}', '{a} -> {b}'][args.verbose]
    for i,a in enumerate(expressions):
        b = a.simplify(args.steps)
        if args.steps:
            for j, (step, x) in enumerate(b):
                print('#{} {:10} {}'.format(j, step, x.toString()))
                if args.graph:
                    y = open('{0}.{1}.{2}.dot'.format(args.graph, i+1, j+1), 'w+')
                    y.write(x.toDOTString())
                    y.close()
            print()
            b = x
        else:
            if args.join:
                b = ext.reduceChoiceNary(b)
            print (f.format(a=a.toString(), b=b.toString()))
        if args.graph:
            x = open('{0}.{1}.in.dot'.format(args.graph, i+1), 'w+')
            y = open('{0}.{1}.out.dot'.format(args.graph, i+1), 'w+')
            x.write(a.toDOTString())
            y.write(b.toDOTString())
            x.close()
            y.close()

