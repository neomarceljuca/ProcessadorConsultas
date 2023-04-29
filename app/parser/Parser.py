import re


def parser(self, sql_query):

    # Define a expressão regular para extrair a coluna e a tabela
    pattern = r"SELECT\s+(\w+)\s+FROM\s+(\w+);"
    match = re.match(pattern, sql_query)

    # Extrai a coluna e a tabela
    coluna = match.group(1)
    tabela = match.group(2)

    # Gera a expressão de álgebra relacional correspondente
    expr = "pi {}({})".format(coluna, tabela)
    print(expr)
