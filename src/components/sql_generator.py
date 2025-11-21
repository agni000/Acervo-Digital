import os
from openai import OpenAI
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
            max_tokens=1000,
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

    
    def generate_pdf_answer(self, question: str, pdf_content: str) -> str:
        """
        Gera uma resposta baseada no conteúdo extraído de um PDF.
        """
        # Truncar conteúdo se for muito grande (limite de segurança simples)
        #max_chars = 20000 
        content_sample = pdf_content#[:max_chars]

        prompt = f"""
        Você é um assistente acadêmico inteligente. O usuário fez uma pergunta sobre um documento específico.
        
        CONTEÚDO DO DOCUMENTO (Extraído do PDF):
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        {content_sample}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        PERGUNTA DO USUÁRIO:
        "{question}"
        
        INSTRUÇÕES CRÍTICAS:
        1. O usuário está fazendo perguntas sobre o documento acima.
        2. Se a pergunta for genérica (ex: "abra o arquivo", "leia o pdf", "o que tem na linha X"), ignore a referência à "linha" ou "tabela" e **FAÇA UM RESUMO DETALHADO** do conteúdo do texto.
        3. Se a pergunta for específica (ex: "qual a metodologia?", "quem é o autor?"), responda baseando-se no texto.
        """
        
        if self.model_type == "gpt":
            return self.generate_gpt(prompt)
        else:
            return self.generate_gemini(prompt)
        
    def generate(self, question: str, schema_description: dict) -> str:
        schema_text = schema_description["schema"]
        db_state_text = schema_description["state"]

        prompt = f"""Você é um assistente de IA integrado a um banco de dados PostgreSQL.

                VOCÊ TEM DUAS HABILIDADES:

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                MODO 1: TEXT-TO-SQL (Consultas ao Banco de Dados)
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                Quando o usuário pede para:
                - Listar, buscar, mostrar, encontrar dados
                - Contar, somar, calcular estatísticas
                - Inserir, atualizar, deletar registros
                - Fazer qualquer operação no banco de dados

                CASO ESPECIAL (LEITURA DE PDFS):
                Se o usuário perguntar sobre o CONTEÚDO de um artigo, tese ou documento (ex: "Resuma o artigo X", "O que diz o TCC Y?"):
                1. Você DEVE gerar um SQL que selecione a coluna 'arquivo' (bytea) da tabela PRODUCAO.
                2. Exemplo: SELECT arquivo FROM PRODUCAO WHERE titulo ILIKE '%titulo%';
                3. Faça uma análise do arquivo com base no pedido do usuário.

                VOCÊ DEVE RETORNAR **APENAS** A QUERY SQL da seguinte forma:
                - Sem explicações antes ou depois
                - Sem Markdown (```sql ou ```)
                - Sem texto adicional
                - Ao gerar SQL relacionado à tabela PRODUCAO, inclua a coluna 'arquivo' somente no caso do usuário pedir acesso ao BLOB/Binário

                Exemplos de perguntas que precisam SQL:
                - "Quantos usuários temos?"
                - "Liste os produtos mais vendidos"
                - "Mostre pedidos do último mês"
                - "Insira um novo cliente chamado João"
                - "Atualize o preço do produto X"

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                MODO 2: LINGUAGEM NATURAL (Conversação)
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                Quando o usuário pede:
                - Explicações conceituais
                - Ajuda sobre como usar o sistema
                - Perguntas gerais (não relacionadas aos dados)
                - Interpretações ou análises textuais

                VOCÊ DEVE RESPONDER em linguagem natural, de forma clara e amigável.

                Exemplos de perguntas que precisam resposta em texto:
                - "Como funciona este sistema?"
                - "O que é um banco de dados relacional?"
                - "Explique o que são chaves primárias"
                - "Olá, tudo bem?"
                - "Me ajude a entender estas tabelas"

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ESQUEMA DO BANCO DE DADOS:
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                {schema_text}

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ESTADO ATUAL DO BANCO (respeite as constraints):
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                {db_state_text}

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                PERGUNTA DO USUÁRIO:
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                "{question}"

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                DECISÃO:
                1. Se precisa consultar o banco → retorne APENAS o SQL
                2. Se é pergunta geral → responda em linguagem natural

                LEMBRE-SE:
                - SQL deve ser limpo, sem markdown ou explicações
                - Respostas naturais devem ser claras e úteis
                - Use português brasileiro em respostas de texto
                """

        if (self.model_type == "gpt"):
            response = self.generate_gpt(prompt)
        else:
            response = self.generate_gemini(prompt)

        return response