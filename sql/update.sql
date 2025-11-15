UPDATE PESSOA
SET email = 'ana.souza.nova@example.com'
WHERE id_pessoa = 1;

UPDATE PRODUCAO
SET ano = 2023
WHERE id_producao = 2;

UPDATE FINANCIAMENTO
SET valor = valor + 10000
WHERE id_financiador = 1 AND id_projeto_pesq = 1;

UPDATE EDITORA
SET fator_impacto = 4.850
WHERE id_editora = 1;
