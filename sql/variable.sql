-- Retorna o total de producoes filtrado por Editora
SELECT E.nome, COUNT(P.id_producao) AS total_producoes 
FROM PRODUCAO P 
JOIN PUBLICACAO PU ON P.id_producao = PU.id_producao 
JOIN EDITORA E ON PU.id_editora = E.id_editora 
GROUP BY E.nome 
ORDER BY total_producoes;
