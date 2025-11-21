# Importação de bibliotecas
import os
import psycopg2
from psycopg2 import errors
import pandas as pd
from pathlib import Path
import sqlparse
from components.text_to_sql_pipeline import TextToSQLPipeline
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# Estabelece a conexão com o banco de dados
def connectionSQL():
    load_dotenv()  
    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    
    try:
        cnx = psycopg2.connect(
            host=host,
            port='5432',
            database=database,
            user=user,
            password=password
        )
        print("Conexão com o PostgreSQL estabelecida com sucesso.")

        cursor = cnx.cursor()

        # Recuperar a versão do servidor PostgreSQL
        cursor.execute("SELECT version();")
        db_info = cursor.fetchone()
        print("Versão do servidor PostgreSQL:", db_info[0])

        # Verificar o banco de dados atual
        cursor.execute("SELECT current_database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados:", linha[0])

        cursor.close()
        return cnx
    
    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)
        return None

# Implementação do menu
def menu():
    print("-----------------------\n Menu (Acervo Digital) \n-----------------------")
    print("1. Criar Tabelas (Pronto) \n2. Carregar Tabelas (Pronto) \n3. Atualizar Tabelas (Pronto) \n4. Consultar Tabelas (Pronto) \n5. Deletar Tabelas (Pronto) \n6. CRUD \n7. Inserção \n8. Atualização \n9. Exclusão \n10. Consulta em Linguagem Natural \n0. Sair")
    opcao = int(input("Opção: "))
    while (opcao > 10 or opcao < 0):
            opcao = int(input("Selecione uma opção válida: "))
    return opcao

# Executa o comando (DDL) conforme o caminho do arquivo sql
def executarSQL(connect, sqlCaminho):
    # Lê o script SQL completo
    sql = Path(sqlCaminho).read_text(encoding="utf-8")
    
    try:
        cursor = connect.cursor()
        # Divide o sql em declarações separadas para execução e commit.
        for stmt in sqlparse.split(sql):
            if stmt.strip():
                cursor.execute(stmt)
        connect.commit()
    except psycopg2.Error as e:
        connect.rollback()
        print("-------------------------------------------")
        print("ERRO AO EXECUTAR O SCRIPT!")
        print("O banco de dados fez um ROLLBACK automático.")
        print(e.pgerror)
        print("-------------------------------------------")
        # 'raise' faz com que a função que chamou executarSQL também receba a exceção e não continue a execução normalmente
        raise 
    finally:
        cursor.close()

# Executa manipulações (DML) conforme o caminho do arquivo sql
def consultarSQL(connect, sqlCaminho):
    # Lê o script SQL completo
    sql = Path(sqlCaminho).read_text(encoding="utf-8")
    
    try:
        cursor = connect.cursor()
        # Divide o sql em declarações separadas para execução e commit
        for stmt in sqlparse.split(sql):
            if stmt.strip():
                cursor.execute(stmt)
        connect.commit()

        # Acessa todas as linhas e colunas da do resultado e retorna um dicionário 
        try:
            linhas = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            res = {'linhas': linhas, 'colunas': colunas}
            return res
        except: 
            return None
    
    except psycopg2.Error as e:
        print("-------------------------------------------")
        print("ERRO AO EXECUTAR O SCRIPT!")
        print(e.pgerror)
        print("-------------------------------------------")
        raise
    finally:
        cursor.close()
    
# Carrega o esquema completo no banco
def criarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "schema.sql"
    executarSQL(connect, sqlCaminho)
    print("\nEsquema criado com sucesso!")

# Carrega as tabelas com valores pré-definidos
def carregarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "insert.sql"
    executarSQL(connect, sqlCaminho)
    print("\nValores carregados no banco!")

# Atualiza algumas tabelas com valores pré-definidos
def atualizarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "update.sql"
    executarSQL(connect, sqlCaminho)
    print("\nValores atualizados no banco!")

# Realiza consulta pré-definida
def consultarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "queries.sql"
    sql = Path(sqlCaminho).read_text(encoding="utf-8")
    consults = {}

    # Splita a query e itera sobre as consultas dentro do arquivo carregado atribuindo as declarações para consults
    for i, stmt in enumerate(sqlparse.split(sql)):
        if stmt.strip():
            consults[i] = stmt
            print(f"\n{i}. {consults[i]}")

    opcao = int(input("\nSelecione a consulta que deseja executar: "))
    resultado = varSQL(connect, consults[opcao])

    try:
        # Cria um data frame conforme a consulta e plota um gráfico com base no resultado
        df = pd.DataFrame(resultado['linhas'], columns=resultado['colunas'])
        sns.barplot(data=df, x=resultado['colunas'][0], y=resultado['colunas'][1])
        plt.show()
    except Exception as e:
        print("-------------------------------------------")
        print(e)
        print("-------------------------------------------")
        raise
    finally:
        print(df)
        
# Deleta todas as tabelas do banco
def deletarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "dropCascade.sql"
    executarSQL(connect, sqlCaminho)
    print("\nEsquema deletado com sucesso!")

# Retorna um dicionário com as tabelas e suas respectivas colunas
def iterarTabelas(connect):

    cursor = connect.cursor()
    # Listar todas as tabelas no schema public
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = [row[0] for row in cursor.fetchall()]

    res = {}

    for tableName in tables:
        # Listar todas as colunas em cada tabela
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            ORDER BY ordinal_position;
        """, (tableName,))

        columnNames = [row[0] for row in cursor.fetchall()]
        res[tableName] = columnNames

    cursor.close()

    return res

# Mostra todas as tabelas
def mostrarTabelas(connect):
    
    res = iterarTabelas(connect)

    for tabela, colunas in res.items():
        print(f"{tabela}: {colunas}")
    
# Coloca o código SQL dentro do arquivo para chamar a função de DML
def varSQL(connect, sql):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "variable.sql"
    sqlCaminho.write_text(sql)
    resultado = consultarSQL(connect, sqlCaminho)

    return resultado

# Inserção manual
def inserir(connect):
    mostrarTabelas(connect)

    # Seleciona a tabela a receber o dado
    tableName = input(str("\nSelecione uma tabela para inserir o novo dado: ")).upper()
    select = "select * from " + tableName
    resultado = varSQL(connect, select)

    # Printa o estado atual da tabela
    df = pd.DataFrame(resultado['linhas'], columns=resultado['colunas'])
    print(df)

    sql = "INSERT INTO " + tableName + " values ("

    res = iterarTabelas(connect)

    for tabela, colunas in res.items():
        if str(tabela).upper() == tableName:
            for i, nomeColuna in enumerate(colunas):
                atb = input(f"\nDigite o dado a ser inserido em {nomeColuna}: ")
                atb = f"'{atb}'"

                if(i == (len(colunas) - 1)):
                    sql = sql + atb + ");"
                else:
                    sql = sql + atb + ", "

    varSQL(connect, sql)

# Atualização manual
def atualizar(connect):
    mostrarTabelas(connect)
    
    # Seleciona a tabela a ser atualizada
    tableName = input(str("\nSelecione uma tabela para atualizar: ")).upper()
    select = "select * from " + tableName
    resultado = varSQL(connect, select)

    # Printa o estado atual da tabela
    df = pd.DataFrame(resultado['linhas'], columns=resultado['colunas'])
    print(df)

    res = iterarTabelas(connect)

    for tabela, colunas in res.items():
        if str(tabela).upper() == tableName:
            col = colunas[0]
            
    atb = input("Digite o atributo a ser alterado: ")
    valor = input("Digite o valor a ser atribuído: ")
    valor = f"'{valor}'"
    id = input("Digite o valor numérico do campo da chave primária: ")
    query = ['UPDATE ', tableName, ' SET ', atb, ' = ', valor, ' WHERE ', col, ' = ', id]
    sql = ''.join(query)
    varSQL(connect, sql)

# Exclusão manual
def excluir(connect):
    mostrarTabelas(connect)
    
    # Seleciona a tabela a ser excluida
    tableName = input(str("\nSelecione uma tabela para deletar um dado: ")).upper()
    select = "select * from " + tableName
    resultado = varSQL(connect, select)
    
    # Printa o estado atual da tabela    
    df = pd.DataFrame(resultado['linhas'], columns=resultado['colunas'])
    print(df)

    res = iterarTabelas(connect)

    for tabela, colunas in res.items():
        if str(tabela).upper() == tableName:
            col = colunas[0]
            
    id = input("\nDigite o valor numérico do campo da chave primária: ")
    query = ['DELETE FROM ', tableName, ' WHERE ', col, ' = ', id]
    sql = ''.join(query)
    varSQL(connect, sql)

def executarPipeline(connect, descricao):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "schema.sql"
    schema = Path(sqlCaminho).read_text(encoding="utf-8")
    
    # Instancia a pipeline e executa
    pipeline = TextToSQLPipeline(connect)
    result_df = pipeline.run(descricao, schema)

    # Mostra os resultados
    print("\nResultado da consulta:")
    print(result_df)

def main():
    conn = connectionSQL()
    opcao = 1

    while (opcao != 0):

        try:
            opcao = menu()

            match opcao:

                case 1:
                    criarTabelas(conn)
                case 2:
                    carregarTabelas(conn)
                case 3:
                    atualizarTabelas(conn)
                case 4:
                    consultarTabelas(conn)
                case 5:
                    deletarTabelas(conn)
                case 6:
                    deletarTabelas(conn)
                    criarTabelas(conn)
                    carregarTabelas(conn)
                    atualizarTabelas(conn)
                    consultarTabelas(conn)
                case 7:
                    inserir(conn)
                case 8:
                    atualizar(conn)
                case 9:
                    excluir(conn)
                case 10:
                    consulta = input("\nDigite a consulta em linguagem natural: ")
                    executarPipeline(conn, consulta)
                case 0:
                    if not conn.closed:
                        print("\nConexão encerrada.")
                        conn.close()

        except Exception as e:
            if not conn.closed:
                conn.rollback()
            print(f"\nUm erro ocorreu: {e}")
                    
if __name__ == "__main__":
    main()
