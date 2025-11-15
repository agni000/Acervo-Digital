SELECT p.id_producao, p.titulo, e.nome AS editora
FROM PRODUCAO p
JOIN PRODUCAO_EDITORA pe ON pe.id_producao = p.id_producao
JOIN EDITORA e ON e.id_editora = pe.id_editora;