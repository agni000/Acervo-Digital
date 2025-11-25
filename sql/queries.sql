-- Retorna o total de producoes filtrado por Editora
SELECT E.nome, COUNT(P.id_producao) AS total_producoes 
FROM PRODUCAO P 
JOIN PUBLICACAO PU ON P.id_producao = PU.id_producao 
JOIN EDITORA E ON PU.id_editora = E.id_editora 
GROUP BY E.nome 
ORDER BY total_producoes;

-- Retorna o valor medio de financiamento por financiador
SELECT F.nome, AVG(FI.valor) AS valor_medio_financiamento 
FROM FINANCIAMENTO FI 
JOIN FINANCIADOR F ON FI.id_financiador = F.id_financiador 
JOIN PROJETO_DE_PESQUISA PP ON FI.id_projeto_pesq = PP.id_projeto_pesq 
GROUP BY F.nome 
ORDER BY valor_medio_financiamento;

-- Retorna o numero de producoes por pessoa
SELECT P.nome, COUNT(PP.id_producao) AS numero_producoes 
FROM PRODUCAO_PESSOA PP 
JOIN PESSOA P ON PP.id_pessoa = P.id_pessoa 
JOIN PRODUCAO PR ON PP.id_producao = PR.id_producao 
GROUP BY P.nome
ORDER BY numero_producoes
