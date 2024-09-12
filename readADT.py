from parsy import forward_declaration, regex, seq, string
import parsy
import json
import sys
sys.setrecursionlimit(100000)

# Utilities
maybe_whitespace = regex(r'\s*')
lexeme = lambda p: p << maybe_whitespace

# Punctuation
lparen = lexeme(string("("))
rparen = lexeme(string(")"))
lbrace = lexeme(string("{"))
rbrace = lexeme(string("}"))
lbrack = lexeme(string("["))
rbrack = lexeme(string("]"))
eq = lexeme(string("="))
comma = lexeme(string(","))

# Primitives
true = lexeme(string("true")).result(True)
false = lexeme(string("false")).result(False)
null = lexeme(string("null")).result(None)
number = lexeme(regex(r"-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?")).map(json.loads)
def quoted_by(quote):
    string_part = regex(fr'[^{quote}\\]+')
    string_esc = string("\\") >> (
        string("\\")
        | string("/")
        | string(quote)
        | string("b").result("\b")
        | string("f").result("\f")
        | string("n").result("\n")
        | string("r").result("\r")
        | string("t").result("\t")
        | regex(r"u[0-9a-fA-F]{4}").map(lambda s: chr(int(s[1:], 16)))
    )
    return (lexeme(string(quote) >> (string_part | string_esc).many().concat() << string(quote))).map(
        lambda x:[quote,x])

quoted_1 = quoted_by("'")
quoted_2 = quoted_by('"')

# Data structures
single_value = forward_declaration()
#multivalue can't be empty
multivalue = single_value.at_least(1).map(lambda xs:xs[0] if len(xs)==1 else xs)
#     increased recursion depth?
#     but not slower
#multivalue = single_value.many().map(lambda xs:xs[0] if len(xs)==1 else xs)
identifier = regex("[a-zA-Z][a-zA-Z0-9_]*") << maybe_whitespace
object_pair = seq(identifier << eq, multivalue).map(tuple)
pseudojson_object = lbrace >> object_pair.sep_by(comma).map(dict) << rbrace
array = (lbrack >> multivalue.sep_by(comma) << rbrack).map(lambda xs:['[]']+xs)

# Everything
single_value.become(identifier | quoted_1 | quoted_2 | number | pseudojson_object | array |
    lparen >> multivalue << rparen
)

doc = maybe_whitespace>>multivalue

if __name__ == "__main__":
    #from sys import stdin
    import sys
    import json
    json.dump(doc.parse(sys.stdin.read()),sys.stdout)

