from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

from app.services.embedding_service import embedding_model
from app.services.llm_service import generate_completion


class RAGService:

    @staticmethod
    def load_documents():

        docs = []

        folder_path = "app/data/rag_docs"

        for filename in os.listdir(folder_path):

            if filename.endswith(".txt"):

                loader = TextLoader(
                    os.path.join(folder_path, filename),
                    encoding="utf-8"
                )

                docs.extend(loader.load())

        return docs

    @staticmethod
    def create_vector_store():

        documents = RAGService.load_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="chroma_db"
        )

        return vector_db

    @staticmethod
    def ask_question(question):

        vector_db = RAGService.create_vector_store()

        retriever = vector_db.as_retriever(
            search_kwargs={"k": 2}
        )

        docs = retriever.invoke(question)

        if not docs:
            return {
                "answer": "I do not know based on the provided documents"
            }

        context = "\n\n".join([
            doc.page_content for doc in docs
        ])

        prompt = f'''
Answer ONLY from the provided context.

Context:
{context}

Question:
{question}

If answer is not present in context, say:
"I do not know based on the provided documents."
'''

        answer = generate_completion(prompt)
       

        citations = [
            doc.metadata.get("source")
            for doc in docs
        ]

        return {
            "answer": answer,
            "citations": citations
        }