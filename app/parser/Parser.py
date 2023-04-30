import re


def parser(sql_query):

    # Expressão regular para procurar a palavra "exemplo"
    pattern_WHERE = r"\bWHERE\b"

    # Procura a palavra "exemplo" na string
    match_WHERE = re.search(pattern_WHERE, sql_query)

    # Verifica se a palavra foi encontrada
    if match_WHERE:
        parser_where(sql_query)
    else:

        # Define a expressão regular para extrair as colunas e a tabela
        pattern = r"SELECT\s+([\w,\s]+)\s+FROM\s+(\w+);"
        match = re.match(pattern, sql_query)

        # Extrai as colunas e a tabela
        colunas = match.group(1).split(",")
        tabela = match.group(2)

        # Gera a expressão de álgebra relacional correspondente
        expr = "pi {}({})".format(", ".join(colunas), tabela)
        print(expr)


def parser_where(sql_query):
    # Define a expressão regular para extrair as colunas, a tabela e a condição
    pattern = r"SELECT\s+([\w,\s]+)\s+FROM\s+(\w+)\s+WHERE\s+(.+);"
    match = re.match(pattern, sql_query)

    # Extrai as colunas, a tabela e a condição
    colunas = match.group(1).split(",")
    tabela = match.group(2)
    condicao = match.group(3)

    expr = "sigma {}({})".format(condicao, tabela)
    print(expr)