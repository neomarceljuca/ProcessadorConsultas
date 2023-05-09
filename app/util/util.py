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
                join_str += f" ({join} ⨝  "
                continue
            else:
                table, on_clause = join.split(" on ")
                # join_str += f"{tmp_table}⨝ ({table} ⨝ {' ∧ '.join(join_conditions)})"
                join_conditions = on_clause.replace("=", " = ").split(" and ")
                if index == len(join_part) - 1:
                    join_str += f"{' '.join(join_conditions)} {table}) "
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
        where_str = " σ " + " ∧ ".join(where_conditions)

    # Combinando os componentes da Álgebra Relacional
    if join_str:
        relational_algebra = f"{select_str} ( {where_str} ( {join_str} ) ) "
    else:
        relational_algebra = f"{select_str} ( {where_str} ( {from_str} ) ) "

    return relational_algebra.replace("<  >", "<>")

def apply_join_heuristic(expr):
    # Extrair informações das expressões de seleção, projeção e junção
    selection_expr = re.findall(r'σ(.+?)(?=\()', expr)
    projection_expr = re.findall(r'π(.+?)(?=\()', expr)
    join_expr = re.findall(r'⨝(.+?)(?=[(⨝])', expr)

    # Aplicar a heurística da junção
    result = ""

    for join in join_expr:
        join_conditions = join.split(' ∧ ')
        for condition in join_conditions:
            result += f"σ{condition} ( "

    for join in join_expr:
        join_tables = re.findall(r'\b\w+\b', join)
        result += f" ( {join_tables[0]} ⨝ {join_tables[1]} ) "
        result += " ) " * len(join.split(' ∧ '))

    for projection in projection_expr:
        result += f"π{projection} ("

    result += expr[-2]
    result += ")" * (len(selection_expr) + len(projection_expr))

    return result

def apply_heuristics(relational_algebra):
    swords = re.split(r"\s+", relational_algebra)
    selections = []

    for index, token in enumerate(swords):
        if token == "σ":
            selections.append(token)
            aux_index = index + 1
            while swords[aux_index] != "(":
                selections.append(swords[aux_index])
                aux_index +=1
            index = aux_index

    #Find join final order
    joins_order = []
    found_join_symbol = False
    for index, token in enumerate(swords):
        if token == "⨝":
            found_join_symbol = True
            joins_order.append(swords[index-1].replace("(", "").replace(")",""))
        elif ")" in token and found_join_symbol:
            joins_order.append(swords[index].replace("(", "").replace(")",""))
            break

    tmp_selection = " ".join(selections)
    selections = [tmp_selection]
    projections = re.findall(r"π[\w\.,\s]+", relational_algebra)
    joins = re.findall(r"⨝[\w\.,\s=]+", relational_algebra)



    #Apply the selection operation
    selection_filtered = {}

    if len(selections)>0:
        conditions = re.findall(r"[\w\.]+[\s]*[><=]+[\s]*[\w\.]+", selections[0])
        for condition in conditions:
            table_owner_name = re.findall(r"\b\w+\.", condition)[0].replace(".","")
            if table_owner_name in selection_filtered:
                selection_filtered[table_owner_name].append(f"σ {condition}")
            else:
                selection_filtered[table_owner_name] = [f"σ {condition}"]

    #Apply the projection operation
    projection_filtered = {}

    if len(projections)>0:
        # conditions = re.findall(r"[\w\.]+[\s]*[><=]+[\s]*[\w\.]+", selections[0])
        for projection in projections:
            select_cols = re.split(r' *, *', projection)
            for select in select_cols:
                col_name = select.split(".")[1].strip()
                table_owner_name = re.findall(r"\b\w+\.", select)[0].replace(".","")
                if table_owner_name in projection_filtered:
                    if col_name not in projection_filtered[table_owner_name][0]:
                        projection_filtered[table_owner_name][0] += f", {col_name}"
                else:
                    projection_filtered[table_owner_name] = [f"π {col_name}"]


    if len(joins) > 0:
        for join in joins:
            select_cols = re.split(r'=', join)
            for select in select_cols:
                col_name = select.split(".")[1].strip().split(" ")[0]
                table_owner_name = re.findall(r"\b\w+\.", select)[0].replace(".", "")
                # if col_name not in selections[0] and table_owner_name not in selections[0]:
                #     continue
                if table_owner_name in projection_filtered:
                    if col_name not in projection_filtered[table_owner_name][0]:
                        projection_filtered[table_owner_name][0] += f", {col_name}"
                else:
                    projection_filtered[table_owner_name] = [f"π {col_name}"]
            print(join)

    # Apply heuristics:
    # 1. Move selections down the tree (closer to the base tables)
    # 2. Move projections down the tree (closer to the base tables)
    new_selections = []
    for selection in selections:
        conditions = re.findall(r"[\w\.]+[\s]*[><=]+[\s]*[\w\.]+", selection)
        for condition in conditions:
            # Split conditions by the ∧ operator
            parts = condition.split("∧")
            for part in parts:
                new_selections.append("σ " + part.strip())

    # Build the optimized relational algebra string
    join_str = ""

    for index, j_order in enumerate(joins):
        str_projection = None
        str_selection = None
        table_owner_name = joins_order[index]
        if table_owner_name in projection_filtered:
            str_projection = projection_filtered[table_owner_name][0]

        if table_owner_name in selection_filtered:
            str_selection = selection_filtered[table_owner_name][0]

        end_join_str = ""
        end_join = joins[index].split()[-1]

        #Bulding end_join
        end_join_selection = f"( {' '.join(selection_filtered[end_join])} ( {end_join} ) )" if end_join in selection_filtered else f"( {end_join} )"
        end_join_projection = f"{' '.join(projection_filtered[end_join])}" if end_join in projection_filtered else ""

        end_join_str = f"( {end_join_projection} {end_join_selection} )"
        # if end_join in projection_filtered:
        #     end_join_str = f"( {' '.join(projection_filtered[end_join])} {'(' } ({end_join})))"
        tmp_inner_join = joins[index].split()[:-1]
        inner_join_str = " ".join(tmp_inner_join)
        if index == 0:
            join_str += f" ( ( {str_projection} ( {str_selection} ( {table_owner_name} ) ) ) {inner_join_str} {end_join_str} "
        else:
            join_str += f" {inner_join_str} {end_join_str} "
            # if table_owner_name in projection_filtered:
            #     join_str += f"( {str_projection} ( {str_selection} ( {table_owner_name} ) ) ) {inner_join_str} {end_join_str} ) "
            # else:
            #     join_str += f" ⨝ {inner_join_str} ({end_join_str})"
            # join_str += f"( {str_projection} ( {str_selection} ) {joins[index]} )"

    # optimized_relational_algebra = (
    #     f"{projections[0]} ("
    #     f"(π pk, Nome ({new_selections[0]} (Tb1))) {joins[0]} Tb2 "
    #     f"{joins[1]} (π fk, sal ({new_selections[1]} (tb3)))"
    #     f")"
    # )

    print(f"{projections[0]} ( {join_str} )")
    print("H")
    # return optimized_relational_algebra
