# MidleCode Studio

MidleCode Studio is a lightweight, cross-platform Python IDE designed to convert custom DSL scripts into executable Python apps using a local LLM (`Qwen2.5-Coder`). 

## Features
- **Local AI Conversion**: Converts `.midlecode` files into standalone CustomTkinter apps.
- **Cross-Platform Support**: Automated startup scripts for Windows, macOS, and Linux.
- **Built-in File Explorer**: Easily manage files, folders, and project structures.
- **Auto Model Fetching**: Downloads the local model directly from Hugging Face on first run.

---

## Quick Start

### macOS / Linux

1. **Prerequisite**: Ensure system Tkinter is installed:
   ```bash
   sudo apt update && sudo apt install python3-tk -y