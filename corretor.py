import streamlit as st
import google.generativeai as genai

# Puxa a chave de forma segura das configurações ocultas do Streamlit
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

# Configuração da página para celular
st.set_page_config(page_title="Corretor ENEM", page_icon="📝", layout="centered")

st.title("📝 Corretor de Redação ENEM")
st.write("Insira o tema e o seu texto abaixo para uma correção sem vícios.")

# --- CONTROLE DE FLUXO E MEMÓRIA ---
if "tema_redacao" not in st.session_state:
    st.session_state.tema_redacao = ""
if "texto_redacao" not in st.session_state:
    st.session_state.texto_redacao = ""
if "corrigido" not in st.session_state:
    st.session_state.corrigido = False
if "resultado_analise" not in st.session_state:
    st.session_state.resultado_analise = ""
if "nota_final" not in st.session_state:
    st.session_state.nota_final = ""

# Função para resetar e zerar o app
def limpar_tudo():
    st.session_state.tema_redacao = ""
    st.session_state.texto_redacao = ""
    st.session_state.resultado_analise = ""
    st.session_state.nota_final = ""
    st.session_state.corrigido = False
    st.rerun()

# Entradas sincronizadas com o estado interno do Streamlit
tema = st.text_input("Tema da Redação:", key="tema_redacao", placeholder="Ex: O impacto das IAs na educação...")
texto_redacao = st.text_area("Cole sua Redação aqui:", key="texto_redacao", height=250, placeholder="Digite ou cole o texto completo...")

# --- ALTERNÂNCIA DE BOTÕES (MÁQUINA DE ESTADOS) ---
if not st.session_state.corrigido:
    # Se NÃO foi corrigido ainda, mostra o botão tradicional para corrigir
    if st.button("🚀 Corrigir Redação", use_container_width=True):
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
                        model_name="gemini-2.0-flash", # Modelo estável oficial, grátis e sem o bug do 404
                        generation_config={"temperature": 0.2}
                    )
                    response = model.generate_content(prompt_sistema)
                    resultado_bruto = response.text
                    
                    if "NOTA_TOTAL:" in resultado_bruto:
                        linhas = resultado_bruto.split("\n")
                        linha_nota = [l for l in lines if "NOTA_TOTAL:" in l][0]
                        st.session_state.nota_final = linha_nota.replace("NOTA_TOTAL:", "").strip()
                        st.session_state.resultado_analise = "\n".join([l for l in lines if "NOTA_TOTAL:" not in l])
                    else:
                        st.session_state.nota_final = "N/A"
                        st.session_state.resultado_analise = resultado_bruto
                    
                    # Ativa o estado de corrigido e atualiza a tela
                    st.session_state.corrigido = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro ao conectar com o servidor: {e}")
else:
    # Se JÁ foi corrigido, o botão antigo some e este aparece no exato lugar dele
    st.button("🔄 Nova Correção (Limpar Tela)", on_click=limpar_tudo, use_container_width=True)

# --- EXIBIÇÃO DO RESULTADO (SÓ APARECE SE TIVER SIDO CORRIGIDO) ---
if st.session_state.corrigido:
    st.success("✨ Correção Concluída!")
    st.metric(label="💯 Nota Final Estimada (C1 a C4)", value=f"{st.session_state.nota_final} / 800")
    st.markdown("### 📊 Resultado da Avaliação Detalhada")
    st.markdown(st.session_state.resultado_analise)