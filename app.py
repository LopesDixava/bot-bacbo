import streamlit as st
from collections import Counter
import time

# Configuração da página
st.set_page_config(page_title="Bot Bac Bo PRO MAX", page_icon="🎲", layout="wide")

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
if 'ultima_analise_completa' not in st.session_state:
    st.session_state.ultima_analise_completa = None
if 'ultima_direcao_sugerida' not in st.session_state:
    st.session_state.ultima_direcao_sugerida = None
if 'aguardando_resultado' not in st.session_state:
    st.session_state.aguardando_resultado = False
if 'estatisticas_acertos' not in st.session_state:
    st.session_state.estatisticas_acertos = {
        'greens': 0,
        'reds': 0,
        'empates': 0,
        'historico_resultados': []
    }

# CSS TEMA ULTRA ESCURO PROFISSIONAL
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; }
    .stButton>button {
        width: 100%; height: 90px; font-size: 18px; font-weight: bold;
        border-radius: 12px; border: 2px solid #333; transition: all 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); border-color: #666; }
    .main .block-container { background-color: #0a0a0a; padding: 2rem; }
    .stMarkdown { color: #e0e0e0; }
    [data-testid="stMetric"] {
        background-color: #1a1a1a; border: 1px solid #333;
        border-radius: 10px; padding: 15px;
    }
    [data-testid="stMetricLabel"] { color: #aaaaaa !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    .historico-container {
        background-color: #0f0f0f; padding: 20px; border-radius: 12px;
        border: 1px solid #2a2a2a; font-family: 'Courier New', monospace;
        font-size: 20px; line-height: 2;
    }
    .jogador { color: #4a9eff; font-weight: bold; text-shadow: 0 0 5px #4a9eff; }
    .banca { color: #ff4d4d; font-weight: bold; text-shadow: 0 0 5px #ff4d4d; }
    .empate { color: #32cd32; font-weight: bold; text-shadow: 0 0 5px #32cd32; }
    
    /* SCORE CARD */
    .score-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        border: 2px solid #333;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }
    .score-number {
        font-size: 72px;
        font-weight: 900;
        margin: 10px 0;
        text-shadow: 0 0 20px currentColor;
    }
    .score-verde { color: #00ff88; border-color: #00ff88; }
    .score-amarelo { color: #ffaa00; border-color: #ffaa00; }
    .score-laranja { color: #ff8800; border-color: #ff8800; }
    .score-vermelho { color: #ff4444; border-color: #ff4444; }
    
    .recomendacao {
        font-size: 28px;
        font-weight: bold;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        letter-spacing: 2px;
    }
    .rec-entrar { background: #00ff8822; color: #00ff88; border: 2px solid #00ff88; }
    .rec-moderado { background: #ffaa0022; color: #ffaa00; border: 2px solid #ffaa00; }
    .rec-aguardar { background: #ff880022; color: #ff8800; border: 2px solid #ff8800; }
    .rec-evitar { background: #ff444422; color: #ff4444; border: 2px solid #ff4444; }
    
    /* DIREÇÃO VISUAL GIGANTE COM COR */
    .direcao-visual {
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        border: 4px solid;
        position: relative;
        overflow: hidden;
    }
    .direcao-visual::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0.1;
        z-index: 0;
    }
    .direcao-jogador {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a1a2a 100%);
        border-color: #4a9eff;
        box-shadow: 0 0 30px rgba(74, 158, 255, 0.3);
    }
    .direcao-banca {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a0a0a 100%);
        border-color: #ff4d4d;
        box-shadow: 0 0 30px rgba(255, 77, 77, 0.3);
    }
    .direcao-neutro {
        background: linear-gradient(135deg, #1a1a1a 0%, #1a1a1a 100%);
        border-color: #666;
        box-shadow: 0 0 30px rgba(100, 100, 100, 0.3);
    }
    .direcao-titulo {
        color: #aaaaaa;
        font-size: 16px;
        letter-spacing: 3px;
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }
    .direcao-icone {
        font-size: 80px;
        margin: 20px 0;
        position: relative;
        z-index: 1;
    }
    .direcao-texto {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    .direcao-jogador .direcao-texto {
        color: #4a9eff;
        text-shadow: 0 0 20px #4a9eff;
    }
    .direcao-banca .direcao-texto {
        color: #ff4d4d;
        text-shadow: 0 0 20px #ff4d4d;
    }
    .direcao-neutro .direcao-texto {
        color: #888;
    }
    
    .fator-item {
        background: #1a1a1a;
        border-left: 4px solid #4a9eff;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .fator-positivo { border-left-color: #00ff88; }
    .fator-negativo { border-left-color: #ff4444; }
    .fator-neutro { border-left-color: #ffaa00; }
    
    /* ESTATÍSTICAS DE ACERTOS */
    .stats-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        border: 2px solid #333;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
    }
    .stats-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        letter-spacing: 2px;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }
    .stat-box {
        background: #0a0a0a;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 2px solid #333;
    }
    .stat-box-green { border-color: #00ff88; }
    .stat-box-red { border-color: #ff4444; }
    .stat-box-empate { border-color: #32cd32; }
    .stat-box-assert { border-color: #4a9eff; }
    
    .stat-number {
        font-size: 48px;
        font-weight: 900;
        margin: 10px 0;
    }
    .stat-number-green { color: #00ff88; text-shadow: 0 0 15px #00ff88; }
    .stat-number-red { color: #ff4444; text-shadow: 0 0 15px #ff4444; }
    .stat-number-empate { color: #32cd32; text-shadow: 0 0 15px #32cd32; }
    .stat-number-assert { color: #4a9eff; text-shadow: 0 0 15px #4a9eff; }
    
    .stat-label {
        color: #aaaaaa;
        font-size: 12px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .alerta-aguardando {
        background: #ffaa0022;
        border: 2px solid #ffaa00;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #ffaa00;
        font-weight: bold;
        margin: 15px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    h1, h2, h3 { color: #ffffff !important; }
    hr { border-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES DE ANÁLISE PROFISSIONAL
# ============================================

def detectar_padrao_jogo(historico):
    """Detecta se o jogo está em DRAGON (sequência) ou CHOP (alternância)"""
    if len(historico) < 10:
        return "INDEFINIDO", 0
    
    alternancias = sum(1 for i in range(1, len(historico)) if historico[i] != historico[i-1])
    taxa_chop = (alternancias / (len(historico) - 1)) * 100
    
    max_seq = 1
    seq_atual = 1
    for i in range(1, len(historico)):
        if historico[i] == historico[i-1]:
            seq_atual += 1
            max_seq = max(max_seq, seq_atual)
        else:
            seq_atual = 1
    
    if taxa_chop > 65:
        return "CHOP (Alternância)", taxa_chop
    elif taxa_chop < 35 or max_seq >= 5:
        return "DRAGON (Sequência)", taxa_chop
    else:
        return "MISTO", taxa_chop

def analisar_tendencia(historico):
    """Compara curto prazo (últimas 10) vs longo prazo (todas)"""
    if len(historico) < 20:
        return None
    
    curto = historico[-10:]
    longo = historico
    
    cont_curto = Counter(curto)
    cont_longo = Counter(longo)
    
    j_curto = cont_curto.get("Jogador", 0)
    b_curto = cont_curto.get("Banca", 0)
    j_longo = cont_longo.get("Jogador", 0)
    b_longo = cont_longo.get("Banca", 0)
    
    if j_curto > b_curto * 1.3:
        tendencia_curto = "JOGADOR"
    elif b_curto > j_curto * 1.3:
        tendencia_curto = "BANCA"
    else:
        tendencia_curto = "NEUTRO"
    
    if j_longo > b_longo * 1.2:
        tendencia_longo = "JOGADOR"
    elif b_longo > j_longo * 1.2:
        tendencia_longo = "BANCA"
    else:
        tendencia_longo = "NEUTRO"
    
    return {
        "curto": tendencia_curto,
        "longo": tendencia_longo,
        "alinhadas": tendencia_curto == tendencia_longo and tendencia_curto != "NEUTRO"
    }

def probabilidade_condicional(historico):
    """O que aconteceu após a sequência atual X vezes nas últimas ocorrências?"""
    if len(historico) < 10:
        return None
    
    ultimo = historico[-1]
    tamanho_seq = 1
    for i in range(len(historico) - 2, -1, -1):
        if historico[i] == ultimo:
            tamanho_seq += 1
        else:
            break
    
    continuacoes = 0
    quebras = 0
    
    for i in range(len(historico) - tamanho_seq - 1):
        seq_ok = True
        for j in range(tamanho_seq):
            if i + j >= len(historico) or historico[i + j] != ultimo:
                seq_ok = False
                break
        
        if seq_ok and i + tamanho_seq < len(historico):
            proximo = historico[i + tamanho_seq]
            if proximo == ultimo:
                continuacoes += 1
            else:
                quebras += 1
    
    total = continuacoes + quebras
    if total == 0:
        return None
    
    return {
        "tamanho_seq": tamanho_seq,
        "resultado": ultimo,
        "continuacoes": continuacoes,
        "quebras": quebras,
        "total": total,
        "taxa_continuacao": (continuacoes / total) * 100,
        "taxa_quebra": (quebras / total) * 100
    }

def calcular_volatilidade(historico):
    """Mede o desvio em relação à matemática pura"""
    total = len(historico)
    contagem = Counter(historico)
    
    exp_j = total * 0.486
    exp_b = total * 0.486
    exp_e = total * 0.028
    
    qtd_j = contagem.get("Jogador", 0)
    qtd_b = contagem.get("Banca", 0)
    qtd_e = contagem.get("Empate", 0)
    
    vol = ((qtd_j - exp_j)**2)/exp_j + ((qtd_b - exp_b)**2)/exp_b + ((qtd_e - exp_e)**2)/exp_e
    return vol

def calcular_score_confianca(historico):
    """SISTEMA DE PONTUAÇÃO INTELIGENTE"""
    if len(historico) < 10:
        return 0, [], None
    
    score = 50
    fatores = []
    
    # 1. VOLATILIDADE
    vol = calcular_volatilidade(historico)
    if vol < 3:
        score += 15
        fatores.append(("🎯 Volatilidade BAIXA (jogo previsível)", "+15", "positivo"))
    elif vol < 7:
        score += 5
        fatores.append(("📊 Volatilidade NORMAL", "+5", "neutro"))
    elif vol > 15:
        score -= 15
        fatores.append(("🌪️ Volatilidade ALTA (jogo caótico)", "-15", "negativo"))
    else:
        score -= 5
        fatores.append(("⚠️ Volatilidade ELEVADA", "-5", "negativo"))
    
    # 2. PADRÃO DETECTÁVEL
    padrao, taxa = detectar_padrao_jogo(historico)
    if "DRAGON" in padrao or "CHOP" in padrao:
        score += 15
        fatores.append((f"🔗 Padrão claro: {padrao}", "+15", "positivo"))
    else:
        fatores.append(("🎲 Padrão INDEFINIDO (jogo errático)", "0", "neutro"))
    
    # 3. ALINHAMENTO DE TENDÊNCIAS
    tendencia = analisar_tendencia(historico)
    if tendencia and tendencia["alinhadas"]:
        score += 15
        fatores.append((f"📈 Tendências ALINHADAS ({tendencia['curto']})", "+15", "positivo"))
    elif tendencia and tendencia["curto"] != tendencia["longo"]:
        score -= 10
        fatores.append(("🔄 Tendências CONFLITANTES (curto vs longo)", "-10", "negativo"))
    
    # 4. SEQUÊNCIA ATUAL
    ultimo = historico[-1]
    seq_atual = 1
    for i in range(len(historico) - 2, -1, -1):
        if historico[i] == ultimo:
            seq_atual += 1
        else:
            break
    
    if seq_atual >= 7:
        score -= 20
        fatores.append((f"⚠️ Sequência MUITO longa ({seq_atual}x) - risco de reversão", "-20", "negativo"))
    elif seq_atual >= 5:
        score -= 10
        fatores.append((f"🔥 Sequência longa ({seq_atual}x) - atenção", "-10", "negativo"))
    elif seq_atual <= 2:
        score += 5
        fatores.append(("✅ Sequência curta (momento estável)", "+5", "positivo"))
    
    # 5. PROBABILIDADE CONDICIONAL
    prob_cond = probabilidade_condicional(historico)
    if prob_cond and prob_cond["total"] >= 3:
        if prob_cond["taxa_continuacao"] > 70:
            score += 10
            fatores.append((f"📊 Histórico favorece CONTINUAÇÃO ({prob_cond['taxa_continuacao']:.0f}%)", "+10", "positivo"))
        elif prob_cond["taxa_quebra"] > 70:
            score += 10
            fatores.append((f"📊 Histórico favorece QUEBRA ({prob_cond['taxa_quebra']:.0f}%)", "+10", "positivo"))
        else:
            fatores.append(("📊 Histórico inconclusivo", "0", "neutro"))
    
    # 6. EMPATES
    contagem = Counter(historico)
    taxa_empate = (contagem.get("Empate", 0) / len(historico)) * 100
    if taxa_empate > 10:
        score -= 10
        fatores.append((f"🟢 Muitos empates ({taxa_empate:.1f}%) - jogo instável", "-10", "negativo"))
    
    score = max(0, min(100, score))
    
    direcao = determinar_direcao(historico, padrao, tendencia, prob_cond)
    
    return score, fatores, direcao

def determinar_direcao(historico, padrao, tendencia, prob_cond):
    """Determina a melhor direção baseada em todos os fatores"""
    if len(historico) < 5:
        return "AGUARDAR MAIS DADOS"
    
    ultimo = historico[-1]
    oposto = "Banca" if ultimo == "Jogador" else "Jogador"
    
    if "DRAGON" in padrao:
        return f"CONTINUAR EM {ultimo.upper()}" if ultimo == "Jogador" else f"CONTINUAR EM {ultimo.upper()}"
    
    if "CHOP" in padrao:
        return f"VIRAR PARA {oposto.upper()}" if oposto == "Jogador" else f"VIRAR PARA {oposto.upper()}"
    
    if tendencia and tendencia["alinhadas"]:
        if tendencia["curto"] == "JOGADOR":
            return "SEGUIR TENDÊNCIA: JOGADOR"
        elif tendencia["curto"] == "BANCA":
            return "SEGUIR TENDÊNCIA: BANCA"
    
    if prob_cond and prob_cond["total"] >= 3:
        if prob_cond["taxa_continuacao"] > 70:
            return f"HISTÓRICO FAVORECE: {ultimo.upper()}"
        elif prob_cond["taxa_quebra"] > 70:
            return f"HISTÓRICO FAVORECE: {oposto.upper()}"
    
    return "SEM DIREÇÃO CLARA - EVITAR"

def classificar_score(score):
    """Classifica o score em categorias"""
    if score >= 75:
        return "ENTRAR COM CONFIANÇA", "rec-entrar", "score-verde"
    elif score >= 60:
        return "ENTRADA MODERADA", "rec-moderado", "score-amarelo"
    elif score >= 40:
        return "AGUARDAR MELHOR MOMENTO", "rec-aguardar", "score-laranja"
    else:
        return "EVITAR ENTRADA", "rec-evitar", "score-vermelho"

def extrair_direcao_limpa(direcao_completa):
    """Extrai apenas JOGADOR ou BANCA da direção completa"""
    if "JOGADOR" in direcao_completa:
        return "Jogador"
    elif "BANCA" in direcao_completa:
        return "Banca"
    else:
        return None

# ============================================
# INTERFACE
# ============================================

st.markdown("# 🎲 Bot Bac Bo PRO MAX")
st.markdown("---")

# SEÇÃO 1: Configuração da Banca
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
        st.session_state.ultima_analise_completa = None
        st.session_state.ultima_direcao_sugerida = None
        st.session_state.aguardando_resultado = False
        st.session_state.estatisticas_acertos = {'greens': 0, 'reds': 0, 'empates': 0, 'historico_resultados': []}
        st.rerun()

with col3:
    if st.button("🗑️ Limpar", use_container_width=True):
        st.session_state.historico = []
        st.session_state.banca_atual = st.session_state.banca_inicial
        st.session_state.analise_gerada = False
        st.session_state.ultima_analise_completa = None
        st.session_state.ultima_direcao_sugerida = None
        st.session_state.aguardando_resultado = False
        st.session_state.estatisticas_acertos = {'greens': 0, 'reds': 0, 'empates': 0, 'historico_resultados': []}
        st.rerun()

if not st.session_state.sessao_ativa:
    st.warning("⚠️ Configure a banca e clique em 'Iniciar Sessão' para começar.")
    st.stop()

st.markdown("---")

# SEÇÃO 2: Botões de Registro
st.markdown("### 🎯 Registrar Resultado ao Vivo")

# ALERTA SE ESTIVER AGUARDANDO RESULTADO
if st.session_state.aguardando_resultado:
    st.markdown(f"""
    <div class="alerta-aguardando">
        ⚠️ AGUARDANDO RESULTADO DA ANÁLISE<br>
        Direção sugerida: <strong>{st.session_state.ultima_direcao_sugerida}</strong><br>
        Registre o resultado real para contabilizar GREEN/RED
    </div>
    """, unsafe_allow_html=True)

col_j, col_b, col_e = st.columns(3)

with col_j:
    if st.button("🔵 JOGADOR", key="btn_jogador", use_container_width=True):
        st.session_state.historico.append("Jogador")
        st.session_state.analise_gerada = False
        
        # VERIFICA GREEN/RED
        if st.session_state.aguardando_resultado and st.session_state.ultima_direcao_sugerida:
            direcao_limpa = extrair_direcao_limpa(st.session_state.ultima_direcao_sugerida)
            if direcao_limpa == "Jogador":
                st.session_state.estatisticas_acertos['greens'] += 1
                st.session_state.estatisticas_acertos['historico_resultados'].append(('GREEN', 'Jogador'))
            else:
                st.session_state.estatisticas_acertos['reds'] += 1
                st.session_state.estatisticas_acertos['historico_resultados'].append(('RED', 'Jogador'))
            st.session_state.aguardando_resultado = False
        
        st.rerun()

with col_b:
    if st.button("🔴 BANCA", key="btn_banca", use_container_width=True):
        st.session_state.historico.append("Banca")
        st.session_state.analise_gerada = False
        
        # VERIFICA GREEN/RED
        if st.session_state.aguardando_resultado and st.session_state.ultima_direcao_sugerida:
            direcao_limpa = extrair_direcao_limpa(st.session_state.ultima_direcao_sugerida)
            if direcao_limpa == "Banca":
                st.session_state.estatisticas_acertos['greens'] += 1
                st.session_state.estatisticas_acertos['historico_resultados'].append(('GREEN', 'Banca'))
            else:
                st.session_state.estatisticas_acertos['reds'] += 1
                st.session_state.estatisticas_acertos['historico_resultados'].append(('RED', 'Banca'))
            st.session_state.aguardando_resultado = False
        
        st.rerun()

with col_e:
    if st.button("🟢 EMPATE", key="btn_empate", use_container_width=True):
        st.session_state.historico.append("Empate")
        st.session_state.analise_gerada = False
        
        # EMPATE SEMPRE É GREEN
        if st.session_state.aguardando_resultado:
            st.session_state.estatisticas_acertos['empates'] += 1
            st.session_state.estatisticas_acertos['historico_resultados'].append(('EMPATE', 'Empate'))
            st.session_state.aguardando_resultado = False
        
        st.rerun()

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("↩️ Desfazer Último", key="btn_desfazer", use_container_width=True):
        if st.session_state.historico:
            st.session_state.historico.pop()
            st.session_state.analise_gerada = False
            st.rerun()

st.markdown("---")

# SEÇÃO 3: Histórico Visual
st.markdown("### 📊 Histórico da Sessão")

if not st.session_state.historico:
    st.info("Aguardando resultados ao vivo...")
else:
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
    
    historico_html = '<div class="historico-container">'
    for linha_idx in range(linhas_por_coluna):
        for coluna in colunas:
            if linha_idx < len(coluna):
                res = coluna[linha_idx]
                classe = res.lower()
                historico_html += f'<span class="{classe}">● </span>'
            else:
                historico_html += '<span style="color: #1a1a1a;">● </span>'
        historico_html += '<br>'
    historico_html += '</div>'
    
    st.markdown(historico_html, unsafe_allow_html=True)

st.markdown("---")

# SEÇÃO 4: Botão de Análise com Cooldown REDUZIDO (5s)
st.markdown("### 📈 Análise Profissional")

tempo_atual = time.time()
tempo_desde_ultima = tempo_atual - st.session_state.ultima_analise
cooldown = 5  # REDUZIDO de 15s para 5s

pode_analisar = tempo_desde_ultima >= cooldown or not st.session_state.analise_gerada

if pode_analisar:
    if st.button("🧠 GERAR ANÁLISE PRO MAX", key="btn_analise", use_container_width=True):
        if len(st.session_state.historico) >= 10:
            score, fatores, direcao = calcular_score_confianca(st.session_state.historico)
            st.session_state.ultima_analise_completa = {
                "score": score,
                "fatores": fatores,
                "direcao": direcao,
                "timestamp": time.time()
            }
            st.session_state.analise_gerada = True
            st.session_state.ultima_analise = time.time()
            st.session_state.ultima_direcao_sugerida = direcao
            st.session_state.aguardando_resultado = True
            st.rerun()
        else:
            st.warning("⚠️ Registre pelo menos 10 resultados para uma análise confiável.")
else:
    tempo_restante = int(cooldown - tempo_desde_ultima)
    st.button(f"⏳ Aguarde... ({tempo_restante}s)", key="btn_analise_disabled", disabled=True, use_container_width=True)
    time.sleep(1)
    st.rerun()

# SEÇÃO 5: Resultados da Análise PRO MAX
if st.session_state.ultima_analise_completa:
    analise = st.session_state.ultima_analise_completa
    score = analise["score"]
    fatores = analise["fatores"]
    direcao = analise["direcao"]
    
    recomendacao, classe_rec, classe_score = classificar_score(score)
    
    st.markdown(f"""
    <div class="score-card {classe_score}">
        <div style="color: #aaaaaa; font-size: 14px; letter-spacing: 3px;">SCORE DE CONFIANÇA</div>
        <div class="score-number">{score}</div>
        <div style="color: #888; font-size: 16px;">de 100 pontos</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="recomendacao {classe_rec}">⚡ {recomendacao}</div>', unsafe_allow_html=True)
    
    # DIREÇÃO VISUAL GIGANTE COM COR
    direcao_limpa = extrair_direcao_limpa(direcao)
    if direcao_limpa == "Jogador":
        classe_direcao = "direcao-jogador"
        icone = "🔵"
        texto_direcao = "JOGADOR"
    elif direcao_limpa == "Banca":
        classe_direcao = "direcao-banca"
        icone = "🔴"
        texto_direcao = "BANCA"
    else:
        classe_direcao = "direcao-neutro"
        icone = "⚪"
        texto_direcao = "EVITAR"
    
    st.markdown(f"""
    <div class="direcao-visual {classe_direcao}">
        <div class="direcao-titulo">🎯 DIREÇÃO SUGERIDA PELA MÁQUINA</div>
        <div class="direcao-icone">{icone}</div>
        <div class="direcao-texto">{texto_direcao}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔍 Fatores Analisados pela Máquina")
    
    for fator, pontos, tipo in fatores:
        st.markdown(f"""
        <div class="fator-item fator-{tipo}">
            <span style="color: #e0e0e0;">{fator}</span>
            <span style="color: {'#00ff88' if '+' in pontos else '#ff4444' if '-' in pontos else '#ffaa00'}; font-weight: bold;">{pontos}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    total = len(st.session_state.historico)
    contagem = Counter(st.session_state.historico)
    
    with col1:
        st.metric("🔵 Jogador", f"{contagem.get('Jogador', 0)}x ({contagem.get('Jogador', 0)/total*100:.1f}%)")
    with col2:
        st.metric("🔴 Banca", f"{contagem.get('Banca', 0)}x ({contagem.get('Banca', 0)/total*100:.1f}%)")
    with col3:
        st.metric("🟢 Empate", f"{contagem.get('Empate', 0)}x ({contagem.get('Empate', 0)/total*100:.1f}%)")
    
    entrada_sugerida = st.session_state.banca_atual * 0.02
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Banca Atual", f"R$ {st.session_state.banca_atual:.2f}")
    with col2:
        st.metric("💵 Entrada Sugerida (2%)", f"R$ {entrada_sugerida:.2f}")

elif st.session_state.analise_gerada:
    st.info("Registre pelo menos 10 resultados para gerar uma análise PRO MAX.")
else:
    st.info("🧠 Clique em 'GERAR ANÁLISE PRO MAX' para ativar a máquina de análise.")

# ============================================
# SEÇÃO 6: ESTATÍSTICAS DE ACERTOS
# ============================================

st.markdown("---")
st.markdown("### 📊 Estatísticas de Assertividade")

stats = st.session_state.estatisticas_acertos
greens = stats['greens']
reds = stats['reds']
empates = stats['empates']
total_apostas = greens + reds + empates

if total_apostas > 0:
    taxa_assertividade = ((greens + empates) / total_apostas) * 100
else:
    taxa_assertividade = 0

st.markdown(f"""
<div class="stats-container">
    <div class="stats-title">🎯 DESEMPENHO DO BOT</div>
    <div class="stats-grid">
        <div class="stat-box stat-box-green">
            <div class="stat-label">GREENS</div>
            <div class="stat-number stat-number-green">{greens}</div>
            <div class="stat-label">Acertos</div>
        </div>
        <div class="stat-box stat-box-red">
            <div class="stat-label">REDS</div>
            <div class="stat-number stat-number-red">{reds}</div>
            <div class="stat-label">Erros</div>
        </div>
        <div class="stat-box stat-box-empate">
            <div class="stat-label">EMPATES</div>
            <div class="stat-number stat-number-empate">{empates}</div>
            <div class="stat-label">Push</div>
        </div>
        <div class="stat-box stat-box-assert">
            <div class="stat-label">ASSERTIVIDADE</div>
            <div class="stat-number stat-number-assert">{taxa_assertividade:.1f}%</div>
            <div class="stat-label">{total_apostas} análises</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Histórico detalhado
if stats['historico_resultados']:
    st.markdown("### 📝 Histórico Detalhado de Resultados")
    
    historico_html = '<div style="background: #0f0f0f; padding: 15px; border-radius: 10px; border: 1px solid #2a2a2a;">'
    for i, (resultado, tipo) in enumerate(reversed(stats['historico_resultados'][-20:]), 1):
        cor = "#00ff88" if resultado == "GREEN" else "#ff4444" if resultado == "RED" else "#32cd32"
        icone = "✅" if resultado == "GREEN" else "❌" if resultado == "RED" else "🟢"
        historico_html += f'<div style="color: {cor}; padding: 8px; border-bottom: 1px solid #1a1a1a;">{icone} Análise #{len(stats["historico_resultados"]) - i + 1}: {resultado} ({tipo})</div>'
    historico_html += '</div>'
    
    st.markdown(historico_html, unsafe_allow_html=True)
