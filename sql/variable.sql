-- Retorna o total de producoes filtrado por Editora
SELECT E.nome, COUNT(P.id_producao) AS total_producoes 
FROM PRODUCAO P 
JOIN PRODUCAO_EDITORA PE ON P.id_producao = PE.id_producao 
JOIN EDITORA E ON PE.id_editora = E.id_editora 
GROUP BY E.nome 
ORDER BY total_producoes;