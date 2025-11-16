#from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import pandas as pd
from .query_parser import QueryParser
from .sql_generator import SQLGenerator

class TextToSQLPipeline:
    def __init__(self, connection):
        load_dotenv()   
        type = os.getenv("gpt")
        self.parser = QueryParser()
        if (type == "gpt"):
            model = os.getenv("GPT_MODEL")
            api_key = os.getenv("GPT_KEY")
        else:
            model = os.getenv("GEMINI_MODEL")
            api_key = os.getenv("GEMINI_KEY")

        self.sql_generator = SQLGenerator(type, model, api_key)
        self.db_executor = connection; 

    def run_query(self, sql: str):
        cursor = self.db_executor.cursor()

        # Se for SELECT → usar pandas
        if sql.strip().lower().startswith("select"):
            return pd.read_sql_query(sql, self.db_executor)

        # Se for INSERT / UPDATE / DELETE → usar cursor.execute()
        try:
            cursor.execute(sql)
            self.db_executor.commit()

            # Tenta pegar dados (caso seja RETURNING)
            try:
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(rows, columns=columns)
            except:
                # Sem retorno → confirmação
                return pd.DataFrame({"status": ["OK"]})

        except Exception as e:
                self.db_executor.rollback()
                return pd.DataFrame({"error": [str(e)]})

    # def run(self, question: str, schema_description: str) -> pd.DataFrame:
    #     parsed_question = self.parser.parse(question)
    #     sql_query = self.sql_generator.generate(parsed_question, schema_description)
    #     print(f"Generated SQL:\n{sql_query}")
    #     return self.run_query(sql_query)
    
    def extract_database_state(self):
        cursor = self.db_executor.cursor()

        state = {}

        # listar todas as tabelas no schema public
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            state[table] = {}

            # pegar chave primária
            cursor.execute(f"""
                SELECT a.attname
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid
                AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = '{table}'::regclass
                AND i.indisprimary;
            """)
            pk_rows = cursor.fetchall()
            if pk_rows:
                pk = pk_rows[0][0]
                state[table]["primary_key"] = pk

                cursor.execute(f"SELECT {pk} FROM {table};")
                state[table]["existing_primary_keys"] = [
                    row[0] for row in cursor.fetchall()
                ]

            # encontrar colunas unique
            cursor.execute(f"""
                SELECT a.attname
                FROM pg_constraint c
                JOIN pg_attribute a 
                ON a.attrelid = c.conrelid 
                AND a.attnum = ANY(c.conkey)
                WHERE c.conrelid = '{table}'::regclass
                AND c.contype = 'u';
            """)
            unique_cols = [u[0] for u in cursor.fetchall()]

            if unique_cols:
                state[table]["unique_columns"] = {}
                for col in unique_cols:
                    cursor.execute(f"SELECT {col} FROM {table};")
                    state[table]["unique_columns"][col] = [
                        row[0] for row in cursor.fetchall()
                    ]

        return state    
    
    def run(self, question: str, schema_description: str) -> pd.DataFrame:
        # 1. Extrair estado atual do DB (PK, UNIQUE, FK)
        db_state = self.extract_database_state()

        # 2. Injetar no prompt
        enhanced_schema = {
            "schema": schema_description,
            "state": db_state
        }

        parsed_question = self.parser.parse(question)

        sql_query = self.sql_generator.generate(
            parsed_question,
            enhanced_schema
        )

        print(f"Generated SQL:\n{sql_query}")
        return self.run_query(sql_query)