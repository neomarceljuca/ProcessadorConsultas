Start Transaction ;

Use exercicios;

INSERT INTO `categoria`
(`idCategoria`,
`DescCategoria`)
VALUES
(1,'Salário'),
(2,'Aluguel'),
(3,'Academia'),
(4,'Acessórios'),
(5,'Almoço'),
(6,'Animal de Estimação'),
(7,'Açougue'),
(8,'Bar/Balada'),
(9,'Café/lanches'),
(10,'Celular'),
(11,'Cinema'),
(12,'Combustível'),
(13,'Ônibus'),
(14,'Condomínio'),
(15,'Cursos'),
(16,'Dentista'),
(17,'Eletrônicos'),
(18,'Faculdade'),
(19,'Futebol');

INSERT INTO `usuario`
(`idUsuario`,
`Nome`,
`Logradouro`,
`Número`,
`Bairro`,
`CEP`,
`UF`,
`DataNascimento`)
VALUES
 (1, 'Thanos', 'Rua Suécia', 2330, 'Maraponga', '60000000', 'CE', '1910-05-25'),
 (2, 'Saitama', 'Trashed area', 12, 'Z City', '68485848', 'Z', '2000-06-22'),
 (3, 'Naruto Uzumaki', 'Distrito Norte', 19, 'Silvermoon', '65545665', 'CE', '2000-07-23'),
 (4, 'Kakashi Hatake', 'Vale da Força', 23, 'Ogrimar', '68485848', 'ce', '2000-08-24'),
(5, 'Anakim', 'Vale da Força', 33, 'Ogrimar', '68485848', 'ce', '2000-08-28') ,
(6, 'Darth Lucas Skywalker', 'Vale da Força', 33, 'Ogrimar', '68485848', 'ce', '2000-08-28') ,
 (7, 'Minato Namikaze', 'Av. Santos Dumont', 2313, 'Fortaleza', '60000000', 'CE', '2000-09-25');

INSERT INTO `tipoconta` (`idTipoConta`, `Descrição`) VALUES (1, 'Cartão de Crédito');
INSERT INTO `tipoconta` (`idTipoConta`, `Descrição`) VALUES (2, 'Conta Corrente');

INSERT INTO `tipomovimento` (`idTipoMovimento`, `DescMovimentacao`) VALUES ('1', 'Débito');
INSERT INTO `tipomovimento` (`idTipoMovimento`, `DescMovimentacao`) VALUES ('2', 'Crédito');


INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('1', 'Credicard', '1', '1', '234');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('2', 'Visa', '1', '2', '5124');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('3', 'Banco do Nordeste', '2', '3', '2134');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('4', 'Volkscard', '1', '4', '232');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('5', 'Hipercard', '1', '5', '2345');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('6', 'Bradesco', '2', '6', '234');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('7', 'ChicoCard', '1', '2', '5476');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('8', 'Bitcoin', '2', '4', '554');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('9', 'Palmas', '1', '2', '353');
INSERT INTO `contas` (`idConta`, `Descricao`, `TipoConta_idTipoConta`, `Usuario_idUsuario`, `SaldoInicial`) VALUES ('10', 'Itaú ', '2', '1', '678');

Commit;

