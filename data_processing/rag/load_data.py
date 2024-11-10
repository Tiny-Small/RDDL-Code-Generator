import os

# Gather all file paths from main_dir and its subdirectories
def load_files(main_dir):
    all_files = []
    for root, dirs, files in os.walk(main_dir):
        if os.path.basename(root) == "MDP":  # Only process "MDP" directories
            for file in files:
                all_files.append(os.path.join(root, file))
    all_files.sort()
    return all_files

# Load content from files into a list
def read_files_content(file_paths):
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            documents.append(content)
    return documents
