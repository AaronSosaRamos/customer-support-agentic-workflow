from langchain_qdrant import FastEmbedSparse, RetrievalMode
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

def compile_and_return_retriever(docs):
    vector_store = QdrantVectorStore.from_documents(
        docs,
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        location=":memory:",
        collection_name="my_documents",
        retrieval_mode=RetrievalMode.HYBRID,
    )

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})

    return retriever