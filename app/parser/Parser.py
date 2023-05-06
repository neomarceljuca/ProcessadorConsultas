import re


# def parser(sql_query):

def sql_to_relational_algebra(query):

    pattern = r"SELECT\s+(.*?)\s+FROM\s+(.*)"
    pattern2 = r"FROM\s+(\w+)"
    unions = []
    selections = []
    conditions = []

    match = re.match(pattern, query)
    main_table = re.search(pattern2, query)
    
    # print(match.group(1))
    # print(main_table.group(1))

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
        if wheres is not None:
            conditions = []
            conditions.append(f"sigma {wheres[0]} ({main_table.group(1)})")
        
        print(selections)
        print(conditions)
        print(unions)
        # print(selected_columns)
        # print(main_table.group(1))


sql_to_relational_algebra("SELECT nome, datanascimento, descricao, saldoinicial FROM usuario JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario WHERE saldoinicial >=235 AND uf ='ce' AND cep <> '62930000';")
# sql_to_relational_algebra("SELECT idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição FROM usuario JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario JOIN tipoconta ON tipoconta.idTipoConta = contas.TipoConta_idTipoConta WHERE saldoinicial < 3000 AND uf = 'ce' AND Descrição <> 'Conta Corrente' AND idusuario > 3;")
