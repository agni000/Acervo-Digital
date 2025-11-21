import io
from pypdf import PdfReader

class PDFProcessor:
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        """
        Recebe bytes de um PDF e retorna o texto extraído.
        """
        try:
            # Cria um stream de bytes na memória
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)
            text = []
            
            # Extrai texto de todas as páginas
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text.append(content)
            
            return "\n".join(text)
        except Exception as e:
            return f"Erro ao ler PDF: {str(e)}"