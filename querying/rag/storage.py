from llama_index.core import StorageContext, load_index_from_storage

# Load existing vector store index from storage
def load_vector_store(persist_dir="../../storage"):
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index
