import re
# from parser.validator import SQLQueryValidator

def validate(sql_query):
    validator = SQLQueryValidator()
    return validator.validate_query(sql_query)

def parser(sql_query):
    return

def extrair_colunas(query):
    regex = r"([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)"
    colunas = re.findall(regex, query)
    return colunas

def is_table_in_array(table_name, array):
    return any(table_name in column for column in array)

def encontrar_posicoes(array, string):
    posicoes = []
    for i in range(len(array)):
        if string in array[i].lower():
            posicoes.append(i)
    return posicoes


def sql_to_relational_algebra(query):
    query = query.lower()
    pattern = r"select\s+(.*?)\s+from\s+(.*)"
    pattern2 = r"from\s+(\w+)"
    expr = ""

    tables = []
    cols = []
    selected_columns = []
    unions = []
    selections = []
    conditions = []

    match = re.match(pattern, query)
    main_table = re.search(pattern2, query)
    

    # Se o pattern tiver match, ou seja se a base da query for SELECT * FROM ...;
    if match:
        # Extrai as colunas da query, todas as colunas que estiver entre o SELECT e o FROM;
        selected_columns = [col.strip() for col in match.group(1).split(",")]
        # Procura os JOIN * ON ...;
        padrao_join = re.compile(r'join \w+ on \w+\.\w+ = \w+\.\w+') 
        joins = padrao_join.findall(match.group(2))

        # Procura os WHERE *;
        padrao_where = re.compile(r'where\s+(.*)')
        wheres = padrao_where.findall(match.group(2))


        # Se tiver o padrão JOIN * ON * ...;
        if joins is not None:
            first_run = True
            for i in joins:
                padrao_join = re.compile(r'join\s+(\w+)\s+on\s+(\w+\.\w+)\s+=\s+(\w+\.\w+)')
                joins_ = padrao_join.findall(i)
                padrao_onde = r"(?<=on\s).*"
                ondes = re.search(padrao_onde, i)
                aux = ondes.group(0).split(" = ")
                cols.extend(aux)
                if first_run:
                    unions.append(f"{main_table.group(1)} |X| {ondes.group(0)} {joins_[0][0]}")
                    tables.append(main_table.group(1))
                    tables.append(joins_[0][0])
                    first_run = False
                else:
                    unions.append(f"|X| {ondes.group(0)} {joins_[0][0]}")
                    tables.append(joins_[0][0])
        
        # Se tiver o padrão WHERE *;
        if len(wheres) > 0:
            conditions = []
            conditions.append(f"sigma {wheres[0]}")
        

        columns = ", ".join(selected_columns)
        expr_union = ""

        if unions:
            expr_union = f"{unions[0]}"
            for i in range(1, len(unions)):
                expr_union = f"( {expr_union} ) {unions[i]}"


        if conditions and unions: 
            expr = f"pi {columns} ( {conditions[0]} ( {expr_union} ) )"
            print(expr)
            strictly_cols = cols + selected_columns
            strictly_cols = list(set(strictly_cols))
            print(f"colunas: {cols}")
            print(f"colunas principais: {selected_columns}")
            print(f"condição: {conditions[0]}")
            print(f"colunas estritamente necessárias: {strictly_cols}")
            print(f"tabelas: {tables}")
            print(f"expressão união: {expr_union}")


            sigma_split = conditions[0].split("sigma")
            and_split = sigma_split[1].split("and")
            # print("-----")
            # print(f"and_split: {and_split}")
            flag = False
            
            expr_union_v2 = expr_union.split(" ")
            a_ = [None] * len(expr_union_v2)
            b_ = []
            # print(f"expr_union_v2: {expr_union_v2}")

            # Pegando apenas os valores que satisfaçam as condições
            for i in range(len(expr_union_v2)):
                for j in range(len(and_split)):
                    # print(f"comparando {expr_union_v2[i]} com {and_split[j]}")
                    # se o expr_union_v2[i] for uma tabela e estiver dentro do array and_split que é um array com condições ele entra no if;
                    if expr_union_v2[i] in and_split[j] and tables.__contains__(expr_union_v2[i]):
                        # print(f"{expr_union_v2[i]} está em {and_split[j]} onde a posiçao é {i} para o array expr_union_v2 e {j} para o array and_split")
                        a_[i] = a_[i] +"^"+ and_split[j] if a_[i] != None else f"{and_split[j]}"
                        flag = True
                        for x in strictly_cols:
                            a = x.split(".")
                            if expr_union_v2[i] in a[0]:
                                b_.append(x)

                if tables.__contains__(expr_union_v2[i]) and flag == False:
                    # print("apenas uma tabela")
                    for x in strictly_cols:
                        a = x.split(".")
                        if expr_union_v2[i] in a[0]:
                            # print(f"tabela {expr_union_v2[i]} precisa das colunas {x}")
                            b_.append(x)
                                
    
                if flag:
                    if len(b_) > 0:
                        _b_ = ", ".join(b_)
                        expr_union_v2[i] = f" ( pi {_b_} ( sigma {a_[i]} ( {expr_union_v2[i]} ) ) )"
                        b_.clear()
                        # a_[i] = f"pi  ({a_[i]})"
                        
                    flag = False
                else: 
                    if len(b_) > 0:
                        _b_ = ", ".join(b_)
                        expr_union_v2[i] = f" ( pi {_b_} ( {expr_union_v2[i]} ) ) "
                        b_.clear()


            # print(f"{a_}")
            expr_union_v2 = " ".join(expr_union_v2)
            print("-- 3 heuristica  --")
            # print(f"{expr_union_v2}")
            expr = f"pi {columns} ( {expr_union_v2} )"

            # print(expr)
            

        if conditions and not unions: 
            expr = f"pi {columns} ( {conditions[0]} ( {main_table.group(1)} ) )"
            print(expr)

        if not conditions and unions:
            expr = f"pi {columns} ({expr_union})"
            print(expr)
            strictly_cols = cols + selected_columns
            strictly_cols = list(set(strictly_cols))
            # print(f"colunas: {cols}")
            # print(f"colunas principais: {selected_columns}")
            # print(f"colunas estritamente necessárias: {strictly_cols}")
            # print(f"tabelas: {tables}")
            # print(f"expressão união: {expr_union}")

            expr_union_v2 = expr_union.split(" ")
            b_ = []
            for i in range(len(expr_union_v2)):
                if tables.__contains__(expr_union_v2[i]):
                    # print(f"{expr_union_v2[i]} é uma tabela")
                    for x in strictly_cols:
                        a = x.split(".")
                        if expr_union_v2[i] in a[0]:
                            # print(f"tabela {expr_union_v2[i]} precisa das colunas {x}")
                            b_.append(x)
                
                if len(b_) > 0:
                        _b_ = ", ".join(b_)
                        expr_union_v2[i] = f" ( pi {_b_} ( {expr_union_v2[i]} ) ) "
                        b_.clear()
            expr_union_v2 = " ".join(expr_union_v2)
            # print(expr_union_v2)
            expr = f"pi {columns} ( {expr_union_v2} )"
            print(expr)



        if not conditions and not unions:
            expr = f"pi {columns} ({main_table.group(1)})"
            print(expr)
            
        # print(expr)


# sql_to_relational_algebra("SELECT usuario.nome, usuario.datanascimento, contas.descricao, contas.saldoinicial FROM usuario JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario WHERE contas.saldoinicial >= 235 AND usuario.uf = 'ce' AND usuario.cep <> '62930000'")
print("--------")
# sql_to_relational_algebra("SELECT usuario.idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição FROM usuario JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario JOIN tipoconta ON tipoconta.idTipoConta = contas.TipoConta_idTipoConta")
# sql_to_relational_algebra("SELECT table1.column1, table2.column2, table3.column3, table4.column4 FROM table1 JOIN table2 ON table1.column1 = table2.column2 JOIN table3 ON table2.column2 = table3.column3 JOIN table4 ON table3.column3 = table4.column4 WHERE table1.column1 = 'value'")

# sql_to_relational_algebra("SELECT nome, datanascimento, descricao, saldoinicial FROM usuario")
# sql_to_relational_algebra("SELECT tb1.Nome, tb3.sal FROM tb1 JOIN tb2 ON tb1.pk = tb2.fk JOIN tb3 ON tb2.pk = tb3.fk WHERE tb1.id > 300 AND tb3.sal <> 0")
# sql_to_relational_algebra("SELECT tb1.Nome, tb1.cpf, tb3.sal, tb2.coluna FROM tb1 JOIN tb2 ON tb1.pk = tb2.fk JOIN tb3 ON tb2.pk = tb3.fk WHERE tb1.id > 300 AND tb3.sal <> 0")
# sql_to_relational_algebra("SELECT usuario.nome, contas.saldo FROM usuario JOIN contas ON usuario.id = contas.fk WHERE usuario.nome <> 'francisco'")
# sql_to_relational_algebra("SELECT usuario.nome, contas.saldo FROM usuario JOIN contas ON usuario.id = contas.fk")
# print("--------")
# sql_to_relational_algebra("SELECT usuario.nome, contas.saldo, table3.col3 FROM usuario JOIN contas ON usuario.id = contas.fk JOIN table3 ON contas.pk = table3.col3")
# sql_to_relational_algebra("SELECT usuario.nome FROM usuario JOIN contas ON usuario.id = contas.fk JOIN table3 ON contas.pk = table3.col3")
sql_to_relational_algebra("SELECT usuario.nome FROM usuario WHERE usuario.id > 300 AND usuario.nome <> 'Josef'")
print("--------")
sql_to_relational_algebra("SELECT nome FROM usuario")