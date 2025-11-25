INSERT INTO EDITORA (id_editora, nome) VALUES
(1, 'Springer Nature'),
(2, 'Elsevier'),
(3, 'SciELO Brasil'),
(4, 'Editora IME'),
(5, 'IEEE Press'),
(6, 'ACM Books');

INSERT INTO PROJETO_DE_PESQUISA (id_projeto_pesq, titulo, descricao) VALUES
(1, 'Detecção Inteligente de Doenças Respiratórias', 'Projeto utilizando IA e sensores biomédicos para diagnóstico precoce.'),
(2, 'Otimização de Redes LoRaWAN', 'Pesquisa sobre protocolos para comunicação de sensores IoT via LoRa.'),
(3, 'Modelagem Matemática em Biomecânica', 'Estudo de modelos diferenciais aplicados ao movimento humano.'),
(4, 'Sistema de Monitoramento de Bovinos a Pasto', 'Estudo de viabilidade de caso para monitoramento de bovinos via tags RFID.'),
(5, 'Edge AI para Dispositivos de Baixo Consumo', 'Pesquisa sobre modelos reduzidos e quantização para inferência em edge devices.'),
(6, 'Detecção de Anomalias em Redes LoRa', 'Métodos de detecção de falhas e intrusões em redes LoRaWAN.'),
(7, 'Aplicações de Transfer Learning em Biomecânica', 'Uso de transfer learning para análise de movimento com poucos dados rotulados.'),
(8, 'Sistema de Telemetria para Monitoramento Bovino', 'Desenvolvimento de plataforma integrada de telemetria e análise de dados para pecuária.');

INSERT INTO PRODUCAO (id_producao, id_projeto_pesq, titulo, tipo, resumo, ano, arquivo) VALUES
(1, 1, 'Classificação de padrões respiratórios usando CNNs', 'Artigo', 'Apresenta uma CNN capaz de diferenciar padrões respiratórios em sinais biomédicos.', 2023, NULL),
(2, 1, 'TCC - Sistema embarcado para análise de ar', 'TCC', 'Trabalho de conclusão envolvendo microcontroladores e sensores de ar.', 2022, NULL),
(3, 2, 'Análise de desempenho de gateways LoRa', 'Artigo', 'Comparação entre diferentes gateways LoRaWAN em ambientes reais.', 2024, NULL),
(4, 3, 'Modelagem diferencial do movimento humano', 'Tese', 'Tese sobre equações diferenciais aplicadas à biomecânica.', 2023, NULL),
(5, 2, 'Dissertação - Otimização de rotas LoRaWAN', 'Dissertação', 'Aborda algoritmos para melhorar a transmissão em redes LoRa.', 2021, NULL),
(6, 2, 'Dissertação - Otimização de rotas LoRaWAN', 'Dissertação', 'Aborda algoritmos para melhorar a transmissão em redes LoRa.', 2021, NULL),
(7, 1, 'Classificação Avançada de padrões respiratórios usando CNNs', 'Artigo', 'Apresenta uma CNN capaz de diferenciar padrões respiratórios em sinais biomédicos.', 2024, NULL),
(8, 5, 'Redes neurais compactas para classificação em tempo real', 'Artigo', 'Propõe arquiteturas compactas adequadas para execução em microcontroladores.', 2024, NULL),
(9, 6, 'Detecção de anomalias em LoRaWAN usando autoencoders', 'Artigo', 'Autoencoders para identificar padrões de tráfego anômalo em gateways LoRa.', 2025, NULL),
(10, 7, 'Transfer Learning aplicado ao reconhecimento de marcha', 'Dissertação', 'Avalia estratégias de fine-tuning para datasets pequenos em biomecânica.', 2023, NULL),
(11, 8, 'Plataforma de telemetria com análise preditiva para bovinos', 'TCC', 'Implementação de uma solução completa com captura, transmissão e dashboard.', 2025, NULL),
(12, 1, 'Aprimoramento de CNNs para sinais respiratórios', 'Artigo', 'Melhorias arquiteturais e técnicas de augmentação para sinais respiratórios.', 2024, NULL),
(13, 2, 'Estudo sobre Latência em Gateways LoRa Comerciais', 'Artigo', 'Medições de latência e perda de pacotes em diferentes modelos de gateway.', 2023, NULL),
(14, 5, 'Quantização e pruning para microcontroladores', 'Artigo', 'Comparativo de técnicas de compressão de modelos para execução em MCU.', 2025, NULL),
(15, 4, 'Integração de RFID e IoT para Monitoramento de Ativos', 'Artigo', 'Proposta e avaliação de um sistema híbrido RFID-LoRa para rastreio em fazendas.', 2022, NULL),
(16, 1, 'Título 1', 'TCC', 'Resumo 1', 2025, pg_read_binary_file('pdf/TCC1.pdf')),
(17, 1, 'Título 2', 'TCC', 'Resumo 2', 2025, pg_read_binary_file('pdf/TCC2.pdf')),
(18, 1, 'Título 3', 'TCC', 'Resumo 3', 2024, pg_read_binary_file('pdf/TCC3.pdf')),
(19, 1, 'Título 4', 'Tese', 'Resumo 4', 2025, pg_read_binary_file('pdf/TESE.pdf')),
(20, 1, 'Título 5', 'Dissertação', 'Resumo 5', 2025, pg_read_binary_file('pdf/DISSERTACAO.pdf'));

INSERT INTO PUBLICACAO (id_editora, id_producao, ISSN, fatorImpacto) VALUES
(1, 1,  '1000-0001', 2.500),
(3, 2,  '3000-0003', 3.100),
(2, 3,  '2000-0002', 1.850),
(1, 4,  '1000-0001', 2.550),
(2, 5,  '2000-0002', 1.850),
(4, 6,  '4000-0004', 0.950),
(3, 7,  '3000-0003', 3.200),
(1, 8,  '1000-0001', 2.500),
(5, 9,  '5000-0005', 5.200),
(5, 15, '5000-0005', 5.200),
(6, 10, '6000-0006', 1.100),
(1, 11, '1000-0001', 2.500),
(4, 12, '4000-0004', 0.950),
(2, 13, '2000-0002', 1.900),
(3, 14, '3000-0003', 3.100),
(4, 16, '4000-0004', 0.950);

INSERT INTO REFERENCIA (id_producao_referente, id_producao_referenciada) VALUES
(1, 2), (3, 1), (4, 1), (5, 3), (8, 1), (9, 1), (10, 3), (11, 4), (12, 5), (13, 1), (15, 9), (16, 5);

INSERT INTO FINANCIADOR (id_financiador, tipo, nome) VALUES
(1, 'Público', 'CNPq'),
(2, 'Público', 'CAPES'),
(3, 'Privado', 'Samsung Research'),
(4, 'Privado', 'Intel Labs'),
(5, 'Público', 'FAPESC'),
(6, 'Privado', 'Google Research');

INSERT INTO FINANCIAMENTO (id_financiador, id_projeto_pesq, valor, data_financiamento) VALUES
(1, 1, 50000, '2023-01-10'),
(2, 1, 20000, '2023-06-12'),
(3, 2, 75000, '2022-11-03'),
(4, 3, 120000, '2024-02-20'),
(2, 4, 30000, '2025-09-29'),
(5, 5, 85000, '2024-07-30'),
(6, 5, 60000, '2025-03-15'),
(3, 6, 40000, '2024-11-05'),
(1, 8, 45000, '2025-01-20');

INSERT INTO TEMA (id_tema, nome) VALUES
(1, 'Inteligência Artificial'),
(2, 'Internet das Coisas'),
(3, 'Biomecânica'),
(4, 'Processamento de Sinais'),
(5, 'Redes Neurais'),
(6, 'Sistemas Embarcados'),
(7, 'Edge Computing');

INSERT INTO PRODUCAO_TEMA (id_tema, id_producao) VALUES
(1, 1), (4, 1), (1, 2), (2, 3), (2, 5), (3, 4), (5, 9), (6, 9), (5, 11), (6, 12), (7, 15), (2, 16), (1, 13), (4, 13);

INSERT INTO PALAVRA_CHAVE (id_palavra_chave, descricao) VALUES
(1, 'CNN'),
(2, 'Sensores'),
(3, 'LoRaWAN'),
(4, 'Equações Diferenciais'),
(5, 'IA'),
(6, 'Biomecânica'),
(7, 'Quantização'),
(8, 'Pruning'),
(9, 'Autoencoder'),
(10, 'RFID');

INSERT INTO TEMA_PALAVRA_CHAVE (id_tema, id_palavra_chave) VALUES
(1, 1), (1, 5), (2, 2), (2, 3), (3, 6), (4, 4), (5, 7), (5, 8), (5, 9), (3, 10), (2, 9);

INSERT INTO PESSOA (id_pessoa, nome, CPF, email) VALUES
(1, 'Ana Souza', '12345678901', 'ana.souza@example.com'),
(2, 'Carlos Lima', '23456789012', 'carlos.lima@example.com'),
(3, 'Mariana Alves', '34567890123', 'mariana.alves@example.com'),
(4, 'João Ferreira', '45678901234', 'joao.ferreira@example.com'),
(5, 'Luis Moreira', '56789012345', 'luis.moreira@example.com'),
(6, 'Marcos Souza Cruz', '67890123456', 'marcos.pinto@example.com'),
(7, 'Sofia Ramos', '78901234567', 'sofia.ramos@example.com'),
(8, 'Paulo Castro', '89012345678', 'paulo.castro@example.com'),
(9, 'Beatriz Nunes', '90123456789', 'beatriz.nunes@example.com');

INSERT INTO PRODUCAO_PESSOA (id_pessoa, id_producao, tipo) VALUES
(1, 1, 'Professor'),
(2, 1, 'Aluno'),
(3, 2, 'Aluno'),
(1, 3, 'Professor'),
(4, 3, 'Técnico'),
(5, 4, 'Professor'),
(2, 5, 'Aluno'),
(3, 7, 'Aluno'),
(1, 8, 'Professor'),
(6, 9, 'Aluno'),
(7, 10, 'Aluno'),
(8, 11, 'Professor'),
(9, 12, 'Aluno'),
(6, 15, 'Aluno'),
(2, 14, 'Professor'),
(5, 16, 'Professor');

INSERT INTO INSTITUICAO (id_instituicao, nome, endereco) VALUES
(1, 'Universidade Federal de Santa Catarina', 'Florianópolis, SC'),
(2, 'Instituto Tecnológico de São Paulo', 'São Paulo, SP'),
(3, 'Universidade Estadual de Campinas', 'Campinas, SP'),
(4, 'Universidade de São Paulo', 'São Paulo, SP');

INSERT INTO DEPARTAMENTO (id_departamento, id_instituicao, nome) VALUES
(1, 1, 'Departamento de Engenharia Elétrica'),
(2, 1, 'Departamento de Computação'),
(3, 2, 'Departamento de Tecnologia'),
(4, 3, 'Departamento de Engenharia de Computação'),
(5, 4, 'Departamento de Engenharia Biomédica');

INSERT INTO CURSO (id_curso, id_departamento, nome, nivel) VALUES
(1, 2, 'Engenharia de Computação', 'Graduação'),
(2, 1, 'Engenharia Eletrônica', 'Graduação'),
(3, 3, 'Ciência da Computação', 'Mestrado'),
(4, 3, 'Engenharia Biomédica', 'Doutorado'),
(5, 4, 'Mestrado em Sistemas Embarcados', 'Mestrado'),
(6, 5, 'Bacharelado em Engenharia Biomédica', 'Graduação');

INSERT INTO PESSOA_CURSO (id_pessoa, id_curso) VALUES
(1, 4), (2, 1), (3, 1), (4, 3), (5, 2), (6, 5), (7, 5), (8, 6), (9, 6);
