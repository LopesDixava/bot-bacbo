import streamlit as st
from collections import Counter
import time

# Configuração da página
st.set_page_config(page_title="Bot Bac Bo PRO", page_icon="🎲", layout="wide")

# Inicialização do estado da sessão
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'banca_inicial' not in st.session_state:
    st.session_state.banca_inicial = 0.0
if 'banca_atual' not in st.session_state:
    st.session_state.banca_atual = 0.0
if 'sessao_ativa' not in st.session_state:
    st.session_state.sessao_ativa = False
if 'ultima_analise' not in st.session_state:
    st.session_state.ultima_analise = 0
if 'analise_gerada' not in st.session_state:
    st.session_state.analise_gerada = False

# CSS personalizado para botões grandes e responsivos
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        border: none;
    }
    .botao-jogador {
        background-color: #1e90ff !important;
        color: white !important;
    }
    .botao-banca {
        background-color: #dc143c !important;
        color: white !important;
    }
    .botao-empate {
        background-color: #32cd32 !important;
        color: white !important;
    }
    .botao-analise {
        background-color: #ffaa00 !important;
        color: black !important;
        height: 100px !important;
        font-size: 22px !important;
    }
    .botao-analise:disabled {
        background-color: #555555 !important;
        color: #aaaaaa !important;
    }
    .historico-container {
        background-color: #121212;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        font-size: 18px;
        line-height: 1.8;
    }
    .jogador { color: #1e90ff; font-weight: bold; }
    .banca { color: #ff4d4d; font-weight: bold; }
    .empate { color: #32cd32; font-weight: bold; }
    .alerta { color: #ffaa00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown("# 🎲 Bot de Estatísticas Bac Bo PRO")
st.markdown("---")

# --- SEÇÃO 1: Configuração da Banca ---
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    banca_input = st.number_input("💰 Banca Inicial (R$)", value=500.0, min_value=0.0, step=50.0, format="%.2f")

with col2:
    if st.button("🚀 Iniciar Sessão", use_container_width=True):
        st.session_state.banca_inicial = banca_input
        st.session_state.banca_atual = banca_input
        st.session_state.historico = []
        st.session_state.sessao_ativa = True
        st.session_state.analise_gerada = False
        st.rerun()

with col3:
    if st.button("🗑️ Limpar", use_container_width=True):
        st.session_state.historico = []
        st.session_state.banca_atual = st.session_state.banca_inicial
        st.session_state.analise_gerada = False
        st.rerun()

if not st.session_state.sessao_ativa:
    st.warning("⚠️ Configure a banca e clique em 'Iniciar Sessão' para começar.")
    st.stop()

st.markdown("---")

# --- SEÇÃO 2: Botões de Registro ao Vivo ---
st.markdown("### 🎯 Registrar Resultado ao Vivo")

col_j, col_b, col_e, col_d = st.columns(4)

with col_j:
    if st.button("🔵 JOGADOR", key="btn_jogador"):
        st.session_state.historico.append("Jogador")
        st.session_state.analise_gerada = False
        st.rerun()

with col_b:
    if st.button("🔴 BANCA", key="btn_banca"):
        st.session_state.historico.append("Banca")
        st.session_state.analise_gerada = False
        st.rerun()

with col_e:
    if st.button("🟢 EMPATE", key="btn_empate"):
        st.session_state.historico.append("Empate")
        st.session_state.analise_gerada = False
        st.rerun()

with col_d:
    if st.button("↩️ Desfazer", key="btn_desfazer"):
        if st.session_state.historico:
            st.session_state.historico.pop()
            st.session_state.analise_gerada = False
            st.rerun()

st.markdown("---")

# --- SEÇÃO 3: Histórico Visual ---
st.markdown("### 📊 Histórico da Sessão")

if not st.session_state.historico:
    st.info("Aguardando resultados ao vivo...")
else:
    # Organiza em grade (8 linhas por coluna)
    linhas_por_coluna = 8
    colunas = []
    coluna_atual = []
    ultimo_item = None
    
    for item in st.session_state.historico:
        if item == ultimo_item or not coluna_atual:
            coluna_atual.append(item)
            if len(coluna_atual) >= linhas_por_coluna:
                colunas.append(coluna_atual)
                coluna_atual = []
                ultimo_item = None
        else:
            colunas.append(coluna_atual)
            coluna_atual = [item]
        ultimo_item = item
        
    if coluna_atual:
        colunas.append(coluna_atual)
    
    # Renderiza o histórico com cores
    historico_html = '<div class="historico-container">'
    for linha_idx in range(linhas_por_coluna):
        for coluna in colunas:
            if linha_idx < len(coluna):
                res = coluna[linha_idx]
                classe = res.lower()
                historico_html += f'<span class="{classe}">● </span>'
            else:
                historico_html += '<span style="color: #333;">● </span>'
        historico_html += '<br>'
    historico_html += '</div>'
    
    st.markdown(historico_html, unsafe_allow_html=True)

st.markdown("---")

# --- SEÇÃO 4: Botão de Análise com Cooldown ---
st.markdown("### 📈 Análise Profissional")

tempo_atual = time.time()
tempo_desde_ultima = tempo_atual - st.session_state.ultima_analise
cooldown = 15

pode_analisar = tempo_desde_ultima >= cooldown or not st.session_state.analise_gerada

if pode_analisar:
    if st.button("📊 GERAR ANÁLISE PROFISSIONAL", key="btn_analise", use_container_width=True):
        st.session_state.analise_gerada = True
        st.session_state.ultima_analise = time.time()
        st.rerun()
else:
    tempo_restante = int(cooldown - tempo_desde_ultima)
    st.button(f"⏳ Aguarde... ({tempo_restante}s)", key="btn_analise_disabled", disabled=True, use_container_width=True)
    # Auto-refresh para atualizar o contador
    time.sleep(1)
    st.rerun()

# --- SEÇÃO 5: Resultados da Análise ---
if st.session_state.analise_gerada and len(st.session_state.historico) >= 5:
    total = len(st.session_state.historico)
    contagem = Counter(st.session_state.historico)
    
    qtd_j = contagem.get("Jogador", 0)
    qtd_b = contagem.get("Banca", 0)
    qtd_e = contagem.get("Empate", 0)
    
    # Sequência atual
    seq_atual = 1
    ultimo = st.session_state.historico[-1]
    for i in range(len(st.session_state.historico) - 2, -1, -1):
        if st.session_state.historico[i] == ultimo:
            seq_atual += 1
        else:
            break
    
    # Volatilidade
    exp_j = total * 0.486
    exp_b = total * 0.486
    exp_e = total * 0.028
    vol = ((qtd_j - exp_j)**2)/exp_j + ((qtd_b - exp_b)**2)/exp_b + ((qtd_e - exp_e)**2)/exp_e
    
    # Entrada sugerida
    entrada_sugerida = st.session_state.banca_atual * 0.02
    
    # Exibe as métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔵 Jogador", f"{qtd_j}x ({qtd_j/total*100:.1f}%)")
    
    with col2:
        st.metric("🔴 Banca", f"{qtd_b}x ({qtd_b/total*100:.1f}%)")
    
    with col3:
        st.metric("🟢 Empate", f"{qtd_e}x ({qtd_e/total*100:.1f}%)")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🔥 Sequência Atual", f"{seq_atual}x {ultimo}")
        st.metric("💰 Banca Atual", f"R$ {st.session_state.banca_atual:.2f}")
    
    with col2:
        if vol > 10:
            st.markdown(f'<p class="alerta">🌪️ Volatilidade: {vol:.2f} (ALTA - Cuidado!)</p>', unsafe_allow_html=True)
        else:
            st.metric("🌪️ Volatilidade", f"{vol:.2f} (Normal)")
        st.metric("💵 Entrada Sugerida (2%)", f"R$ {entrada_sugerida:.2f}")
    
    # Alertas especiais
    if seq_atual >= 6:
        st.warning(f"⚠️ SEQUÊNCIA LONGA DETECTADA: {seq_atual}x {ultimo}")
    
    if vol > 10:
        st.warning("⚠️ ALTA VOLATILIDADE: O jogo está fugindo da matemática padrão. Reduza o risco!")

elif st.session_state.analise_gerada:
    st.info("Registre pelo menos 5 resultados para gerar uma análise.")

else:
    st.info("Clique em 'GERAR ANÁLISE PROFISSIONAL' para ver as estatísticas.")
