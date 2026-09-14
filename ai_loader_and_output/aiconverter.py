def convert_dsl_to_python(llm_instance, dsl_code, target_language="python"):
    """
    Converts MidleCode DSL into specified programming language code using local LLM.
    """
    prompt = f"""<|im_start|>system
You are an expert compiler and software developer. Convert the following MidleCode DSL script into production-ready {target_language} code. 
Only output the raw source code inside a single markdown code block. Do not add conversational text or explanations.
<|im_end|>
<|im_start|>user
{dsl_code}
<|im_end|>
<|im_start|>assistant
"""
    
    response = llm_instance(
        prompt,
        max_tokens=2048,
        temperature=0.2,
        stop=["<|im_end|>"]
    )
    
    output_text = response["choices"][0]["text"].strip()
    
    # Extract code from markdown blocks if present
    if "```" in output_text:
        lines = output_text.splitlines()
        code_lines = []
        inside_block = False
        for line in lines:
            if line.startswith("```"):
                inside_block = not inside_block
                continue
            if inside_block:
                code_lines.append(line)
        return "\n".join(code_lines)
    
    return output_text