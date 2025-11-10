# Importação de bibliotecas
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
import pandas as pd

# Estabelece a conexão com o banco de dados

def connectionSQL():

    try:
        conn = mysql.connector.connect(user = 'root', password = 'master',
                                host = 'localhost',
                                database = 'acervo',
                                autocommit = False)
        print("Conexão com o banco de dados estabelecida.")
        return conn
    except mysql.connector.Error as error:
        print("Não foi possível realizar a conexão com o banco de dados {}.".format(error))
        quit()

def menu():

    print("-----------------------\n Menu (Acervo Digital) \n-----------------------")
    print("1. Criar Tabelas (Pronto) \n2. Carregar Tabelas (Pronto) \n3. Atualizar Tabelas (Pronto) \n4. Deletar Tabelas (Pronto) \n5. Consultar Tabelas (Pronto) \n6. CRUD \n7. Inserção \n8. Atualização \n9. Exclusão \n10. Consulta \n11. Deleção Total \n0. Sair")
    opcao = int(input("Opção: "))
    return opcao

def criarTabelas():

    txt = "inserirTabelas.txt"

    try:
        with open(txt, "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{txt}' não foi encontrado.")
    except Exception as e:
        print(f"Um erro ocorreu: {e}")

def main():

    conn = connectionSQL()

    opcao = 1

    while (opcao != 0):

        opcao = menu()

        match opcao:

            case 1:
                criarTabelas()
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
                if conn.is_connected():
                    print("Conexão encerrada.")
                    conn.close()

if __name__ == "__main__":
    main()
    

