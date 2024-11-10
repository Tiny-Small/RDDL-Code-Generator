# from llama_index.core import Settings  # Import if needed for Settings.llm

async def query_with_feedback(initial_prompt, query_engine, error_message, Settings, iteration, memory):
    print(f"System: Iteration {iteration + 1}\n")

    if iteration == 0:
        # Initial response with the initial prompt
        response_text = query_engine.query(initial_prompt).response
    else:
        # Generate correction prompt based on the provided error message
        correction_prompt = f"""
        The generated RDDL code failed with the following error:
        {error_message}

        Please refine the code and correct any issues based on the error above.
        """
        memory.append(correction_prompt)  # Append correction prompt to memory
        prompt_with_memory = "\n\n".join(memory)

        # Await async completion
        response = await Settings.llm.acomplete(prompt_with_memory)
        response_text = response.text  # Adjust as per actual response structure

    # Append response to memory for the next iteration
    memory.append(response_text)

    yield response_text, memory
