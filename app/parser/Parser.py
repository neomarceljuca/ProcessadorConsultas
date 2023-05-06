import re
from parser.validator import SQLQueryValidator

def validate(sql_query):
    validator = SQLQueryValidator()
    return validator.validate_query(sql_query)

def parser(sql_query):
    return

def sql_to_relational_algebra(query):

    pattern = r"SELECT\s+(.*?)\s+FROM\s+(.*)"
    pattern2 = r"FROM\s+(\w+)"
    expr = ""
    unions = []
    selections = []
    conditions = []

    match = re.match(pattern, query)
    main_table = re.search(pattern2, query)
    

    # Se o pattern tiver match, ou seja se a base da query for SELECT * FROM ...;
    if match:
        # Extrai as colunas da query, todas as colunas que estiver entre o SELECT e o FROM;
        selected_columns = [col.strip() for col in match.group(1).split(",")]
        selections.append(f"pi {selected_columns} ({main_table.group(1)})")
        
        # Procura os JOIN * ON ...;
        padrao_join = re.compile(r'JOIN \w+ ON \w+\.\w+ = \w+\.\w+') 
        joins = padrao_join.findall(match.group(2))

        # Procura os WHERE *;
        padrao_where = re.compile(r'WHERE\s+(.*)')
        wheres = padrao_where.findall(match.group(2))


        # Se tiver o padrão JOIN * ON * ...;
        if joins is not None:
            first_run = True
            for i in joins:
                padrao_join = re.compile(r'JOIN\s+(\w+)\s+ON\s+(\w+\.\w+)\s+=\s+(\w+\.\w+)')
                joins_ = padrao_join.findall(i)
                padrao_onde = r"(?<=ON\s).*"
                ondes = re.search(padrao_onde, i)
                if first_run:
                    unions.append(f"{main_table.group(1)} |X| {ondes.group(0)} {joins_[0][0]}")
                    first_run = False
                else:
                    unions.append(f"|X| {ondes.group(0)} {joins_[0][0]}")
        
        # Se tiver o padrão WHERE *;
        if len(wheres) > 0:
            conditions = []
            conditions.append(f"sigma {wheres[0]}")
        
        # print(selections)
        # print(conditions)
        # print(conditions)

        columns = ", ".join(selected_columns)
        expr_union = ""

        if unions:
            expr_union = unions[0]
            for i in range(1, len(unions)):
                expr_union = f"({expr_union}) {unions[i]}"

        if conditions and unions: 
            expr = f"pi {columns} ({conditions[0]} ({expr_union}))"

        if conditions and not unions: 
            expr = f"pi {columns} ({conditions[0]})"

        if not conditions and unions:
            expr = f"pi {columns} ({expr_union})"

        if not conditions and not unions:
            expr = f"pi {columns} ({main_table.group(1)})"

        print(expr)
        # print(selected_columns)
        # print(main_table.group(1))


# sql_to_relational_algebra("SELECT nome, datanascimento, descricao, saldoinicial FROM usuario JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario WHERE saldoinicial >=235 AND uf ='ce' AND cep <> '62930000'")
# sql_to_relational_algebra("SELECT idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição FROM usuario JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario JOIN tipoconta ON tipoconta.idTipoConta = contas.TipoConta_idTipoConta")
# sql_to_relational_algebra("SELECT a.column1, b.column2, c.column3, d.column4 FROM table1 JOIN table2 ON a.column1 = b.column2 JOIN table3 ON b.column2 = c.column3 JOIN table4 ON c.column3 = d.column4 WHERE a.column1 = 'value'")
# sql_to_relational_algebra("SELECT nome, datanascimento, descricao, saldoinicial FROM usuario")
