INSERT INTO PROJETO_DE_PESQUISA (id_projeto_pesq, titulo, descricao) 
VALUES (1, 'Título 1', 'Descrição 1'), ();

INSERT INTO PRODUCAO (id_producao, id_projeto_pesq, titulo, tipo, resumo, ano, arquivo) 
VALUES (1, 1, 'Título 1', 'TCC', 'Resumo 1', '2025', pg_read_binary_file('/caminho/arquivo.pdf'));
