from fastapi import FastAPI
from Agent.models import ProcessoJudicial, DecisaoProcesso
from Agent.agent_processes import VerificadorProcessos

app = FastAPI(title="Verificador de Processos Judiciais")
verificador = VerificadorProcessos()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/verificar", response_model=DecisaoProcesso)
def verificar_processo(processo: ProcessoJudicial):
    return verificador.verificar_processo(processo)
