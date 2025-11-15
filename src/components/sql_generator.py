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

    def generate(self, question: str, schema_description: dict) -> str:
        schema_text = schema_description["schema"]
        db_state_text = schema_description["state"]

        prompt = f'''
            You are a Text-to-SQL generator. 
            Here is the schema:
            {schema_text}

            Here is the CURRENT DATABASE STATE (important! do not violate constraints):
            {db_state_text}

            Now write SQL to answer:
            "{question}"

            Rules:
            - Return ONLY a valid SQL string.
            - DO NOT repeat primary keys.
            - DO NOT repeat UNIQUE values.
            - If generating INSERT statements, ensure all constraints are respected.
            - No formatting, no markdown.
            - No trailing semicolon.
        '''

        if (self.model_type == "gpt"):
            response = self.generate_gpt(prompt)
        else:
            response = self.generate_gemini(prompt)

        return response
