from basilica import Connection

API_KEY = "ba063e4f-17ce-e0d0-43fc-943b39462921"

sentences = [
    "This is a sentence!",
    "This is a similar sentence",
    "I don't think this sentence is similar at all...",
]

connection = Connection(API_KEY)
print("CONNECTION", type(connection))

embeddings = list(connection.embed_sentences(sentences))
print(embeddings)

breakpoint()