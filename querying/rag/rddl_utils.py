import re
import os
import pyRDDLGym

# Extract RDDL blocks from LLM response
def extract_rddl_blocks(rddl_text):
    blocks = {}
    patterns = {
        "domain": r"### Domain Block\n```rddl([\s\S]+?)```",
        "non-fluents": r"### Non-Fluent Block\n```rddl([\s\S]+?)```",
        "instance": r"### Instance Block\n```rddl([\s\S]+?)```"
    }
    for block_name, pattern in patterns.items():
        match = re.search(pattern, rddl_text)
        if match:
            blocks[block_name] = match.group(1)
    return blocks

# Save RDDL blocks to files
def save_rddl_blocks_to_files(rddl_text, output_dir, i):
    rddl_blocks = extract_rddl_blocks(rddl_text)
    os.makedirs(output_dir, exist_ok=True)
    if "domain" in rddl_blocks:
        domain_file_path = os.path.join(output_dir, f"{i}_domain.rddl")
        with open(domain_file_path, 'w') as f:
            f.write(rddl_blocks["domain"])
    if "non-fluents" in rddl_blocks or "instance" in rddl_blocks:
        instance_file_path = os.path.join(output_dir, f"{i}_instance.rddl")
        with open(instance_file_path, 'w') as f:
            if "non-fluents" in rddl_blocks:
                f.write(rddl_blocks["non-fluents"] + '\n\n')
            if "instance" in rddl_blocks:
                f.write(rddl_blocks["instance"])

# Load RDDL files and track errors
def load_rddl_and_track_errors(domain_file, instance_file):
    success_count, error_count = 0, 0
    error_types = {}
    try:
        env = pyRDDLGym.make(domain_file, instance_file)
        success_count += 1
        return env
    except Exception as e:
        error_count += 1
        error_type, error_message = type(e).__name__, str(e)
        error_types.setdefault(error_type, []).append(error_message)
        return success_count, error_count, error_types


def load_rddl_into_list(main_dir):
    # Gather all file paths from main_dir and its subdirectories
    all_files = []
    for root, dirs, files in os.walk(main_dir):
        for file in files:
            # Get all .txt files in the current directory
            all_files.append(os.path.join(file))
    all_files.sort()
    return all_files
