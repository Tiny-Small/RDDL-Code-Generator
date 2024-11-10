from config import load_env
from rag.load_data import load_files, read_files_content
from rag.process_data import process_content, generate_metadata
from rag.index import create_index, save_index

# Load environment variables
ENV_PATH = "../.env"
load_env(ENV_PATH)

# Define main directory
MAIN_DIR = "data/IPPC2011"

# Load and preprocess files
all_files = load_files(MAIN_DIR)
documents = read_files_content(all_files)

# Process files and generate metadata
updated_strings, captured_content = process_content(documents)
metadatas = generate_metadata(captured_content)

# Create and persist the index
index = create_index(updated_strings, metadatas)
PERSIST_DIR = "../storage"
save_index(index, PERSIST_DIR)
