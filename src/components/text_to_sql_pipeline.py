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

    def run_query(self, sql):
        df = pd.read_sql_query(sql, self.db_executor)
        return df

    def run(self, question: str, schema_description: str) -> pd.DataFrame:
        parsed_question = self.parser.parse(question)
        sql_query = self.sql_generator.generate(parsed_question, schema_description)
        print(f"Generated SQL:\n{sql_query}")
        return self.run_query(sql_query)