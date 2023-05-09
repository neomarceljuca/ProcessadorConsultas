from validator import SQLQueryValidator
from app.util.util import sql_to_relational_algebra, apply_heuristics

# Create SQL query validator instance
validator = SQLQueryValidator()
#parser = Parser()

# Sample SQL queries to validate
# query1 = "Select id, name, email From users Where id = 1;"
query1 = "Select Tb1.Nome, tb3.sal From Tb1 Join Tb2 on tb1.pk = tb2.fk Join tb3 on tb2.pk = tb3.fk Where tb1.id > 300 and tb3.sal <> 0"
query2 = "SELECT name, price FROM productsssszzz WHERE price < 10.0;"
query3 = "SELECT Nome, DataNascimento, Descricao, SaldoInicial FROM Usuario join Contas on Usuario.idUsuario = Contas.Usuario_idUsuario WHERE SaldoInicial >= 235 and UF ='ce' and CEP <> '62930000';"
query4 = "SELECT idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição FROM usuario join contas on usuario.idUsuario = contas.Usuario_idUsuario join tipoconta on tipoconta.idTipoConta = contas.TipoConta_idTipoConta WHERE saldoinicial < 3000 and uf = 'ce' and Descrição <> 'Conta Corrente' and idusuario > 3; "
query5 = "SELECT idUsuario FROM Usuario JOIN Contas ON Usuario.idUsuario = Contas.Usuario_idUsuario;"
query6 = "SELECT idUsuario FROM Usuario;"

# Relational Algebra Parser Test
print("1")
rel_alg = sql_to_relational_algebra(query1)
print(rel_alg)
print(apply_heuristics(rel_alg))
# print("2")
# print(sql_to_relational_algebra(query2))
# print("3")
# print(sql_to_relational_algebra(query3))
# print("4")
# print(sql_to_relational_algebra(query4))
# print("5")
# print(sql_to_relational_algebra(query5))
# print("6")
# print(sql_to_relational_algebra(query6))


# # Validate SQL queries
# print(validator.validate_query(query1))  # True
# print(validator.validate_query(query2))  # False
# print(validator.validate_query(query3))  # True
# print(validator.validate_query(query4))  # True
# print(validator.validate_query(query5))  # True
# print(validator.validate_query(query6))  # True


