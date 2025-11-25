import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Verificador de Processos Judiciais",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { max-width: 1200px; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; font-weight: 500; }
    .success-box { background-color: #ffffff; padding: 20px; border-radius: 8px; border-left: 5px solid #28a745; }
    .success-box h4 { color: #28a745; margin-top: 0; }
    .success-box p { color: #1a1a1a; }
    .reject-box { background-color: #ffffff; padding: 20px; border-radius: 8px; border-left: 5px solid #dc3545; }
    .reject-box h4 { color: #dc3545; margin-top: 0; }
    .reject-box p { color: #1a1a1a; }
    .incomplete-box { background-color: #ffffff; padding: 20px; border-radius: 8px; border-left: 5px solid #ff9800; }
    .incomplete-box h4 { color: #ff9800; margin-top: 0; }
    .incomplete-box p { color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

API_URL = "http://localhost:8000"

st.title("Verificador de Processos Judiciais")
st.markdown("Análise automatizada de conformidade com políticas de compra de crédito")

tab1, tab2, tab3 = st.tabs(["Análise", "Dados de Exemplo", "Sobre"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Dados do Processo")
    
    with col2:
        if st.button("Carregar Exemplo", use_container_width=True):
            st.session_state.show_example = True
    
    if st.session_state.get("show_example", False):
        st.info("Exemplo carregado. Edite os campos conforme necessário.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        numero_processo = st.text_input(
            "Número do Processo",
            value="0004587-00.2021.4.05.8100" if st.session_state.get("show_example") else "",
            placeholder="0000000-00.0000.0.00.0000"
        )
        
        classe = st.text_input(
            "Classe do Processo",
            value="Cumprimento de Sentença contra a Fazenda Pública" if st.session_state.get("show_example") else "",
            placeholder="Ex: Cumprimento de Sentença"
        )
        
        orgao_julgador = st.text_input(
            "Órgão Julgador",
            value="19ª VARA FEDERAL - SOBRAL/CE" if st.session_state.get("show_example") else "",
            placeholder="Ex: 19ª VARA FEDERAL"
        )
        
        ultima_distribuicao = st.date_input(
            "Última Distribuição",
            value=datetime(2024, 11, 18) if st.session_state.get("show_example") else None
        )
    
    with col2:
        valor_causa = st.number_input(
            "Valor da Causa (R$)",
            value=67592.0 if st.session_state.get("show_example") else 0.0,
            min_value=0.0,
            step=100.0
        )
        
        valor_condenacao = st.number_input(
            "Valor da Condenação (R$)",
            value=67592.0 if st.session_state.get("show_example") else 0.0,
            min_value=0.0,
            step=100.0
        )
        
        assunto = st.text_input(
            "Assunto",
            value="Rural (Art. 48/51)" if st.session_state.get("show_example") else "",
            placeholder="Ex: Causas Cíveis"
        )
        
        sigla_tribunal = st.text_input(
            "Sigla do Tribunal",
            value="TRF5" if st.session_state.get("show_example") else "",
            placeholder="Ex: TRF5"
        )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sigilo_justica = st.checkbox(
            "Segredo de Justiça",
            value=False
        )
    
    with col2:
        justica_gratuita = st.checkbox(
            "Justiça Gratuita",
            value=True if st.session_state.get("show_example") else False
        )
    
    with col3:
        esfera = st.selectbox(
            "Esfera",
            options=["Federal", "Estadual", "Trabalhista", "Eleitoral"],
            index=0 if st.session_state.get("show_example") else 0
        )
    
    st.markdown("---")
    
    st.subheader("Documentos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Sentença de Mérito")
        data_sentenca = st.date_input(
            "Data da Sentença",
            key="data_sentenca",
            value=datetime(2023, 9, 10) if st.session_state.get("show_example") else None
        )
        resumo_sentenca = st.text_area(
            "Resumo",
            value="Procedência parcial do pedido..." if st.session_state.get("show_example") else "",
            height=80,
            key="resumo_sentenca"
        )
    
    with col2:
        st.markdown("##### Trânsito em Julgado")
        transito_status = st.selectbox(
            "Status",
            options=["Sim", "Não"],
            index=0 if st.session_state.get("show_example") else 1,
            key="transito_status"
        )
        transito_indicacao = st.text_area(
            "Indicação",
            value="Certidão juntada em 12/12/2023..." if st.session_state.get("show_example") else "",
            height=80,
            key="transito_indicacao"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Cumprimento Definitivo")
        cumprimento_status = st.selectbox(
            "Status",
            options=["Sim", "Não"],
            index=0 if st.session_state.get("show_example") else 1,
            key="cumprimento_status"
        )
        cumprimento_data = st.date_input(
            "Data",
            key="cumprimento_data",
            value=datetime(2024, 1, 20) if st.session_state.get("show_example") else None
        )
    
    with col2:
        st.markdown("##### Óbito do Autor")
        obito_status = st.selectbox(
            "Status",
            options=["Não", "Sim"],
            index=0 if st.session_state.get("show_example") else 0,
            key="obito_status"
        )
        obito_habilitacao = st.selectbox(
            "Habilitação no Inventário",
            options=["Não aplicável", "Sim", "Não"],
            key="obito_habilitacao"
        )
    
    st.markdown("---")
    
    st.subheader("Honorários")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        honorarios_contratuais = st.number_input(
            "Contratuais (R$)",
            value=6000.0 if st.session_state.get("show_example") else 0.0,
            min_value=0.0,
            step=100.0
        )
    
    with col2:
        honorarios_periciais = st.number_input(
            "Periciais (R$)",
            value=1200.0 if st.session_state.get("show_example") else 0.0,
            min_value=0.0,
            step=100.0
        )
    
    with col3:
        honorarios_sucumbenciais = st.number_input(
            "Sucumbenciais (R$)",
            value=300.0 if st.session_state.get("show_example") else 0.0,
            min_value=0.0,
            step=100.0
        )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Analisar Processo", use_container_width=True, type="primary"):
            if not numero_processo or not classe or not orgao_julgador:
                st.error("Preencha os campos obrigatórios: Número, Classe e Órgão Julgador")
            else:
                with st.spinner("Analisando processo..."):
                    payload = {
                        "numeroProcesso": numero_processo,
                        "classe": classe,
                        "orgaoJulgador": orgao_julgador,
                        "ultimaDistribuicao": ultima_distribuicao.isoformat() + "T00:00:00Z",
                        "valorCausa": valor_causa if valor_causa > 0 else None,
                        "assunto": assunto,
                        "segredoJustica": sigilo_justica,
                        "justicaGratuita": justica_gratuita,
                        "siglaTribunal": sigla_tribunal,
                        "esfera": esfera,
                        "valorCondenacao": valor_condenacao if valor_condenacao > 0 else None,
                        "documentos": {
                            "sentencaMerito": {
                                "data": data_sentenca.isoformat() if data_sentenca else None,
                                "resumo": resumo_sentenca
                            } if resumo_sentenca else None,
                            "transitoJulgado": {
                                "status": transito_status,
                                "indicacao": transito_indicacao
                            },
                            "cumprimentoDefinitivoIniciado": {
                                "status": cumprimento_status,
                                "data": cumprimento_data.isoformat() if cumprimento_data else None
                            },
                            "obitoAutor": {
                                "status": obito_status,
                                "habilitacaoInventario": obito_habilitacao
                            }
                        },
                        "honorarios": {
                            "contratuais": honorarios_contratuais if honorarios_contratuais > 0 else None,
                            "periciais": honorarios_periciais if honorarios_periciais > 0 else None,
                            "sucumbenciais": honorarios_sucumbenciais if honorarios_sucumbenciais > 0 else None
                        }
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/verificar", json=payload)
                        
                        if response.status_code == 200:
                            resultado = response.json()
                            st.session_state.resultado = resultado
                            st.success("Análise concluída com sucesso!")
                        else:
                            st.error(f"Erro na API: {response.status_code}")
                            st.json(response.json())
                    
                    except requests.exceptions.ConnectionError:
                        st.error("Erro: Não foi possível conectar à API. Certifique-se que está rodando em http://localhost:8000")
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
    
    with col2:
        if st.button("Limpar Formulário", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    if st.session_state.get("resultado"):
        st.markdown("---")
        st.subheader("Resultado da Análise")
        
        resultado = st.session_state.resultado
        decision = resultado.get("decision", "").lower()
        
        if decision == "approved":
            st.markdown(f"""
                <div class="success-box">
                <h4>Resultado: APROVADO</h4>
                <p><strong>Justificativa:</strong> {resultado.get('rationale', '')}</p>
                <p><strong>Políticas Aplicadas:</strong> {', '.join(resultado.get('citacoes', []))}</p>
                </div>
                """, unsafe_allow_html=True)
        
        elif decision == "rejected":
            st.markdown(f"""
                <div class="reject-box">
                <h4>Resultado: REJEITADO</h4>
                <p><strong>Justificativa:</strong> {resultado.get('rationale', '')}</p>
                <p><strong>Políticas Violadas:</strong> {', '.join(resultado.get('citacoes', []))}</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown(f"""
                <div class="incomplete-box">
                <h4>Resultado: INCOMPLETO</h4>
                <p><strong>Justificativa:</strong> {resultado.get('rationale', '')}</p>
                <p><strong>Motivo:</strong> {', '.join(resultado.get('citacoes', []))}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("Ver JSON completo"):
            st.json(resultado)

with tab2:
    st.subheader("Dados de Exemplo")
    
    with open("dados.json", "r", encoding="utf-8") as f:
        exemplos = json.load(f)
    
    if exemplos:
        st.json(exemplos[0])
        st.info(f"Total de exemplos disponíveis: {len(exemplos)}")

with tab3:
    st.subheader("Sobre o Sistema")
    
    st.markdown("""
    ### Verificador de Processos Judiciais
    
    Este sistema automatiza a análise de processos judiciais de acordo com as políticas de compra de crédito da empresa.
    
    #### Políticas Implementadas
    
    - **POL-1:** Apenas processos transitados em julgado em fase de execução
    - **POL-2:** Valor de condenação deve ser informado
    - **POL-3:** Valor mínimo de R$ 1.000,00
    - **POL-4:** Sem condenações na esfera trabalhista
    - **POL-5:** Sem óbito do autor sem habilitação no inventário
    - **POL-6:** Sem substabelecimento sem reserva de poderes
    - **POL-7:** Informar honorários quando existirem
    - **POL-8:** Documentos essenciais obrigatórios
    
    #### Decisões Possíveis
    
    - **Aprovado:** Processo atende a todos os critérios
    - **Rejeitado:** Processo viola uma ou mais políticas
    - **Incompleto:** Faltam documentos ou informações essenciais
    
    #### Tecnologia
    
    - FastAPI para a API REST
    - Google Gemini 2.5 Flash para análise com IA
    - Streamlit para interface web
    - Python com Pydantic para validação de dados
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Modelos de Política", "8")
    
    with col2:
        st.metric("Decisões Possíveis", "3")
