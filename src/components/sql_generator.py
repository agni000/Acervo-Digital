import os
#pip install --upgrade openai
from openai import OpenAI
#pip install google-genai
from google import genai
from dotenv import load_dotenv

class SQLGenerator:
    def __init__(self, type, model, api_key):
        if (type == "gpt"):
            self.genai_client = OpenAI(api_key=api_key)
        else:
            self.genai_client = genai.Client(api_key=api_key)
        self.model_type = type    
        self.genai_model = model

    def generate_gpt(self, prompt: str) -> str:
        completion = self.genai_client.chat.completions.create(
            model=self.genai_model,
            max_tokens=500,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()

    def generate_gemini(self, prompt: str) -> str:
        response = self.genai_client.models.generate_content(
            model=self.genai_model,
            contents=[
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return response.text.strip()

    def generate(self, question: str, schema_description: str) -> str:
        prompt = f'''Considering the database schema {schema_description}, 
            write an SQL query to answer the query: "{question}". 
            The generated queries must attribute an alias for 
            each column when is not used the column name. 
            In the answer, present only the SQL query without any formatting or line breaks as a string, 
            without the ";" character at the end and without the "\" character'''

        print(self.model_type)
        if (self.model_type == "gpt"):
            response = self.generate_gpt(prompt)
        else:
            response = self.generate_gemini(prompt)

        return response