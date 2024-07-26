# Recrutador AI

Recrutador AI é uma aplicação Streamlit que utiliza inteligência artificial para auxiliar no processo de recrutamento, analisando currículos e requisitos de trabalho.

## Características

- Upload e análise de múltiplos currículos em PDF
- Definição de requisitos de trabalho
- Análise opcional de relatórios de entrevista de RH
- Utilização de modelos de linguagem avançados da OpenAI para análise
- Interface amigável construída com Streamlit

## Instalação

1. Clone o repositório:
git clone https://github.com/seu-usuario/recrutador-ai.git
cd recrutador-ai
2. Crie um ambiente virtual e ative-o:
python -m venv venv
source venv/bin/activate  # No Windows use venv\Scripts\activate
3. Instale as dependências:
pip install -r requirements.txt

Abra seu navegador e acesse `http://localhost:8501`

4. Na interface do aplicativo:
- Insira sua chave de API OpenAI
- Selecione o modelo OpenAI desejado
- Faça upload do arquivo de requisitos do trabalho (obrigatório)
- Opcionalmente, faça upload do arquivo de entrevista de RH
- Faça upload dos currículos em PDF que deseja analisar
- Clique em "Gerar Análise" para iniciar o processo

## Estrutura do Projeto

- `main.py`: Arquivo principal do Streamlit
- `crew.py`: Define a estrutura da equipe de recrutamento AI
- `custom_pdf_tool.py`: Ferramenta personalizada para busca em PDFs
- `config/`: Diretório contendo arquivos de configuração
- `agents.yaml`: Configuração dos agentes AI
- `tasks.yaml`: Configuração das tarefas de recrutamento

## Dependências

- streamlit
- crewai
- langchain
- langchain-community
- pydantic
- PyPDF2
- faiss-cpu
- openai
- PyYAML

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## Aviso

Este projeto utiliza a API da OpenAI, que pode incorrer em custos. Certifique-se de entender a estrutura de preços da OpenAI antes de usar extensivamente.
