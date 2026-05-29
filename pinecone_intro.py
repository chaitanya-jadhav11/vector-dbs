# Add lib
# uv add pinecone

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


load_dotenv()

pinecone_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_key)

index_name = "quickstarts"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=3,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )


index = pc.Index(index_name)

index.upsert(
    vectors=[
        {
            "id": "vec1",
            "values": [1.0, 2.0, 3.0],
            "metadata": {"text": "first vector"}
        },
        {
            "id": "vec2",
            "values": [4.0, 5.0, 6.0],
            "metadata": {"text": "second vector"}
        }
    ]
)
# Target the index

# Upsert the records into a namespace
# Wait for the upserted vectors to be indexed
import time
time.sleep(10)

# View stats for the index
stats = index.describe_index_stats()
print(stats)

results = index.query(
    vector=[1.0, 2.0, 3.0],
    top_k=2,
    include_metadata=True
)

print(results)
# output
# DescribeIndexStatsResponse(dimension=3, total_vector_count=2, metric='cosine', namespaces=1)
# QueryResponse(matches=[ScoredVector(id='vec1', score=1.00112152, values=[], metadata={'text': 'first vector'}),
# ScoredVector(id='vec2', score=0.975468338, values=[], metadata={'text': 'second vector'})],
# namespace='', usage=Usage(read_units=1, write_units=None),
# response_info=ResponseInfo(raw_headers={'date': 'Fri, 29 May 2026 06:36:53 GMT', 'content-type': 'application/json',
# 'content-length': '227', 'connection': 'keep-alive', 'x-pinecone-max-indexed-lsn': '1', 'x-pinecone-request-latency-ms': '39',
# 'x-envoy-upstream-service-time': '39', 'x-pinecone-response-duration-ms': '41', 'grpc-status': '0', 'server': 'envoy'}))

def main():
    pass

# uv run -m pinecone_intro
if __name__ == '__main__':
    main()