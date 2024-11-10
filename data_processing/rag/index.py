from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.nvidia import NVIDIAEmbedding

# Initialize the NVIDIA embedding model
def initialize_embedding_model():
    Settings.embed_model = NVIDIAEmbedding(model="nvidia/nv-embedqa-mistral-7b-v2", truncate="END")

# Create the document index
def create_index(documents, metadatas):
    docs = [Document(text=content) for content in documents]
    for idx, document in enumerate(docs):
        document.metadata["description"] = metadatas[idx]["document"]
    initialize_embedding_model()
    index = VectorStoreIndex.from_documents(docs)
    return index

# Save the index to disk for later use
def save_index(index, persist_dir):
    index.storage_context.persist(persist_dir=persist_dir)
