import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents():
    docs = []
    for root, _, files in os.walk("data"):
        for f in files:
            if f.endswith(".txt"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    docs.append(file.read())
    return docs

def init_retriever():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    embeddings = AzureOpenAIEmbeddings(
       azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
          api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))

    vector_db = Chroma.from_texts(
        chunks,
        embeddings
    )
    return vector_db.as_retriever(search_k=4)