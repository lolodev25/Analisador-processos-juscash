import json
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Agent.models import ProcessoJudicial, DecisaoProcesso
from Agent.policy import get_politicas_texto
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

class VerificadorProcessos:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1,
            google_api_key=api_key
        )
        self.prompt_template = PromptTemplate(
            input_variables=["processo", "politicas"],
            template="""Você é um analisador de processos judiciais. Analise o processo abaixo conforme as políticas da empresa.

POLÍTICAS:
{politicas}

PROCESSO:
{processo}

INSTRUÇÕES:
1. Verifique cada política contra os dados do processo
2. Retorne APENAS um JSON válido (sem markdown, sem explicações extras)
3. Os campos são:
   - decision: "approved", "rejected" ou "incomplete"
   - rationale: justificativa clara e concisa
   - citacoes: array com IDs das políticas relevantes

IMPORTANTE: Retorne SOMENTE o JSON, começando com {{ e terminando com }}

JSON:"""
        )
    
    def verificar_processo(self, processo: ProcessoJudicial) -> DecisaoProcesso:
        processo_json = processo.model_dump_json(indent=2)
        politicas_texto = get_politicas_texto()
        
        prompt = self.prompt_template.format(
            processo=processo_json,
            politicas=politicas_texto
        )
        
        response = self.llm.invoke(prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        try:
            # Limpar resposta de markdown ou caracteres extras
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1]
                if cleaned_response.startswith("json"):
                    cleaned_response = cleaned_response[4:]
            cleaned_response = cleaned_response.strip()
            
            resultado = json.loads(cleaned_response)
            return DecisaoProcesso(**resultado)
        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON: {e}")
            print(f"Resposta recebida: {response_text}")
            return DecisaoProcesso(
                decision="incomplete",
                rationale="Erro ao processar resposta do LLM - JSON inválido",
                citacoes=["POL-8"]
            )
        except Exception as e:
            print(f"Erro geral: {e}")
            return DecisaoProcesso(
                decision="incomplete",
                rationale="Erro ao analisar o processo",
                citacoes=["POL-8"]
            )
