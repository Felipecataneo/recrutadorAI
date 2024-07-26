import os
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings

class CustomPDFSearchInput(BaseModel):
    query: str = Field(..., description="The query to search for in the PDFs")

class CustomPDFSearchTool(BaseTool):
    name: str = "Custom PDF Search"
    description: str = "Search through multiple PDFs for relevant information"
    args_schema: Type[BaseModel] = CustomPDFSearchInput
    pdf_directory: str = Field(..., description="Directory containing PDF files to search")
    documents: list = Field(default_factory=list, exclude=True)
    embeddings: OpenAIEmbeddings = Field(default_factory=OpenAIEmbeddings, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.documents = self._load_documents()

    def _load_documents(self):
        documents = []
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)

    def _run(self, query: str) -> str:
        query_embedding = self.embeddings.embed_query(query)
        
        # Compute similarities
        similarities = []
        for doc in self.documents:
            doc_embedding = self.embeddings.embed_query(doc.page_content)
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((similarity, doc))
        
        # Sort by similarity (descending order)
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 5 results
        top_results = similarities[:5]
        return "\n\n".join([doc.page_content for _, doc in top_results])

    def _cosine_similarity(self, a, b):
        return sum(x*y for x, y in zip(a, b)) / (sum(x*x for x in a)**0.5 * sum(y*y for y in b)**0.5)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("CustomPDFSearchTool does not support async")