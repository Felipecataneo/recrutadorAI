import streamlit as st
import os
from crew import RecruitmentCrew
import tempfile
from custom_pdf_tool import CustomPDFSearchTool

# Configuração da página Streamlit
st.set_page_config(page_title="Recrutamento AI", layout="wide")

# Sidebar
st.sidebar.title("Configurações")

# Input para OPENAI_API_KEY
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
os.environ["OPENAI_API_KEY"] = api_key

# Picklist para OPENAI_MODEL_NAME
model_options = [
    "gpt-3.5-turbo",
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4o-mini"
]
selected_model = st.sidebar.selectbox("Selecione o modelo OpenAI", model_options)
os.environ["OPENAI_MODEL_NAME"] = selected_model

# Upload de arquivo para job_requirements
job_req_file = st.sidebar.file_uploader("Upload Job Requirements (TXT)", type="txt")

# Upload de arquivo para rh_interview (opcional)
rh_interview_file = st.sidebar.file_uploader("Upload RH Interview (TXT, opcional)", type="txt")

# Área principal
st.title("Sistema de Recrutamento AI")

# Upload de currículos
uploaded_cvs = st.file_uploader("Upload Currículos (PDF)", type="pdf", accept_multiple_files=True)

# Limite de PDFs
MAX_PDF_COUNT = 50

# Botão para gerar
if st.button("Gerar Análise"):
    if not api_key:
        st.error("Por favor, insira sua OpenAI API Key.")
    elif not job_req_file:
        st.error("Por favor, faça o upload do arquivo de requisitos do trabalho.")
    elif not uploaded_cvs:
        st.error("Por favor, faça o upload de pelo menos um currículo.")
    elif len(uploaded_cvs) > MAX_PDF_COUNT:
        st.warning(f"Por favor, faça upload de no máximo {MAX_PDF_COUNT} PDFs.")
        uploaded_cvs = uploaded_cvs[:MAX_PDF_COUNT]
    else:
        with st.spinner("Analisando currículos... Isso pode levar alguns minutos."):
            # Criar diretório temporário para os PDFs
            with tempfile.TemporaryDirectory() as temp_dir:
                # Salvar os PDFs no diretório temporário
                for uploaded_file in uploaded_cvs:
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Criar CustomPDFSearchTool com o diretório de PDFs
                pdf_tool = CustomPDFSearchTool(pdf_directory=temp_dir)
                
                # Ler conteúdo dos arquivos de texto
                job_requirements = job_req_file.getvalue().decode("utf-8")
                rh_interview = rh_interview_file.getvalue().decode("utf-8") if rh_interview_file else ""
                
                # Preparar inputs
                inputs = {
                    'job_requirements': job_requirements,
                    'rh_interview': rh_interview
                }
                
                # Executar a análise
                crew = RecruitmentCrew(pdf_tool=pdf_tool)
                result = crew.crew().kickoff(inputs=inputs)
                
                # Exibir resultados
                st.success("Análise concluída!")
                st.write(result)

# Instruções de uso
st.markdown("""
## Como usar:
1. Insira sua OpenAI API Key na barra lateral.
2. Selecione o modelo OpenAI desejado.
3. Faça o upload do arquivo de requisitos do trabalho (obrigatório).
4. Opcionalmente, faça o upload do arquivo de entrevista de RH.
5. Faça o upload dos currículos em PDF que deseja analisar (máximo de 50).
6. Clique em "Gerar Análise" para iniciar o processo.
7. Como gerar sua API key na Openai (https://www.ionos.com/pt-br/digitalguide/sites-de-internet/desenvolvimento-web/chatgpt-api/)
""")