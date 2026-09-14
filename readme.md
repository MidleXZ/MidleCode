# MidleCode Studio

MidleCode Studio is a lightweight, cross-platform Python IDE designed to convert custom `.midlecode` DSL scripts into executable code across multiple target programming languages using a local LLM (`Qwen2.5-Coder`).

## Features
- **Multi-Language Conversion**: Compiles `.midlecode` DSL scripts into **Python (.py)**, **JavaScript (.js)**, **C (.c)**, **C++ (.cpp)**, **Rust (.rs)**, **TypeScript (.ts)**, or **R (.r)**.
- **Local AI Inference**: Generates clean source code locally using `llama-cpp-python` without requiring API keys.
- **Cross-Platform Launchers**: Automated setup and startup scripts (`run.sh` / `run.bat`) for macOS, Linux, and Windows.
- **Built-in File Explorer**: Full file management (create, rename, delete files and folders) integrated into the IDE sidebar.
- **Auto Model Fetching**: Downloads the default GGUF model directly from Hugging Face on the first run.

---

## Quick Start

### macOS / Linux

1. **Install System Dependencies** (Ubuntu/Debian):
   ```bash
   sudo apt update && sudo apt install python3-tk -y