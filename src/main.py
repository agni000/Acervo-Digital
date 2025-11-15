# Importação de bibliotecas
import psycopg2
from psycopg2 import errors
import pandas as pd
from pathlib import Path
import sqlparse
from components.text_to_sql_pipeline import TextToSQLPipeline

# Estabelece a conexão com o banco de dados.
def connectionSQL():
    try:
        cnx = psycopg2.connect(
            host='localhost',
            port='5432',
            database='testesDB',
            user='postgres',
            password='********'
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

# Implementação do menu. 
def menu():
    print("-----------------------\n Menu (Acervo Digital) \n-----------------------")
    print("1. Criar Tabelas (Pronto) \n2. Carregar Tabelas (Pronto) \n3. Atualizar Tabelas (Pronto) \n4. Consultar Tabelas (Pronto) \n5. Deletar Tabelas (Pronto) \n6. CRUD \n7. Inserção \n8. Atualização \n9. Exclusão \n10. Consulta \n0. Sair")
    opcao = int(input("Opção: "))
    while (opcao > 11 or opcao < 0):
            opcao = int(input("Selecione uma opção válida: "))
    return opcao

# Executa o comando(DDL) conforme o caminho do arquivo sql.
def executarSQL(connect, sqlCaminho):
    # Lê o script SQL completo
    sql = Path(sqlCaminho).read_text(encoding="utf-8")
    
    try:
        cursor = connect.cursor()
        for stmt in sqlparse.split(sql):
            if stmt.strip():
                cursor.execute(stmt)
        connect.commit()
    except psycopg2.Error as e:
        connect.rollback()
        print("-------------------------------------------")
        print("ERRO AO EXECUTAR O SCRIPT!")
        print("O banco de dados fez um ROLLBACK automático.")
        print(f"Mensagem do PostgreSQL: {e.pgerror}")
        print("-------------------------------------------")
        # raise faz com que a função que chamou executarSQL também receba a exceção e não continue a execução normalmente.
        raise 
    finally:
        cursor.close()

# Executa manipulações(DML) conforme o caminho do arquivo sql.
def consultarSQL(connect, sqlCaminho):
    sql = Path(sqlCaminho).read_text(encoding="utf-8")
    
    try:
        cursor = connect.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return resultado
    
    except psycopg2.Error as e:
        print("Erro ao executar SELECT!")
        print(e.pgerror)
        raise
    
    finally:
        cursor.close()
    
# Carrega o esquema completo no banco. 
def criarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "schema.sql"
    executarSQL(connect, sqlCaminho)
    print("Esquema criado com sucesso!\n")

# Carrega as tabelas com valores pré-definidos
def carregarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "insert.sql"
    executarSQL(connect, sqlCaminho)
    print("Valores carregados no banco!\n")

# Atualiza algumas tabelas com valores pré-definidos
def atualizarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "update.sql"
    executarSQL(connect, sqlCaminho)
    print("Valores atualizados no banco!\n")

# Realiza consulta pré-definida. 
def consultarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "queries.sql"
    resultado = consultarSQL(connect, sqlCaminho)

    # Imprime cada linha da consulta
    for linha in resultado:
        print(linha)
        
# Deleta todas as tabelas do banco.
def deletarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "dropCascade.sql"
    executarSQL(connect, sqlCaminho)
    print("Esquema deletado com sucesso!\n")

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
                break
            case 7:
                break
            case 8:
                break
            case 9:
                break
            case 10:
                break
            case 11:
                consulta = input("Digite a consulta em linguagem natural: ")
                executarPipeline(conn, consulta)
            case 0:
                if conn.closed == 0:
                    print("Conexão encerrada.")
                    conn.close()
                    
if __name__ == "__main__":
    main()
    

