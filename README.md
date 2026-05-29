# vector-dbs

A hands-on exploration of vector databases for AI / RAG (Retrieval-Augmented Generation) applications. The repo contains runnable examples for three popular vector stores — **ChromaDB**, **pgvector (PostgreSQL)**, and **Pinecone** — plus a small end-to-end document-based RAG pipeline using OpenAI embeddings.

## Contents

| File / Folder | What it demonstrates |
|---|---|
| `chroma_emb.py` | Generating embeddings with Chroma's default embedding function (`all-MiniLM-L6-v2`). |
| `chroma_add_query_docs.py` | Adding documents to an in-memory Chroma collection and running similarity queries. |
| `chroma_persist.py` | Same as above but using a `PersistentClient` so data survives between runs (`./chroma_persist_data`). |
| `openai_embedding.py` | Two ways of integrating OpenAI embeddings with Chroma — using the built-in `OpenAIEmbeddingFunction`, and manual embedding handling. |
| `document_based_rag.py` | Full RAG pipeline: load `.txt` files from `./data/new_articles`, chunk, embed with OpenAI, store in Chroma, retrieve relevant chunks, and answer questions with `gpt-4o-mini`. |
| `pinecone_intro.py` | Creating a serverless Pinecone index, upserting vectors with metadata, and running a top-k similarity query. |
| `pg_vector/basic_connection.py` | Connecting to PostgreSQL and enabling the `pgvector` extension. |
| `pg_vector/quick_demo.py` | Creating a `vector(3)` column, inserting sample vectors, and running a distance-based similarity search (`<->` operator). |
| `pg_vector/enable_extension.sql` | SQL snippet to enable and verify the `pgvector` extension. |
| `data/new_articles/` | Source `.txt` documents consumed by the RAG example. |
| `*.png`, `*.jpeg`, `*.jpg` | Reference diagrams: chunking strategy, vector DB comparison, how to choose a vector DB, and the course completion certificate. |

## Requirements

- Python `>= 3.12`
- [`uv`](https://docs.astral.sh/uv/) for dependency management
- PostgreSQL with the `pgvector` extension (only for the `pg_vector/` examples)
- API keys for OpenAI and Pinecone (only for the examples that use them)

Dependencies (see `pyproject.toml`):

- `chromadb`
- `openai`
- `pgvector`
- `pinecone`
- `psycopg2` / `psycopg2-binary`

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Copy `.env.example` to `.env` and fill in your keys:

   ```env
   OPENAI_API_KEY=<your-openai-key>
   PINECONE_API_KEY=<your-pinecone-key>
   ```

3. (Optional, for pgvector examples) Make sure PostgreSQL is running and update the `DATABASE_URL` in `pg_vector/basic_connection.py` / `pg_vector/quick_demo.py` to match your local credentials.

## Running the examples

Each script is runnable on its own via `uv run`:

```bash
# Chroma — embeddings & basic CRUD
uv run -m chroma_emb
uv run -m chroma_add_query_docs
uv run -m chroma_persist

# Chroma + OpenAI embeddings
uv run -m openai_embedding

# Document-based RAG (uncomment indexing() on first run inside the script)
uv run -m document_based_rag

# Pinecone
uv run -m pinecone_intro

# pgvector
uv run -m pg_vector.basic_connection
uv run -m pg_vector.quick_demo
```

## Notes

- Chroma persistent data lives in `./chroma_db`, `./chroma_db_1`, and `./chroma_persist_data` (gitignored).
- For `document_based_rag.py`, the first run should call `indexing()` to populate the collection; subsequent runs can comment it out and use only `retrieval()`.
- The Pinecone example creates a serverless index named `quickstarts` in `aws / us-east-1` with `dimension=3` and cosine metric — change as needed.
