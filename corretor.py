import streamlit as st
import openai

# 1. Configuração da API
# Substitua pela sua chave real ou configure nos segredos do Streamlit

# Puxa a chave de forma segura das configurações ocultas do Streamlit
api_key = st.secrets["api_key"]
client = openai.OpenAI(api_key=api_key)

# Configuração da página para celular
st.set_page_config(page_title="Corretor ENEM", page_icon="📝", layout="centered")

st.title("📝 Corretor de Redação ENEM")
st.write("Insira o tema e o seu texto abaixo para uma correção sem vícios.")

# 2. Entradas da sua esposa (Interface no celular)
tema = st.text_input("Tema da Redação:", placeholder="Ex: O impacto das IAs na educação...")
texto_redacao = st.text_area("Cole sua Redação aqui:", height=250, placeholder="Digite ou cole o texto completo...")

# Botão de envio
if st.button("🚀 Corrigir Redação", use_container_width=True):
    if not tema or not texto_redacao:
        st.warning("⚠️ Por favor, preencha o tema e a redação!")
    else:
        with st.spinner("Analisando sua redação rigidamente... Aguarde."):
            
            # 3. O prompt com os seus critérios 1, 2, 3 e 4
            prompt_sistema = """
            Você é um corretor de redação do ENEM extremamente rigoroso e analítico. 
            Analise o texto enviado estritamente sob os seguintes critérios:
            
            CORREÇÃO 1: Domínio da norma culta da língua escrita (Gramática, pontuação, regência, crase).
            CORREÇÃO 2: Compreensão do tema e aplicação das áreas do conhecimento (Estrutura dissertativa-argumentativa).
            CORREÇÃO 3: Seleção, relação, organização e interpretação de informações (Coerência e argumentação).
            CORREÇÃO 4: Demonstração de conhecimento dos mecanismos linguísticos (Coesão e conectivos).
            
            Retorne a análise dividida exatamente nesses 4 tópicos (CORREÇÃO 1, 2, 3 e 4), apontando os erros de forma direta, sem elogios ou condescendência, e dê uma nota estimada de 0 a 200 para cada critério.
            """
            
            try:
                # Requisição limpa para a IA (Evita o vício)
                response = client.chat.completions.create(
                    model="gpt-4o", 
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"Tema: {tema}\n\nRedação:\n{texto_redacao}"}
                    ],
                    temperature=0.2
                )
                
                resultado = response.choices[0].message.content
                
                # 4. Exibe o resultado na tela do celular
                st.success("✨ Correção Concluída!")
                st.markdown("### 📊 Resultado da Avaliação")
                st.markdown(resultado)
                
            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")