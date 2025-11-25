<p align = "center"><b>Acervo Digital</b></p>
<p align = "justify">O projeto tem como objetivo desenvolver um acervo digital voltado à organização e consulta de trabalhos acadêmicos, artigos científicos e produções universitárias em geral. A aplicação permitirá o armazenamento estruturado de informações sobre autores, orientadores, cursos, áreas temáticas e instituições, possibilitando buscas eficientes e consultas analíticas sobre os dados cadastrados. Além de servir como ferramenta de apoio à gestão do conhecimento acadêmico, o sistema integrará recursos de inteligência artificial generativa para auxiliar o usuário na contextualização e resumo de trabalhos. Assim, o projeto visa oferecer uma plataforma útil tanto para alunos quanto para pesquisadores, promovendo o acesso e a organização do conteúdo científico institucional.</p>

## Modelo Conceitual
<div align="center">
    <img src="assets/MD-Conceitual.png">
</div>

---

## Modelo Lógico

```mermaid
%%{init: {
    'theme': 'base',
    'themeVariables': {
        'background': '#FFFFFF',
        'primaryColor': '#2E5A88',
        'primaryBorderColor': '#1B3C5D',
        'primaryTextColor': '#FFFFFF',
        'lineColor': '#2E5A88'
    }
}}%%

erDiagram

    %% --------------------- TEMA -----------------------
    Tema {
        int idTema PK
        varchar(100) nome
    }

    Palavra_Chave {
        int idPalavraChave PK
        varchar(500) descricao
    }

    temaPlvrCh {
        int fk_Tema_idTema FK
        int fk_Palavra_Chave_idPalavraChave FK
    }

    %% --------------------- EDITORA -----------------------
    Editora {
        int idEditora PK
        varchar(100) nome
    }

    %% --------------------- PUBLICAÇÃO -----------------------
    Publicacao {
        int fk_Publicacao_idEditora FK
        int fk_Producao_idProducao FK
        varchar(8) ISSN
        numeric(5) fatorImpacto
    }

    %% --------------------- PROJETO DE PESQUISA -----------------------
    Projeto_de_Pesquisa {
        int idPP PK
        varchar(100) titulo
        varchar(500) descricao
    }

    financiamento {
        int fk_Financiador_idFinanciador FK
        int fk_Projeto_de_Pesquisa_idPP FK
        timestamp data
        integer valor
    }

    Financiador {
        int idFinanciador PK
        int tipo
        varchar(100) nome
    }

    %% --------------------- PRODUÇÃO -----------------------
    Producao {
        int idProducao PK
        int tipo
        varchar(1000) resumo
        int ano
        BYTEA arquivo
        varchar(100) titulo
        int fk_Projeto_de_Pesquisa_idPP FK
    }

    producaoTema {
        int fk_Tema_idTema FK
        int fk_Producao_idProducao FK
    }

    Referencia {
        int fk_Producao_idProducao FK
        int fk_Producao_idProducao_ FK
    }

    producaoPessoa {
        int fk_Pessoa_idPessoa FK
        int fk_Producao_idProducao FK
        int tipo
    }

    %% --------------------- PESSOA -----------------------
    Pessoa {
        int idPessoa PK
        varchar(100) nome
        varchar(11) CPF
        varchar(100) email
    }

    pessoaCurso {
        int fk_Pessoa_idPessoa FK
        int fk_Curso_idCurso FK
    }

    Curso {
        int idCurso PK
        varchar(100) nome
        int nivel
        int fk_Departamento_idDepartamento FK
    }

    Departamento {
        int idDepartamento PK
        varchar(100) nome
        int fk_Instituicao_idInstituicao FK
    }

    Instituicao {
        int idInstituicao PK
        varchar(100) nome
        varchar(100) endereco
    }

    %% --------------------- RELACIONAMENTOS -----------------------

    Tema ||--o{ temaPlvrCh : contem
    Palavra_Chave ||--o{ temaPlvrCh : contem

    Editora ||--o{ Publicacao : publica
    Producao ||--o{ Publicacao : referida_em

    Projeto_de_Pesquisa ||--o{ Producao : produz
    Financiador ||--o{ financiamento : financia
    Projeto_de_Pesquisa ||--o{ financiamento : recebe

    Producao ||--o{ producaoTema : possui
    Tema ||--o{ producaoTema : classificado_por

    Producao ||--o{ producaoPessoa : autoria
    Pessoa ||--o{ producaoPessoa : autor

    Producao ||--o{ Referencia : referencia
    Producao ||--o{ Referencia : referenciado_por

    Pessoa ||--o{ pessoaCurso : matriculado
    Curso ||--o{ pessoaCurso : cursado

    Curso ||--o{ Departamento : pertence
    Departamento ||--o{ Instituicao : integra
```

---

[Requisitos completos do trabalho (PDF)](assets/DEC7129-Trabalho-Final.pdf)
