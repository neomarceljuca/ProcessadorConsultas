import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import DML, Keyword, Punctuation


def parse_sql(sql):
    parsed = sqlparse.parse(sql)[0]

    nodes = []
    edges = []
    stack = []

    for token in parsed.tokens:
        if token.ttype is Keyword:
            stack.append(str(token))
        elif token.ttype is Punctuation and token.value == '(':
            if stack:
                nodes.append(' '.join(stack))
                stack.clear()
        elif token.ttype is Punctuation and token.value == ')':
            if stack:
                nodes.append(' '.join(stack))
                if len(nodes) > 1:
                    edges.append((nodes[-2], nodes[-1]))
                stack.clear()

    return nodes, edges

sql = "SELECT A.name, B.address FROM (Customers AS A JOIN (Orders AS B ON A.id = B.customer_id)) WHERE (A.age > 30 AND B.total_amount > 100)"
nodes, edges = parse_sql(sql)

print("Nodes:")
for node in nodes:
    print(node)

print("\nEdges:")
for edge in edges:
    print(' - '.join(edge))