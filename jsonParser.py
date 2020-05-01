import json
from lark import Lark, Transformer

jsonLang = Lark(r"""
    ?value:  dict
         |  array
         |  string
         |  number
         |  "true"      -> true
         |  "false"     -> false
         |  "null"      -> null

    dict:       "{" [pair ("," pair)*] "}"
    pair:       string ":" value

    array:      "[" [value ("," value)*] "]"

    number:     SIGNED_NUMBER
    string:     ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
""", start='value', parser='lalr')


class JsonTransformer(Transformer):
    def dict(self, items):
        return dict(items)

    def pair(self, key_value):
        k, v = key_value
        return k, v

    def array(self, items):
        return list(items)

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def number(self, n):
        (n,) = n
        return float(n)

    def null(self, n):
        return None

    def true(self, n):
        return True

    def false(self, n):
        return False


testStr = '{"key": ["item0", "item1", 3.14, null, true, false]}'

tree = jsonLang.parse(testStr)
print(tree.pretty())

transformed_tree = JsonTransformer().transform(tree)
print(transformed_tree)

assert json.loads(testStr) == transformed_tree
