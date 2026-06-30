import streamlit as st
import google.generativeai as genai

# Puxa a chave de forma segura das configurações ocultas do Streamlit
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

# Configuração da página para celular
st.set_page_config(page_title="Corretor ENEM", page_icon="📝", layout="centered")

st.title("📝 Corretor de Redação ENEM (Grátis)")
st.write("Insira o tema e o seu texto abaixo para uma correção sem vícios.")

# --- ARQUITETURA DE MEMÓRIA (RESET DE CACHE/CAMPOS) ---
# Inicializa os campos na memória se eles não existirem
if "tema_redacao" not in st.session_state:
    st.session_state.tema_redacao = ""
if "texto_redacao" not in st.session_state:
    st.session_state.texto_redacao = ""

# Função que limpa a memória e força o app a recomeçar do zero
def limpar_campos():
    st.session_state.tema_redacao = ""
    st.session_state.texto_redacao = ""
    st.rerun()

# Entradas conectadas ao gerenciador de memória
tema = st.text_input("Tema da Redação:", key="tema_redacao", placeholder="Ex: O impacto das IAs na educação...")
texto_redacao = st.text_area("Cole sua Redação aqui:", key="texto_redacao", height=250, placeholder="Digite ou cole o texto completo...")

# Layout dos botões principais
col1, col2 = st.columns([2, 1])

with col1:
    botao_corrigir = st.button("🚀 Corrigir Redação", use_container_width=True)
with col2:
    # Botão de reset rápido sempre visível
    st.button("🔄 Limpar Tudo", on_click=limpar_campos, use_container_width=True)

# Processamento da correção
if botao_corrigir:
    if not tema or not texto_redacao:
        st.warning("⚠️ Por favor, preencha o tema e a redação!")
    else:
        with st.spinner("Analisando sua redação rigidamente... Aguarde."):
            
            prompt_sistema = f"""
            Você é um corretor de redação do ENEM extremamente rigoroso e analítico. 
            Analise o texto enviado estritamente sob os seguintes critérios:
            
            CORREÇÃO 1: Domínio da norma culta da língua escrita (Gramática, pontuação, regência, crase).
            CORREÇÃO 2: Compreensão do tema e aplicação das áreas do conhecimento (Estrutura dissertativa-argumentativa).
            CORREÇÃO 3: Seleção, relação, organização e interpretação de informações (Coerência e argumentação).
            CORREÇÃO 4: Demonstração de conhecimento dos mecanismos linguísticos (Coesão e conectivos).
            
            FORMATO OBRIGATÓRIO DE RESPOSTA:
            Na primeira linha da sua resposta, você deve escrever APENAS o número da nota total somada (que é a soma das 4 competências, variando de 0 a 800).
            Escreva na primeira linha exatamente assim: NOTA_TOTAL: [VALOR]
            
            Nas linhas seguintes, retorne a análise detalhada dividida exatamente nos 4 tópicos (CORREÇÃO 1, 2, 3 e 4), apontando os erros de forma direta, sem elogios, e dando a nota de 0 a 200 para cada critério.

            Tema da Redação: {tema}
            Texto da Redação: {texto_redacao}
            """
            
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    generation_config={"temperature": 0.2}
                )
                
                response = model.generate_content(prompt_sistema)
                resultado_bruto = response.text
                
                if "NOTA_TOTAL:" in resultado_bruto:
                    linhas = resultado_bruto.split("\n")
                    linha_nota = [l for l in lines if "NOTA_TOTAL:" in l][0]
                    nota_final = linha_nota.replace("NOTA_TOTAL:", "").strip()
                    resultado_formatated = "\n".join([l for l in lines if "NOTA_TOTAL:" not in l])
                else:
                    nota_final = "N/A"
                    resultado_formatated = resultado_bruto
                
                st.success("✨ Correção Concluída!")
                st.metric(label="💯 Nota Final Estimada (C1 a C4)", value=f"{nota_final} / 800")
                
                st.markdown("### 📊 Resultado da Avaliação Detalhada")
                st.markdown(resultado_formatated)
                
                # Botão extra no final do relatório para facilitar a vida dela no celular
                st.write("---")
                st.button("📝 Iniciar Nova Redação (Limpar)", on_click=limpar_campos, key="btn_fim", use_container_width=True)
                
            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")