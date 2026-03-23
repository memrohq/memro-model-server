# Memro Coding Model Server

A production-grade, local CPU-based coding assistant server designed for the Acode mobile editor.

## Features
- **FastAPI-based API**: OpenAI-compatible Chat Completion format.
- **CPU Inference**: Powered by `llama-cpp-python` with `Qwen-2.5-Coder-1.5B-Instruct-GGUF`.
- **Agent Intelligence**: Structured JSON output enforcement for planning and execution.
- **Streaming Support**: Real-time token generation via `StreamingResponse`.
- **Dockerized**: Easy deployment with Docker and Docker Compose.

## Quick Start (Docker)

1.  **Build and Start**:
    ```bash
    docker-compose up --build -d
    ```
2.  **Download Model**:
    ```bash
    docker-compose exec model-server python3 download_model.py
    ```
3.  **Test Connectivity**:
    ```bash
    curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
      "messages": [{"role": "user", "content": "Write a python hello world"}],
      "max_tokens": 50
    }'
    ```

## Manual Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Download Model**:
    ```bash
    python download_model.py
    ```
3.  **Start Server**:
    ```bash
    python server.py
    ```

## Acode Integration

Set the **Model Server URL** in your Acode plugin settings to `http://localhost:8000`.

## Architecture

This server acts as **Server 1** in the Memro Distributed AI System:
- **Client**: Acode Plugin (Agent Controller)
- **Memory**: Memro Server (via MCP)
- **Model**: This Server (Stateless Inference)
