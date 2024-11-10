# main.py
import os
import asyncio
import pyRDDLGym

from llama_index.core import Settings
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.nvidia_rerank import NVIDIARerank

from config import load_env
from rag.storage import load_vector_store
from rag.query_engine import create_query_engine
from rag.rddl_utils import save_rddl_blocks_to_files, load_rddl_and_track_errors, load_rddl_into_list
from rag.conversation import query_with_feedback

# Set directories
PERSIST_DIR = "../storage"
OUTPUT_DIR = "InterimOutputs_ReAct"
SAVE_DIR = "InterimOutputs_ReAct/Correct"
ENV_PATH = "../.env"

# Configure components and Load index
load_env(ENV_PATH)
Settings.embed_model = NVIDIAEmbedding(model="nvidia/nv-embedqa-mistral-7b-v2", truncate="END")
Settings.llm = OpenAI(model="gpt-4o", temperature=1)
reranker = NVIDIARerank(model="nvidia/llama-3.2-nv-rerankqa-1b-v1", top_n=20, truncate="END")
index = load_vector_store(PERSIST_DIR)
query_engine = create_query_engine(index, reranker)

async def run_conversation_loop(job_description, max_iterations, output_dir, save_dir):
    initial_prompt = f"""
    You are an RDDL code generator.
    Generate a complete and compilable RDDL code based on the job description below, ensuring it is fully functional in pyRDDLGym.

    Job Description: {job_description}

    Use the following structure for the RDDL code:

    ### Domain Block
    ```rddl
    <DOMAIN BLOCK CODE>
    ```
    ### Non-Fluent Block
    ```rddl
    <NON-FLUENT CODE>
    ```
    ### Instance Block
    ```rddl
    <INSTANCE CODE>
    """
    memory = [initial_prompt]
    error_message = ""

    all_files = load_rddl_into_list(save_dir)
    result = set(int(item.split('_')[0]) for item in all_files)
    max_num = max(result) + 1 if result else 0

    for iteration in range(max_iterations):
        async for response_text, memory in query_with_feedback(
            initial_prompt, query_engine, error_message, Settings, iteration, memory
        ):
            print(f"System: Iteration {iteration + 1}\n")
            print(f"LLM Response:\n{response_text}\n")

            # Save the response as RDDL code blocks
            save_rddl_blocks_to_files(response_text, output_dir, iteration)

            # Define file paths for the generated RDDL files
            domain_file = os.path.join(output_dir, f"{iteration}_domain.rddl")
            instance_file = os.path.join(output_dir, f"{iteration}_instance.rddl")

            # Attempt to load the RDDL code in pyRDDLGym
            results = load_rddl_and_track_errors(domain_file, instance_file)
            print(f"results:\n{results}\n")

            # Check for success or errors
            if isinstance(results, pyRDDLGym.core.env.RDDLEnv):
                print("System: RDDL code loaded successfully!")
                save_rddl_blocks_to_files(response_text, save_dir, max_num)
                return response_text, None  # Return the response text as successful output

            # Capture and handle errors
            error_message = ""
            for error_type, messages in results[2].items():
                error_message += f"{error_type}: {messages[-1]}\n"
            if iteration == max_iterations - 1:
                return None, "Maximum iterations reached without successful RDDL code load."
    return None, error_message
