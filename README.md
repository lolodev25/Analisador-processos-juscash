# Verificador de Processos Judiciais

Sistema automatizado de análise de processos judiciais utilizando inteligência artificial (LLM) para validar conformidade com políticas de compra de crédito.

## Sobre o Projeto

A aplicação analisa processos judiciais e retorna uma decisão estruturada (aprovado, rejeitado ou incompleto) com justificativa e referências às políticas aplicadas. Utiliza Google Gemini como LLM para análise inteligente dos dados.

## Tecnologias

- Python 3.12
- FastAPI - API REST
- Streamlit - Interface web
- Pydantic - Validação de dados
- LangChain - Integração com LLM
- Google Gemini 2.5 Flash - Modelo de IA
- Docker - Containerização

## Estrutura do Projeto

```
teste_jus/
├── Agent/
│   ├── agent_processes.py    # Lógica de verificação com LLM
│   ├── models.py             # Modelos Pydantic
│   └── policy.py             # Definição de políticas
├── main.py                   # API FastAPI
├── app.py                    # Interface Streamlit
├── dados.json                # Dados de exemplo
├── requirements.txt          # Dependências Python
├── Dockerfile                # Configuração Docker
└── README.md                 # Este arquivo
```

## Instalação Local

### Pré-requisitos

- Python 3.12+
- pip ou conda
- Chave da API Google Gemini

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/lolodev25/Analisador-processos-juscash.git
cd Analisador-processos-juscash
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a variável de ambiente:
```bash
# Crie um arquivo .env na raiz do projeto
echo "GOOGLE_API_KEY=sua_chave_api_aqui" > .env
```

5. Inicie a API (Terminal 1):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. Inicie a interface (Terminal 2):
```bash
streamlit run app.py
```

Acesse:
- API: http://localhost:8000
- Documentação OpenAPI: http://localhost:8000/docs
- Interface: http://localhost:8501

## Docker

### Build da imagem

```bash
docker build -t verificador-processos .
```

### Executar container

```bash
docker run -p 8000:8000 -p 8501:8501 -e GOOGLE_API_KEY=sua_chave_api verificador-processos
```

Acesse:
- API: http://localhost:8000
- Interface: http://localhost:8501

## Políticas de Negócio

O sistema valida os seguintes critérios:

- **POL-1:** Processos transitados em julgado em fase de execução
- **POL-2:** Valor de condenação informado (obrigatório)
- **POL-3:** Valor mínimo de R$ 1.000,00
- **POL-4:** Sem condenações na esfera trabalhista
- **POL-5:** Sem óbito do autor sem habilitação no inventário
- **POL-6:** Sem substabelecimento sem reserva de poderes
- **POL-7:** Informar honorários quando existirem
- **POL-8:** Documentos essenciais obrigatórios

## API Endpoints

### Health Check

```
GET /health

Resposta:
{
  "status": "ok"
}
```

### Verificar Processo

```
POST /verificar

Body:
{
  "numeroProcesso": "0004587-00.2021.4.05.8100",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "19ª VARA FEDERAL - SOBRAL/CE",
  "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
  "valorCausa": 67592,
  "assunto": "Rural (Art. 48/51)",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF5",
  "esfera": "Federal",
  "valorCondenacao": 67592,
  "documentos": { ... },
  "honorarios": { ... }
}

Resposta:
{
  "decision": "approved",
  "rationale": "Processo atende aos critérios de elegibilidade",
  "citacoes": ["POL-1", "POL-2", "POL-7"]
}
```

## Decisões Possíveis

- **approved:** Processo atende a todos os critérios de elegibilidade
- **rejected:** Processo viola uma ou mais políticas
- **incomplete:** Faltam documentos ou informações essenciais

## Exemplo de Uso

### Via Interface

1. Acesse http://localhost:8501
2. Preencha os dados do processo
3. Clique em "Analisar Processo"
4. Visualize o resultado com justificativa e políticas aplicadas

### Via API (curl)

```bash
curl -X POST "http://localhost:8000/verificar" \
  -H "Content-Type: application/json" \
  -d '{
    "numeroProcesso": "0004587-00.2021.4.05.8100",
    "classe": "Cumprimento de Sentença contra a Fazenda Pública",
    "orgaoJulgador": "19ª VARA FEDERAL - SOBRAL/CE",
    "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
    "valorCausa": 67592,
    "assunto": "Rural (Art. 48/51)",
    "segredoJustica": false,
    "justicaGratuita": true,
    "siglaTribunal": "TRF5",
    "esfera": "Federal",
    "valorCondenacao": 67592,
    "documentos": {},
    "honorarios": {}
  }'
```

## Tratamento de Erros

A aplicação retorna:

- **422 Unprocessable Entity:** Dados inválidos ou incompletos
- **500 Internal Server Error:** Erro na análise do LLM
- **Resultado "incomplete":** Quando faltam documentos essenciais

## Desenvolvimento

### Adicionar nova política

1. Edite `Agent/policy.py`
2. Adicione a política no dicionário `POLITICAS`
3. A política será automaticamente considerada na análise

### Estrutura de dados

Os modelos Pydantic definem o contrato de dados:
- `ProcessoJudicial`: Entrada
- `DecisaoProcesso`: Saída
