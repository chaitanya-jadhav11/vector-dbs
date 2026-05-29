import os

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(override=True)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# You have two main ways to integrate OpenAI embeddings with Chroma.
# Option 1 — Recommended (Best Way)
#
# Use Chroma’s built-in OpenAI embedding function

def option_1():

    # Create OpenAI embedding function
    openai_ef = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
    # Create Chroma client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Create collection with embedding function
    collection = chroma_client.get_or_create_collection(
        name="my_docs",
        embedding_function=openai_ef
    )

    # Add documents
    collection.upsert(
        ids=["doc1", "doc2"],
        documents=[
            "Spring Boot is a Java framework",
            "LangChain helps build AI applications"
        ]
    )

    # Query
    results = collection.query(
        query_texts=["Java framework"],
        n_results=2
    )

    print(results)

# Option 2 — Manual Embedding Handling
# This gives more control.
# Useful when:
#
# using custom pipelines
# caching embeddings
# multi-model systems
# advanced architectures
def option_2():

    # Create embedding manually
    response = openai_client.embeddings.create(
        input="Spring Boot is awesome",
        model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding

    # Create chroma client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    collection = chroma_client.get_or_create_collection(
        name="manual_embeddings"
    )

    # Store embedding manually
    collection.upsert(
        ids=["doc1"],
        documents=["Spring Boot is awesome"],
        embeddings=[embedding]
    )




def main():
    option_1()
    option_2()


# uv run -m openai_embedding
if __name__ == '__main__':
    main()