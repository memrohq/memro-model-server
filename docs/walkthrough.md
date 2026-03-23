# AI Coding Agent Walkthrough

I have implemented a production-ready distributed AI system for Acode consisting of a local CPU-based model server and an intelligent agent controller in the Acode plugin.

## Components Built

### 1. Memro Model Server (`memro-model-server`)
- **FastAPI-based API**: Compatible with OpenAI's Chat Completion format.
- **CPU Inference**: Powered by `llama-cpp-python` with `Qwen-2.5-Coder-1.5B-Instruct-GGUF`.
- **Advanced Features**: Supports streaming, optimal thread count, and strict JSON enforcement.

### 2. Acode Agent Controller (`memro-Acode-plugin`)
- **Agent Logic**: Integrated `window.memroAgent` to plan and execute code changes.
- **Precise Range Editing**: Uses line-based edits to ensure stability.
- **Safety Layer**: A Diff Preview UI for user approval before applying changes.
- **Parallel Flow**: Orchestrates Memro recall and editor context gathering concurrently.
- **Memro Integration**: Stores and recalls "Fix Patterns" for intelligent bug resolution.

## How to Test

### Step 1: Start the Model Server (Docker)
1.  Navigate to `memro-model-server/`.
2.  Run `docker-compose up --build -d`.
3.  The server will be available at `http://localhost:8000`.
4.  *(Optional)* Download the model inside the container by running:
    `docker-compose exec model-server python3 download_model.py`

### Step 1 (Alternative): Start the Model Server (Manual)
1.  Navigate to `memro-model-server/`.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Download the model: `python download_model.py`.
4.  Start the server: `python server.py`.

### Step 2: Load the Acode Plugin
1.  In Acode, load the `memro-Acode-plugin` directory.
2.  Open **Memro Agent Settings** (via the floating gear icon).
3.  Configure your **Model Server URL** (e.g., `http://localhost:8000`).
4.  Configure your **Memro MCP Base URL**.

### Step 3: Run the Agent
1.  Open any code file.
2.  Right-click (long-press on mobile) and select **Run Memro Agent**.
3.  Provide a query (e.g., "Fix the async bug" or "Add a hello world function").
4.  Review the **Agent Plan** and **Diff Preview**.
5.  Click **Apply Changes** to execute the edit.

## Verification of Refinements
- ✅ **Streaming**: (Implemented in server.py, ready for plugin UI update in Phase 2).
- ✅ **Precise Range Editing**: Verified in `applyAgentAction` using line-based ranges.
- ✅ **Parallelization**: Implemented in `window.memroAgent.run` using `await memoryPromise`.
- ✅ **Memory Ranking**: Implemented a similarity-based recall through Memro.
- ✅ **Fix Patterns**: Stored as semantic memory after successful edits.
