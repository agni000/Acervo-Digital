-- Retorna o numero de producoes por pessoa
SELECT P.nome, COUNT(PP.id_producao) AS numero_producoes 
FROM PRODUCAO_PESSOA PP 
JOIN PESSOA P ON PP.id_pessoa = P.id_pessoa 
JOIN PRODUCAO PR ON PP.id_producao = PR.id_producao 
GROUP BY P.nome
ORDER BY numero_producoes