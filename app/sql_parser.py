import re
from collections import namedtuple

# Defina as estruturas de dados para armazenar os componentes da consulta
Select = namedtuple("Select", ["columns"])
From = namedtuple("From", ["tables"])
Where = namedtuple("Where", ["conditions"])
Join = namedtuple("Join", ["table", "condition"])

table_fields ={
            "*":["*"],
            # "users": ["id", "name", "email"],
            # "orders": ["id", "user_id", "product_id"],
            # "products": ["id", "name", "price"],
            "usuario": ["idusuario", "nome", "logradouro", "número", "bairro", "cep", "uf", "datanascimento"],
            "contas": ["idconta", "descricao", "tipoconta_idtipoconta", "usuario_idusuario", "saldoinicial"],
            "tipoconta": ["idtipoconta", "descrição"],
            "tipomovimento": ["idtipomovimento", "descmovimentacao"],
            "categoria": ["idcategoria", "desccategoria"],
            "movimentacao": ["idmovimentacao","datamovimentacao","descricao","tipomovimento_idtipomovimento","categoria_idcategoria", "contas_idconta"]
        }


class SQLParser:
    def __init__(self, query):
        self.query = query
        self.fixedQuery = query
        self.tokens = self.tokenize()
        self.default_tokens = ["and"]
        self.comparison_ops = {"=", "<>", "<", "<=", ">", ">=", "in", "not"}

    def tokenize(self):
        query = re.sub(r"\s+", " ", self.query).strip().lower()
        tokens = re.findall(r"[\w._\u00C0-\u017F]+|'.*?'|[,=><!]+", query)
        return tokens
    
    
    def parse(self):
        select = self.parse_select()
        from_ = self.parse_from()
        where = self.parse_where()
        joins = self.parse_joins()

        return {"select": select, "from": from_, "where": where, "joins": joins}

    def parse_select(self):
        if self.tokens[0] != "select":
            raise ValueError("A consulta deve começar com SELECT")

        columns = []
        i = 1
        while self.tokens[i] != "from":
            if self.tokens[i] != "," and self.tokens[i].lower() != "from":
                    
                        
                columns.append(self.tokens[i])
            i += 1


        columns = self.parse_columns(columns)
        return Select(columns)

    def parse_from(self):
        i = self.tokens.index("from")
        tables = []
            

        while self.tokens[i] not in ("where", "join"):
            if self.tokens[i] != "," and self.tokens[i].lower() != "from":
                tables.append(self.tokens[i])
            i += 1
            if i > len(self.tokens) -1:
                break
        self.parse_tables(tables)
        return From(tables)

    def parse_where(self):
        if "where" not in self.tokens:
            return None
        
        a = self.tokens.index("where") + 1

        while self.tokens[a] not in ("where", "join"):
            if a > len(self.tokens) -1:
                break
            if self.tokens[a] != "," and self.tokens[a].lower() != "from":
                prop = self.tokens[a]
                if "." in prop:
                    tablename, col = prop.split(".")
                    if col not in table_fields[tablename]:
                        raise ValueError(f"A coluna {col} não pertence a tabela {tablename}.")
                elif self.tokens[a-1] == "where":
                    self.tokens[a] = self.parse_columns([self.tokens[a]])[0]
            if a >= len(self.tokens) -1:
                break
            a+= 1

        i = self.tokens.index("where") + 1
        conditions = []

        while i < len(self.tokens) and (self.tokens[i] != "join" or i + 5 >= len(self.tokens)):
            if self.tokens[i + 1] == "not" and self.tokens[i + 2] != "in":
                raise ValueError(f"Operador inválido: {self.tokens[i + 2]}")
            if self.tokens[i + 1] == "in" or (self.tokens[i + 1] == "not" and self.tokens[i + 2] == "in"):
                operator = self.tokens[i + 1] if self.tokens[
                                                     i + 1] == "in" else f"{self.tokens[i + 1]} {self.tokens[i + 2]}"
                in_values_start = i + 2 if operator == "in" else i + 3
                in_values_end = in_values_start

                while in_values_end < len(self.tokens) and (self.tokens[in_values_end] != ")" and
                                                            self.tokens[in_values_end] not in self.default_tokens):
                    in_values_end += 1

                in_values = [token for token in self.tokens[in_values_start:in_values_end] if token != ',']
                condition = (self.tokens[i], operator, in_values)
                i = in_values_end + 1
            else:
                if self.tokens[i + 1] not in self.comparison_ops:
                    raise ValueError(f"Operador inválido: {self.tokens[i + 1]}")
                condition = (self.tokens[i], self.tokens[i + 1], self.tokens[i + 2])
                i += 4

            conditions.append(condition)

        conditionsIndex = 0
        for c in conditions:
            prop = c[0]
            if "." not in prop:
                c = (self.parse_columns([c[0]])[0], c[1],c[2])
                print(prop)
                conditions[conditionsIndex] = c
            conditionsIndex += 1
        return Where(conditions)

    def parse_joins(self):
        joins = []

        # a = self.tokens.index("where") + 1

        # while self.tokens[a] not in ("where", "join"):
        #     if self.tokens[a] != "," and self.tokens[a].lower() != "from":
        #         prop = self.tokens[a]
        #         if "." in prop:
        #             tablename, col = prop.split(".")
        #             if col not in table_fields[tablename]:
        #                 raise ValueError(f"A coluna {col} não pertence a tabela {tablename}.")
        #     a+= 1

        while "join" in self.tokens:
            i = self.tokens.index("join")
            table = self.tokens[i + 1]
            condition = (self.tokens[i + 3], self.tokens[i + 4], self.tokens[i + 5])
            joins.append(Join(table, condition))
            self.tokens.pop(i)

        for join in joins:
            cond = join[1]
            for c in cond:
                if "." in c:
                    tablename, col = c.split(".")
                    if col not in table_fields[tablename]:
                        raise ValueError(f"A coluna {col} não pertence a tabela {tablename}")
        return joins
    
    def parse_tables(self, tables):
        found = False
        for table in tables:
            if table.lower()  in table_fields:
                found = True
            else:
                raise ValueError("Tabela " + table  + " nao encontrada")
            
    def replace_substring(self, input_string, old_substring, new_substring):
        pattern = r'(?<!\w)(?<!\.)' + re.escape(old_substring) + r'(?!\w)'
        modified_string = re.sub(pattern, new_substring, input_string)
        return modified_string     

    def parse_columns(self, columns):

        table_field_names = table_fields.keys()
        completeColumns = []
        tableName = ""
        # for column in columns:
        #     column = column.split('.')[1]  if '.' in column else column
        #     found = False
        #     for fields in table_fields.values():
        #         if column.lower()  in fields:
        #             found = True
        #     if not found:
        #         raise ValueError("Campo " + column  + " nao encontrado")  

        for column in columns:
            if '.' not in column:   
                for key, value in table_fields.items():
                    tableName = ""
                    if column in value:
                        tableName = key
                        
                        completeColumns.append(tableName + "." + column)
                        #newFixedQuery = self.fixedQuery.replace(column, tableName + "." + column)
                        newFixedQuery = self.replace_substring(self.fixedQuery, column, tableName + "." + column)
                        self.fixedQuery = newFixedQuery
                        break
            if tableName == "": raise ValueError("Tabela " + tableName  + " nao possui campo " + column)
            found = False
            for fields in table_fields.values():
                if column.lower()  in fields:
                    found = True

            if not found:
                raise ValueError("Campo " + column  + " nao encontrado")  
        
        i = 0

        for col in columns:
            for key in list(table_field_names):
                if key == "*":
                    continue
                prop_values = table_fields[key]

                if col in prop_values:
                        if col not in ["select", "from", "on", "int", "not", "join"]:
                            col = f"{key}.{col}"
        
        return completeColumns
                    

    def sql_dict_to_relational_algebra(self, sql_dict):
        select = sql_dict.get('select')
        from_clause = sql_dict.get('from')
        where = sql_dict.get('where')
        joins = sql_dict.get('joins')

        # Processa a cláusula SELECT
        projection_columns = ', '.join(select.columns)
        projection = f'Π {projection_columns}'

        # Processa a cláusula FROM
        base_relation = from_clause.tables[0]
        relational_expr = f'({base_relation})'

        # Processa as cláusulas JOIN
        if joins:
            for join in joins:
                join_table = join.table
                join_condition = f"{join.condition[0]} {join.condition[1]} {join.condition[2]}"
                relational_expr = f'({relational_expr} ⨝_{join_condition} {join_table})'

        # Processa a cláusula WHERE
        if where:
            conditions = []
            for condition in where.conditions:
                cond_str = f"{condition[0]} {condition[1]} {condition[2]}"
                conditions.append(cond_str)

            conditions_str = ' ∧ '.join(conditions)
            relational_expr = f'σ ({conditions_str}) ({relational_expr})'

        # Combina tudo
        result = f'{projection} ({relational_expr})'

        return result