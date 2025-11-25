from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Documento(BaseModel):
    id: str
    dataHoraJuntada: datetime
    nome: str
    texto: str

class Movimento(BaseModel):
    dataHora: datetime
    descricao: str

class Honorarios(BaseModel):
    contratuais: Optional[float] = None
    periciais: Optional[float] = None
    sucumbenciais: Optional[float] = None

class DocumentosEstruturados(BaseModel):
    sentencaMerito: Optional[Dict[str, Any]] = None
    transitoJulgado: Optional[Dict[str, Any]] = None
    cumprimentoDefinitivoIniciado: Optional[Dict[str, Any]] = None
    calculosApresentados: Optional[Dict[str, Any]] = None
    intimacaoEntePublico: Optional[Dict[str, Any]] = None
    prazoImpugnacaoAberto: Optional[Dict[str, Any]] = None
    requisitorio: Optional[Dict[str, Any]] = None
    cessaoPreviaPagamento: Optional[Dict[str, Any]] = None
    substabelecimentoSemReserva: Optional[Dict[str, Any]] = None
    obitoAutor: Optional[Dict[str, Any]] = None

class ProcessoJudicial(BaseModel):
    numeroProcesso: str
    classe: str
    orgaoJulgador: str
    ultimaDistribuicao: datetime
    valorCausa: Optional[float] = None
    assunto: str
    segredoJustica: bool
    justicaGratuita: bool
    siglaTribunal: str
    esfera: str
    valorCondenacao: Optional[float] = None
    documentos: Optional[DocumentosEstruturados] = None
    movimentos: Optional[List[Movimento]] = None
    honorarios: Optional[Honorarios] = None

class DecisaoProcesso(BaseModel):
    decision: str
    rationale: str
    citacoes: List[str]
