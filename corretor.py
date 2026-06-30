import streamlit as st
import google.generativeai as genai

# Puxa a chave de forma segura das configurações ocultas do Streamlit
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

# Configuração da página para celular
st.set_page_config(page_title="Corretor ENEM", page_icon="📝", layout="centered")

st.title("📝 Corretor de Redação ENEM ")
st.write("Insira o tema e o seu texto abaixo para uma correção sem vícios.")

# Entradas da sua esposa (Interface no celular)
tema = st.text_input("Tema da Redação:", placeholder="Ex: O impacto das IAs na educação...")
texto_redacao = st.text_area("Cole sua Redação aqui:", height=250, placeholder="Digite ou cole o texto completo...")

# Botão de envio
if st.button("🚀 Corrigir Redação", use_container_width=True):
    if not tema or not texto_redacao:
        st.warning("⚠️ Por favor, preencha o tema e a redação!")
    else:
        with st.spinner("Analisando sua redação rigidamente... Aguarde."):
            
            
            # 3. O prompt com os seus critérios 1, 2, 3 e 4 + Nota Total
            prompt_sistema = f"""
            Você é um corretor de redação do ENEM extremamente rigoroso e analítico. 
            Analise o texto enviado estritamente sob os seguintes critérios:
            
            CORREÇÃO 1: Domínio da norma culta da língua escrita (Gramática, pontuação, regência, crase).
            CORREÇÃO 2: Compreensão do tema e aplicação das áreas do conhecimento (Estrutura dissertativa-argumentativa).
            CORREÇÃO 3: Seleção, relação, organização e interpretação de informações (Coerência e argumentação).
            CORREÇÃO 4: Demonstração de conhecimento dos mecanismos linguísticos (Coesão e conectivos).
            
            FORMATO OBRIGATÓRIO DE RESPOSTA:
            Na primeira linha da sua resposta, você deve escrever APENAS o número da nota total somada (que é a soma das 4 competências, variando de 0 a 800 já que não avaliamos a Proposta de Intervenção/Competência 5 aqui, ou adapte para 0 a 1000 dividindo proporcionalmente). 
            Para o ENEM padrão com as 4 competências que você pediu, vamos dar a nota de 0 a 800.
            Escreva na primeira linha exatamente assim: NOTA_TOTAL: [VALOR]
            
            Nas linhas seguintes, retorne a análise detalhada dividida exatamente nos 4 tópicos (CORREÇÃO 1, 2, 3 e 4), apontando os erros de forma direta, sem elogios, e dando a nota de 0 a 200 para cada critério.

            Tema da Redação: {tema}
            Texto da Redação: {texto_redacao}
            """
            
            try:
                # Usando o modelo Flash que é 100% gratuito e ultra rápido
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    generation_config={"temperature": 0.2}
                )
                
                response = model.generate_content(prompt_sistema)
                resultado_bruto = response.text
                
                # Separa a nota total do resto do texto
                if "NOTA_TOTAL:" in resultado_bruto:
                    linhas = resultado_bruto.split("\n")
                    linha_nota = [l for l in linhas if "NOTA_TOTAL:" in l][0]
                    nota_final = linha_nota.replace("NOTA_TOTAL:", "").strip()
                    # Remove a linha da nota do texto principal para não duplicar
                    resultado_formatado = "\n".join([l for l in linhas if "NOTA_TOTAL:" not in l])
                else:
                    nota_final = "N/A"
                    resultado_formatado = resultado_bruto
                
                # 4. Exibe o resultado na tela do celular
                st.success("✨ Correção Concluída!")
                
                # Destaca a nota final dela em um painel bonito
                st.metric(label="💯 Nota Final Estimada (C1 a C4)", value=f"{nota_final} / 800")
                
                st.markdown("### 📊 Resultado da Avaliação Detalhada")
                st.markdown(resultado_formatado)
                
            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")