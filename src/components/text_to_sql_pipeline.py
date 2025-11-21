import os
from dotenv import load_dotenv
import pandas as pd
from .query_parser import QueryParser
from .sql_generator import SQLGenerator
from .pdf_processor import PDFProcessor # <--- Importe o novo processador

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
        self.db_executor = connection

    def is_sql_response(self, response: str) -> bool:
        """
        Determina se a resposta do LLM é SQL ou texto natural.
        """
        response_clean = response.strip().upper()
        
        # Remove markdown se presente
        if response_clean.startswith("```SQL"):
            return True
        if response_clean.startswith("```"):
            return True
            
        # Verifica se começa com comandos SQL
        sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"]
        
        return any(response_clean.startswith(keyword) for keyword in sql_keywords)
    
    def should_trigger_pdf_logic(self, question: str) -> bool:
        """
        Retorna True se a pergunta do usuário indica intenção de ler/usar o conteúdo do PDF.
        """
        question_lower = question.lower()

        pdf_keywords = [
            "pdf", "documento", "arquivo", "conteúdo do pdf",
            "ler pdf", "extrair pdf", "ler o arquivo", "ler o documento",
            "texto do pdf", "conteúdo do documento"
        ]

        return any(keyword in question_lower for keyword in pdf_keywords)
    
    def remove_pdf_columns(self, sql: str) -> str:
        """
        Remove colunas de BLOB/PDF de SELECTs, mantendo apenas metadados.
        Só aplica se NÃO houver pedido explícito de leitura de PDF.
        """
        sql_trim = sql.strip()

        # Só altera SELECTs simples
        if not sql_trim.lower().startswith("select"):
            return sql

        # Palavras que indicam colunas BLOB
        pdf_column_names = ["pdf", "arquivo", "documento"]

        # Se SELECT * não alteramos
        if "*" in sql_trim:
            return sql

        # Separar a primeira ocorrência real do FROM
        sql_lower = sql_trim.lower()
        idx = sql_lower.find(" from ")
        if idx == -1:
            return sql  # SELECT inválido

        select_part = sql_trim[7:idx].strip()   # Depois de "SELECT "
        from_part = sql_trim[idx:].strip()      # Inclui "FROM ..."

        # Lista de colunas
        columns = [c.strip() for c in select_part.split(",")]

        # Remover colunas que contenham nomes proibidos
        filtered_cols = [
            c for c in columns
            if not any(keyword in c.lower() for keyword in pdf_column_names)
        ]

        # Evitar SELECT vazio (inválido)
        if not filtered_cols:
            return sql

        # Reconstruir SQL corretamente
        new_sql = "SELECT " + ", ".join(filtered_cols) + " " + from_part
        return new_sql

    def clean_sql(self, sql: str) -> str:
        """
        Remove markdown e formatação extra do SQL.
        """
        sql = sql.strip()
        
        # Remove markdown
        if sql.startswith("```sql"):
            sql = sql[6:]
        elif sql.startswith("```"):
            sql = sql[3:]
            
        if sql.endswith("```"):
            sql = sql[:-3]
            
        # Remove ponto e vírgula final
        sql = sql.strip().rstrip(';')
        
        return sql

    def run_query(self, sql: str):
        """Executa SQL e retorna DataFrame."""
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
                return pd.DataFrame({"status": ["Operação executada com sucesso"]})

        except Exception as e:
            self.db_executor.rollback()
            return pd.DataFrame({"error": [str(e)]})

    def extract_database_state(self):
        """Extrai estado atual do banco (PKs, UNIQUEs, etc.)"""
        cursor = self.db_executor.cursor()
        state = {}

        # Listar todas as tabelas no schema public
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            state[table] = {}

            # Pegar chave primária
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

            # Encontrar colunas unique
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
    
    def run(self, question: str, schema_description: str):
        """
        Executa a pipeline híbrida.
        Retorna:
        - DataFrame: se for consulta SQL
        - str: se for resposta em linguagem natural
        """
        # 1. Extrair estado atual do DB
        db_state = self.extract_database_state()

        # 2. Montar schema enriquecido
        enhanced_schema = {
            "schema": schema_description,
            "state": db_state
        }

        # 3. Parse da pergunta
        parsed_question = self.parser.parse(question)

        # 4. Gerar resposta (SQL ou texto)
        response = self.sql_generator.generate(
            parsed_question,
            enhanced_schema
        )

       # 5. Verificar lógica
        if self.is_sql_response(response):
            sql_clean = self.clean_sql(response)
            
            #Eliminamos a coluna de arquivo bruto, caso não haja a necessidade de leitura de pdfs
            if not self.should_trigger_pdf_logic(question):
                sql_clean = self.remove_pdf_columns(sql_clean)
            
            print(f"[SQL GERADO]:\n{sql_clean}\n")
            
            # Executa a query
            result_df = self.run_query(sql_clean)

            if not self.should_trigger_pdf_logic(question):
                return result_df
            
            if not result_df.empty:
                pdf_bytes = None

                # Procura em TODAS as linhas e colunas qualquer blob/binário
                for idx in result_df.index:
                    for col in result_df.columns:
                        val = result_df.at[idx, col]

                        if isinstance(val, (bytes, memoryview, bytearray)):
                            pdf_bytes = bytes(val) if isinstance(val, memoryview) else bytes(val)
                            break
                    if pdf_bytes is not None:
                        break

                # Se encontrou algum PDF/BLOB
                if pdf_bytes is not None:
                    print(f"[INFO] Acessando arquivo...")

                    # Limite de segurança para evitar PDF gigante quebrar a memória
                    if len(pdf_bytes) > 10 * 1024 * 1024:  # 10 MB
                        return "O PDF é muito grande para ser processado (limite de 10 MB)."

                    # Tenta extrair texto
                    try:
                        pdf_text = PDFProcessor.extract_text_from_bytes(pdf_bytes)
                    except Exception as e:
                        return f"Erro ao processar o PDF: {str(e)}"

                    if not pdf_text.strip():
                        return (
                            "O PDF foi encontrado, mas não consegui extrair texto. "
                            "Provavelmente é um PDF composto somente por imagens."
                        )

                    print("[INFO] Texto extraído do PDF. Avaliando...")

                    # Chama novamente a IA, agora com texto do PDF
                    try:
                        final_answer = self.sql_generator.generate_pdf_answer(question, pdf_text)
                        return final_answer
                    except Exception as e:
                        return f"Erro ao gerar resposta baseada no PDF: {str(e)}"

            # Se não for PDF → retorna DataFrame normal
            return result_df
        else:
            return response