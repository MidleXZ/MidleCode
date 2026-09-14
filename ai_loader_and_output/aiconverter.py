def convert_dsl_to_python(llm_instance, dsl_code: str) -> str:
    system_prompt = (
        "You are an expert software compiler. Convert the user's custom GUI syntax "
        "into runnable Python code using standard `tkinter`. "
        "Return ONLY standard, executable Python code with no markdown backticks, "
        "no explanations, and no extra commentary."
    )

    response = llm_instance.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": dsl_code}
        ],
        temperature=0.1
    )

    output = response["choices"][0]["message"]["content"].strip()

    # Clean markdown backticks if model generated them
    if output.startswith("```"):
        output = "\n".join(output.split("\n")[1:])
    if output.endswith("```"):
        output = output[:-3]

    return output.strip()