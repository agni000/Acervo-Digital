INSERT INTO EDITORA (id_editora, nome, tipo, fator_impacto, ISBN) VALUES
(1, 'Springer Nature', 1, 4.523, '978-3-16-148410-0'),
(2, 'Elsevier', 1, 5.321, '978-0-12-374856-0'),
(3, 'SciELO Brasil', 2, 2.115, '978-85-359-0277-7');

INSERT INTO PROJETO_DE_PESQUISA (id_projeto_pesq, titulo, descricao) VALUES
(1, 'Detecção Inteligente de Doenças Respiratórias', 'Projeto utilizando IA e sensores biomédicos para diagnóstico precoce.'),
(2, 'Otimização de Redes LoRaWAN', 'Pesquisa sobre protocolos para comunicação de sensores IoT via LoRa.'),
(3, 'Modelagem Matemática em Biomecânica', 'Estudo de modelos diferenciais aplicados ao movimento humano.');

INSERT INTO PRODUCAO (id_producao, id_projeto_pesq, titulo, tipo, resumo, ano, arquivo) VALUES
(1, 1, 'Classificação de padrões respiratórios usando CNNs', 'Artigo', 'Apresenta uma CNN capaz de diferenciar padrões respiratórios em sinais biomédicos.', 2023, NULL),
(2, 1, 'TCC - Sistema embarcado para análise de ar', 'TCC', 'Trabalho de conclusão envolvendo microcontroladores e sensores de ar.', 2022, NULL),
(3, 2, 'Análise de desempenho de gateways LoRa', 'Artigo', 'Comparação entre diferentes gateways LoRaWAN em ambientes reais.', 2024, NULL),
(4, 3, 'Modelagem diferencial do movimento humano', 'Tese', 'Tese sobre equações diferenciais aplicadas à biomecânica.', 2023, NULL),
(5, 2, 'Dissertação - Otimização de rotas LoRaWAN', 'Dissertação', 'Aborda algoritmos para melhorar a transmissão em redes LoRa.', 2021, NULL);

INSERT INTO PRODUCAO_EDITORA (id_editora, id_producao) VALUES
(1, 1), (3, 2), (2, 3), (1, 4), (2, 5);

INSERT INTO REFERENCIA (id_producao_referente, id_producao_referenciada) VALUES
(1, 2), (3, 1), (4, 1), (5, 3);

INSERT INTO FINANCIADOR (id_financiador, tipo, nome) VALUES
(1, 'Público', 'CNPq'),
(2, 'Público', 'CAPES'),
(3, 'Privado', 'Samsung Research'),
(4, 'Privado', 'Intel Labs');

INSERT INTO FINANCIAMENTO (id_financiador, id_projeto_pesq, valor, data_financiamento) VALUES
(1, 1, 50000, '2023-01-10'),
(2, 1, 20000, '2023-06-12'),
(3, 2, 75000, '2022-11-03'),
(4, 3, 120000, '2024-02-20');

INSERT INTO TEMA (id_tema, nome) VALUES
(1, 'Inteligência Artificial'),
(2, 'Internet das Coisas'),
(3, 'Biomecânica'),
(4, 'Processamento de Sinais');

INSERT INTO PRODUCAO_TEMA (id_tema, id_producao) VALUES
(1, 1), (4, 1), (1, 2), (2, 3), (2, 5), (3, 4);

INSERT INTO PALAVRA_CHAVE (id_palavra_chave, descricao) VALUES
(1, 'CNN'),
(2, 'Sensores'),
(3, 'LoRaWAN'),
(4, 'Equações Diferenciais'),
(5, 'IA'),
(6, 'Biomecânica');

INSERT INTO TEMA_PALAVRA_CHAVE (id_tema, id_palavra_chave) VALUES
(1, 1), (1, 5), (2, 2), (2, 3), (3, 6), (4, 4);

INSERT INTO PESSOA (id_pessoa, nome, CPF, email) VALUES
(1, 'Ana Souza', '12345678901', 'ana.souza@example.com'),
(2, 'Carlos Lima', '23456789012', 'carlos.lima@example.com'),
(3, 'Mariana Alves', '34567890123', 'mariana.alves@example.com'),
(4, 'João Ferreira', '45678901234', 'joao.ferreira@example.com'),
(5, 'Luis Moreira', '56789012345', 'luis.moreira@example.com');

INSERT INTO PRODUCAO_PESSOA (id_pessoa, id_producao, tipo) VALUES
(1, 1, 'Professor'),
(2, 1, 'Aluno'),
(3, 2, 'Aluno'),
(1, 3, 'Professor'),
(4, 3, 'Técnico'),
(5, 4, 'Professor'),
(2, 5, 'Aluno');

INSERT INTO INSTITUICAO (id_instituicao, nome, endereco) VALUES
(1, 'Universidade Federal de Santa Catarina', 'Florianópolis, SC'),
(2, 'Instituto Tecnológico de São Paulo', 'São Paulo, SP');

INSERT INTO DEPARTAMENTO (id_departamento, id_instituicao, nome) VALUES
(1, 1, 'Departamento de Engenharia Elétrica'),
(2, 1, 'Departamento de Computação'),
(3, 2, 'Departamento de Tecnologia');

INSERT INTO CURSO (id_curso, id_departamento, nome, nivel) VALUES
(1, 2, 'Engenharia de Computação', 'Graduação'),
(2, 1, 'Engenharia Eletrônica', 'Graduação'),
(3, 3, 'Ciência da Computação', 'Mestrado'),
(4, 3, 'Engenharia Biomédica', 'Doutorado');

INSERT INTO PESSOA_CURSO (id_pessoa, id_curso) VALUES
(1, 4), (2, 1), (3, 1), (4, 3), (5, 2);
