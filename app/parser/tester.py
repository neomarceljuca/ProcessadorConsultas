from validator import SQLQueryValidator

# Create SQL query validator instance
validator = SQLQueryValidator()
#parser = Parser()

# Sample SQL queries to validate
query1 = "Select id, name, email From users Where id = 1;"
query2 = "SELECT name, price FROM productsThisTableDoesntExist WHERE price < 10.0 ORDER BY name;"
query3 = "SELECT Nome, DataNascimento, Descricao, SaldoInicial FROM Usuario join Contas on Usuario.idUsuario = Contas.Usuario_idUsuario WHERE SaldoInicial >= 235 and UF ='ce' and CEP <> '62930000';"
query4 = "SELECT idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição FROM usuario join contas on usuario.idUsuario = contas.Usuario_idUsuario join tipoconta on tipoconta.idTipoConta = contas.TipoConta_idTipoConta WHERE saldoinicial < 3000 and uf = 'ce' and Descrição <> 'Conta Corrente' and idusuario > 3; "
query5 = "SELECT idUsuario FROM Usuario JOIN Contas ON Usuario.idUsuario = Contas.Usuario_idUsuario;"
query6 = "SELECT idUsuario FROM Usuario;"

# Validate SQL queries
print(validator.validate_query(query1))  # True
print(validator.validate_query(query2))  # False
print(validator.validate_query(query3))  # True
print(validator.validate_query(query4))  # True
print(validator.validate_query(query5))  # True
print(validator.validate_query(query6))  # True


