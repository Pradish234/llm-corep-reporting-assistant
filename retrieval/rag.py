from pathlib import Path
from typing import List

from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain.embeddings.base import Embeddings


class RegulatoryRAG:
    """
    Retrieval component for PRA Rulebook and COREP instruction excerpts.
    Designed for auditability and deterministic behaviour.
    """

    def __init__(
        self,
        documents_path: List[str],
        embedding_model: Embeddings,
    ):
        self.documents_path = documents_path
        self.embedding_model = embedding_model
        self.vectorstore = self._build_vectorstore()

    def _load_documents(self) -> List[Document]:
        documents = []

        for path in self.documents_path:
            file_path = Path(path)
            if not file_path.exists():
                raise FileNotFoundError(f"Document not found: {path}")

            text = file_path.read_text(encoding="utf-8")

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name,
                        "document_type": file_path.parent.name,
                    },
                )
            )

        return documents

    def _build_vectorstore(self) -> FAISS:
        raw_documents = self._load_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )

        chunked_documents = splitter.split_documents(raw_documents)

        return FAISS.from_documents(
            chunked_documents,
            self.embedding_model,
        )

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieve the top-k most relevant regulatory text chunks.
        """
        return self.vectorstore.similarity_search(query, k=k)
