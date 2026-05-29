from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

default_ef = DefaultEmbeddingFunction()

name = "Paulo"

emb = default_ef([name])

print(emb)
# output
# [array([-5.19150868e-03,  1.48886638e-02, -4.77073677e-02,  6.03342578e-02,
#        -9.30737257e-02,  3.51901390e-02,  1.37157468e-02,  5.03949411e-02,
#        -2.36647134e-03,  7.57837761e-03,  5.08506559e-02, -1.43065602e-01,
#        -1.71903744e-01,  2.41975747e-02, -6.77832067e-02, -7.00052502e-03,
#        -6.78276469e-04,  4.69658040e-02,  2.93568131e-02,  2.30538361e-02,
#        dtype=float32)]
def main():
    pass

# uv run -m chroma_emb
if __name__ == '__main__':
    main()

