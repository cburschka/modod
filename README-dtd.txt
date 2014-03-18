usage: dtd.py [-h] [-a [AUTPREFIX]] [-c] [-co] [-d]
              [-e ELEMENTS [ELEMENTS ...]] [-j] [-n] [-s] [-u] [-we] [-wep]
              [-wes]
              files [files ...]

This tool takes a list of XML files and computes a DTD.

positional arguments:
  files                 the XML file(s) from which the element type
                        declarations are to be inferred

optional arguments for regular users:
  -h, --help            show this help message and exit
  -c, --chare           infer a chain regular expression, instead of a single
                        occurrence regular expression (the former are flatter
                        than the latter)
  -d, --dre             write output as deterministic regular expression,
                        instead of an element type declaration (also activates
                        -j)
  -e ELEMENTS [ELEMENTS ...], --elements ELEMENTS [ELEMENTS ...]
                        determines for which element names an element type
                        declaration is inferred
  -j, --just-elements   do not put the DOCTYPE declaration around the element
                        tags
  -s, --skip-empty      do not display declarations of elements that have no
                        childer
  -u, --ugly            do not use prettification algorithm

Default is inferring an element type definition for every element in the
files. If you want to compute this for only some elements, use the -e flag. If
you want to exclude elements that have empty definitions, use the -s flag. 

optional arguments for users who want to run tests or care about the theory:
-a [AUTPREFIX], --automaton [AUTPREFIX]
                       for every element E, the inferred SOA is written to
                       the file AUTPREFIX E.dot in the dot-format of Graphviz
-co, --counts          display how often elements occur
-n, --no-inference     do not infer element type declarations (only useful if
                       -a is used as well)
-t, --time-stamps      includes some timestamps (for very elementary profiling) 
-v, --verbose          print additional information
-we, --write-elements  for every element E, write the inferred DTD/regular
                       expression to a file WPREFIX E.WSUFFIX (definable by
                       -wp,-ws)
-wep, --write-prefix  sets WPREFIXe (for -we), default empty
-wes, --write-suffix  sets WPREFIXe (for -we), default .dtd

