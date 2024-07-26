import os
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

class CustomPDFSearchInput(BaseModel):
    query: str = Field(..., description="The query to search for in the PDFs")

class CustomPDFSearchTool(BaseTool):
    name: str = "Custom PDF Search"
    description: str = "Search through multiple PDFs for relevant information"
    args_schema: Type[BaseModel] = CustomPDFSearchInput
    pdf_directory: str = Field(..., description="Directory containing PDF files to search")
    vectorstore: FAISS = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.vectorstore = self._create_vectorstore()

    def _create_vectorstore(self):
        documents = []
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        return FAISS.from_documents(texts, OpenAIEmbeddings())

    def _run(self, query: str) -> str:
        results = self.vectorstore.similarity_search(query, k=5)
        return "\n\n".join([doc.page_content for doc in results])

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("CustomPDFSearchTool does not support async")