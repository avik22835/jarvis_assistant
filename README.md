# Jarvis AI Desktop Assistant 🤖

> A local AI assistant that debugs, improves, and understands your codebase using LLMs with memory, vector search, and multi-agent reasoning.

## Features

- Local LLM with Ollama
- Codebase chunking & semantic search
- Memory: static, dynamic, and long-term
- Multi-agent architecture (QnA, Debug, Improve)
- Finetune Agent (on demand)
- Dual vector databases (code + chat summaries)

## Tech Stack

- Python, LangChain, LangGraph
- Ollama (LLaMA / CodeLLaMA)
- Chroma / FAISS vector DB
- PyQt / Streamlit for GUI

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3:instruct
