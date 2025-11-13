# Importação de bibliotecas
import psycopg2
from psycopg2 import errors
import pandas as pd
from pathlib import Path

# Estabelece a conexão com o banco de dados
def connectionSQL():
    try:
        cnx = psycopg2.connect(
            host='localhost',
            port='5432',
            database='temQueMudar',
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

def menu():

    print("-----------------------\n Menu (Acervo Digital) \n-----------------------")
    print("1. Criar Tabelas (Pronto) \n2. Carregar Tabelas (Pronto) \n3. Atualizar Tabelas (Pronto) \n4. Deletar Tabelas (Pronto) \n5. Consultar Tabelas (Pronto) \n6. CRUD \n7. Inserção \n8. Atualização \n9. Exclusão \n10. Consulta \n11. Deleção Total \n0. Sair")
    opcao = int(input("Opção: "))
    while (opcao > 11 or opcao < 0):
            opcao = int(input("Selecione uma opção válida: "))
    return opcao

def criarTabelas(connect):
    sqlCaminho = Path(__file__).parent.parent / "sql" / "schema.sql"

    # Lê o script SQL completo
    with open(sqlCaminho, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    try:
        cursor = connect.cursor()

        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt + ';') 
        connect.commit()
        print("Script executado com sucesso!")

    except psycopg2.Error as e:
        connect.rollback()
        print("-------------------------------------------")
        print("ERRO AO EXECUTAR O SCRIPT!")
        print("O banco de dados fez um ROLLBACK automático.")
        print(f"Mensagem do PostgreSQL: {e.pgerror}")
        print("-------------------------------------------")

    finally:
        cursor.close()
        connect.close()

def main():
    conn = connectionSQL()
    opcao = 1

    while (opcao != 0):

        opcao = menu()

        match opcao:

            case 1:
                criarTabelas(conn)
            case 2:
                break
            case 3:
                break
            case 4:
                break
            case 5:
                break
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
                break
            case 0:
                if conn.closed == 0:
                    print("Conexão encerrada.")
                    conn.close()
                    
if __name__ == "__main__":
    main()
    

