import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

def load_gguf_model():
    # Set target directory relative to this project
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    print("Checking for model file...")
    model_path = hf_hub_download(
        repo_id="Qwen/Qwen2.5-Coder-3B-Instruct-GGUF",
        filename="qwen2.5-coder-3b-instruct-q4_k_m.gguf",
        local_dir=models_dir
    )

    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        verbose=False
    )
    return llm