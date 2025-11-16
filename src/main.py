# Importação de bibliotecas
import psycopg2
from psycopg2 import errors
import pandas as pd
from pathlib import Path
import sqlparse
from components.text_to_sql_pipeline import TextToSQLPipeline

# Estabelece a conexão com o banco de dados
def connectionSQL():
    try:
        cnx = psycopg2.connect(
            host='localhost',
            port='5432',
            database='testesDB',
            user='postgres',
            password='master'
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
    print("1. Criar Tabelas (Pronto) \n2. Carregar Tabelas (Pronto) \n3. Atualizar Tabelas (Pronto) \n4. Consultar Tabelas (Pronto) \n5. Deletar Tabelas (Pronto) \n6. CRUD \n7. Inserção \n8. Atualização \n9. Exclusão \n10. Consulta \n11. Consulta em Linguagem Natural \n0. Sair")
    opcao = int(input("Opção: "))
    while (opcao > 11 or opcao < 0):
            opcao = int(input("Selecione uma opção válida: "))
    return opcao

# Executa o comando (DDL) conforme o caminho do arquivo sql
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
        print(e.pgerror)
        print("-------------------------------------------")
        # 'raise' faz com que a função que chamou executarSQL também receba a exceção e não continue a execução normalmente
        raise 
    finally:
        cursor.close()

# Executa manipulações (DML) conforme o caminho do arquivo sql
def consultarSQL(connect, sqlCaminho):
    sql = Path(sqlCaminho).read_text(encoding="utf-8")
    
    try:
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.commit()

        try:
            resultado = cursor.fetchall()
            return resultado
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

# Realiza consulta pré-definida
def consultarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "queries.sql"
    resultado = consultarSQL(connect, sqlCaminho)

    # Imprime cada linha da consulta
    for linha in resultado:
        print(linha)
        
# Deleta todas as tabelas do banco
def deletarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "dropCascade.sql"
    executarSQL(connect, sqlCaminho)
    print("Esquema deletado com sucesso!\n")

def mostrarTabelas(connect):
    cursor = connect.cursor()
    # Listar todas as tabelas no schema public
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = [row[0] for row in cursor.fetchall()]

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

        # Imprima o resultado
        print(f"{tableName}: {columnNames}")
    cursor.close()

# Coloca o código SQL dentro do arquivo para chamar a função de DML
def varSQL(connect, sql):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "variable.sql"
    sqlCaminho.write_text(sql)
    resultado = consultarSQL(connect, sqlCaminho)

    try:
        for linha in resultado:
            print(linha)
    except:
        print("Ação executada com sucesso.")

def atualizar(connect):
    mostrarTabelas(connect)
    
    tableName = input(str("\nSelecione uma tabela para atualizar: ")).upper()
    select = "select * from " + tableName
    varSQL(connect, select)
            
    atb = input("Digite o atributo a ser alterado: ")
    valor = input("Digite o valor a ser atribuído: ")
    if isinstance(valor, str): # Testa se é string
        valor = f"'{valor}'"
    col = input("Digite o nome da coluna da chave primária: ")
    id = input("Digite o valor numérico do campo da chave primária: ")
    query = ['UPDATE ', tableName, ' SET ', atb, ' = ', valor, ' WHERE ', col, ' = ', id]
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
                deletarTabelas(conn)
            case 7:
                break
            case 8:
                atualizar(conn)
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
