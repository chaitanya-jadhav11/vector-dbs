import chromadb


def get_documents():
    documents = [
        {"id": "doc1", "text": "Hello, world!"},
        {"id": "doc2", "text": "How are you today?."},
        {"id": "doc3", "text": "GoodBye. see you later!"},
    ]
    return documents


chroma_client = chromadb.Client()
collection_name = "test_collection"
collection = chroma_client.get_or_create_collection(name=collection_name)

docs = get_documents()

for doc in docs:
    collection.upsert(ids=doc["id"], documents=doc["text"])
    # Load a default embedding function C:\Users\Admin\.cache\chromadb\
    # default embedding :-- all-MiniLM-L6-v2/onnx.tar.gz

results= collection.query(query_texts="greeting message",n_results=3 )

for result in results:
    print(result)
    # OUTPUT
    # 1) ids 2)  embeddings 3) documents 4)  uris 5)  included 6)  data 7)  metadatas 8)  distances

print(results["ids"]) #
#output [['doc1', 'doc2', 'doc3']]

print(results["documents"])
# [['Hello, world!', 'How are you today?.', 'GoodBye. see you later!']]

print("----------------Print results one by one----------------")
# [0] ==== results for query1,  bz  query can accept multiple queries like
# collection.query(query_texts=[
#         "hello",
#         "water"
#     ],

ids = results["ids"][0] # results for query1
docs = results["documents"][0] # results for query1
distances = results["distances"][0] # results for query1

for id_, doc, distance in zip(ids, docs, distances):
    print(f"ID: {id_}")
    print(f"Document: {doc}")
    print(f"Distance: {distance}")
    print("-" * 30)




def main():
    pass

# uv run -m chroma_add_query_docs
if __name__ == '__main__':
    main()