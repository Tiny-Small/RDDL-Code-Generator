# app.py
import streamlit as st
import asyncio
from main import run_conversation_loop

st.title("RDDL Code Generator")

# User input for job description
job_description = st.text_area("Describe the environment for which you need RDDL code:",
                               "Generate a RDDL code of a 3 by 3 Game of Life.")
max_iterations = st.number_input("Max Iterations", min_value=1, max_value=40, value=20)

# Directories for saving files
OUTPUT_DIR = "InterimOutputs_ReAct"
SAVE_DIR = "InterimOutputs_ReAct/Correct"

# Run the RDDL generation process
if st.button("Generate RDDL Code"):
    st.write("Generating RDDL code...")

    # Run asynchronous code in Streamlit
    result_text = None
    error_text = None

    # Async function to run the conversation loop and collect result
    async def generate_rddl():
        global result_text, error_text
        result_text, error_text = await run_conversation_loop(job_description, max_iterations, OUTPUT_DIR, SAVE_DIR)

    # Use asyncio.run to call async function
    asyncio.run(generate_rddl())

    # Display results
    if result_text:
        st.success("RDDL code generated successfully!")
        st.code(result_text, language="rddl")
    else:
        st.error("Failed to generate a valid RDDL code.")
        st.write(error_text)
