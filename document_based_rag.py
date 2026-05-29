import chromadb
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv(override=True)
openai_key = os.getenv("OPENAI_API_KEY")
open_client = OpenAI(api_key=openai_key)
directory_path = "./data/new_articles"

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


def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    for filename in os.listdir(directory_path):
        print("file name:-- ", filename)
        if filename.endswith(".txt"):
            with open(
                os.path.join(directory_path, filename), "r", encoding="utf-8"
            ) as file:
                documents.append({"id": filename, "text": file.read()})
    return documents


# Function to split text into chunks
def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks
def get_openai_embedding(text):
    response = open_client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


# =================================
# === For initial setup -- Uncomment (below) all for the first run, and then comment it all out ===
# =================================
# Function to load documents from a directory
def indexing():
    documents = load_documents_from_directory(directory_path)
    print("documents:", len(documents))

    chunked_documents = []
    for doc in documents:
        chunks = split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}_{i}", "text": chunk})

    print("chunked documents:", len(chunked_documents))

    # Generate embeddings for the document chunks
    for doc in chunked_documents:
        print("==== Generating embeddings... ====")
        doc["embedding"] = get_openai_embedding(doc["text"])

    # Upsert documents with embeddings into Chroma
    # manage embeddings manually by providing embeddings=[doc["embedding"]] in the upsert method
    for doc in chunked_documents:
        print("==== Inserting chunks into db;;; ====")
        collection.upsert(
            ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]]
        )
# === End of the initial setup -- Uncomment all for the first run, and then comment it all out ===
# =================================

# Function to query documents
def query_documents(question, n_results=2):
    # query_embedding = get_openai_embedding(question)
    results = collection.query(query_texts=question, n_results=n_results)

    # Extract Only documents from the results and ignore ids and distances for now
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    print("==== Returning relevant chunks ====")
    return relevant_chunks
    # for idx, document in enumerate(results["documents"][0]):
    #     doc_id = results["ids"][0][idx]
    #     distance = results["distances"][0][idx]
    #     print(f"Found document chunk: {document} (ID: {doc_id}, Distance: {distance})")


# Function to generate a response from OpenAI
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = open_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message
    return answer



def retrieval():
    question = "Sundar Pichai"
    relevant_chunks = query_documents(question)
    print(f"relevant chunks: {relevant_chunks}")
    answer = generate_response(question, relevant_chunks)

    print("==== Answer ====")
    print(answer.content)

def main():
    # === For initial setup -- Uncomment (below) all for the first run, and then comment it all out ===
    #indexing()
    retrieval()


# uv run -m document_based_rag
if __name__ == '__main__':
    main()