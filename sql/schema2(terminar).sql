CREATE TABLE producao(
  idProducao INTEGER PRIMARY KEY,
  tipo INTEGER NOT NULL,
  resumo VARCHAR(1000) NOT NULL,
  ano INTEGER NOT NULL,
  idPP INTEGER,
  FOREIGN KEY (idPP) REFERENCES projetoDePesquisa (idPP)
);

CREATE TABLE projetoDePesquisa(
  idPP INTEGER PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  descricao VARCHAR(500) NOT NULL,
);

CREATE TABLE financiador(
  idFinanciador INTEGER PRIMARY KEY,
  tipo INTEGER NOT NULL,
  nome VARCHAR(100) NOT NULL,
);

CREATE TABLE financiamento(
  idFinanciador INTEGER,
  idPP INTEGER,
  valor INTEGER,
  data TIMESTAMP,
  PRIMARY KEY (idFinanciador, idPP),
  FOREIGN KEY (idFinanciador) REFERENCES financiador (idFinanciador),
  FOREIGN KEY (idPP) REFERENCES projetoDePesquisa (idPP)
);

CREATE TABLE tema(
  idTema INTEGER PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
);

CREATE TABLE palavraChave(
  idPalavraChave INTEGER PRIMARY KEY,
  descricao VARCHAR(500) NOT NULL,
);

CREATE TABLE publicacao(
  idPublicacao INTEGER PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  tipo INTEGER NOT NULL,
  fatorImpacto INTEGER,
  ISBN VARCHAR(17) NOT NULL
);

CREATE TABLE publicacao_producao(
  idPublicacao INTEGER,
  idProducao INTEGER,
  PRIMARY KEY (idPublicacao, idProducao),
  FOREIGN KEY (idPublicacao) REFERENCES publicacao (idPublicacao),
  FOREIGN KEY (idProducao) REFERENCES producao (idProducao)
);
