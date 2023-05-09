import re


def sql_to_relational_algebra(sql_query: str):
    tmp_table = ''
    # Padronizando a entrada
    sql_query = sql_query.lower().replace("\n", " ").replace(",", " , ").replace(";","")

    # Verificando se a query é válida

    if not (sql_query.startswith("select") and "from" in sql_query):
        raise ValueError("Consulta SQL inválida")

    # Dividindo a consulta em partes
    select_part, from_part = sql_query.split("from")
    select_part = select_part.replace("select", "").strip()
    from_part = from_part.strip()

    # Verificando se há cláusula WHERE ou JOIN
    where_part = ""
    join_part = ""
    if "where" in from_part:
        from_part, where_part = from_part.split("where")
        where_part = where_part.strip()
    if "join" in from_part:
        join_splited = from_part.split("join")
        tmp_table = join_splited[0]
        # join_part = join_splited[1:]
        join_part = join_splited
        join_part = [join.strip() for join in join_part]

    # Tratando SELECT
    select_cols = re.split(r' *, *', select_part)
    select_str = "π " + ", ".join(select_cols)

    # Tratando FROM
    from_tables = re.split(r' *, *', from_part)
    from_str = "⨝ ".join(from_tables)

    # Tratando JOIN
    join_str = ""
    if join_part:
        for index, join in enumerate(join_part):
            if "on" not in join:
                join_str += f"({join} ⨝  "
                continue
            else:
                table, on_clause = join.split(" on ")
                # join_str += f"{tmp_table}⨝ ({table} ⨝ {' ∧ '.join(join_conditions)})"
                join_conditions = on_clause.replace("=", " = ").split(" and ")
                if index == len(join_part) - 1:
                    join_str += f"{' '.join(join_conditions)} {table})"
                else:
                    join_str += f"{' '.join(join_conditions)} {table} ⨝ "

            # table, on_clause = join.split(" on ")
            # join_str += f"{tmp_table}⨝ ({table} ⨝ {' ∧ '.join(join_conditions)})"

    # Tratando WHERE
    where_str = ""
    if where_part:
        where_conditions = where_part.replace("=", " = ").replace(">", " > ").replace("<", " < ").replace("<=",
                                                                                                          " <= ").replace(
            ">=", " >= ").replace("<>", " <> ").replace(" in ", " ∈ ").replace(" not in ", " ∉ ").split(" and ")
        where_str = "σ " + " ∧ ".join(where_conditions)

    # Combinando os componentes da Álgebra Relacional
    if join_str:
        relational_algebra = f"{select_str}({where_str}({join_str}))"
    else:
        relational_algebra = f"{select_str}({where_str}({from_str}))"

    return relational_algebra
