import re
from llama_index.core import Document

# Process each document by splitting and removing delimiters
def process_content(loader_all):
    captured_content = []
    updated_strings = []
    for string in loader_all:
        parts = re.split(r'//////////////////////////////////////////////////////////////////\n', string)
        if len(parts) > 1:
            captured_content.append(parts[1].strip())
            updated_string = '\n'.join((parts[2:])).strip()
            updated_strings.append(updated_string)
        else:
            updated_strings.append(string.strip())
    return updated_strings, captured_content

# Generate metadata by repeating captured content for each document
def generate_metadata(captured_content):
    metadatas = []
    for item in captured_content:
        metadatas.extend([{"document": item}] * 11)
    return metadatas
