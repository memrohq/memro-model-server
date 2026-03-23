# AI Coding Agent Implementation Plan (Production-Grade)

Build a production-grade AI Coding Agent for Acode that plans, modifies, and fixes code with high precision using a local model server and Memro.

## Proposed Changes

### [NEW] memro-model-server

#### [NEW] [server.py](file:///Users/freya/Documents/work/hackit/memrohq/memro-model-server/server.py)
- **Strict JSON Schema Enforcement**: Use Pydantic or manual validation to ensure the model output matches the `AgentAction` schema.
- **Retry Logic**: Automatically re-prompt the model if the output is malformed or invalid JSON.
- **Optimal Inference**: Support streaming (`StreamingResponse`) and CPU thread optimization.

#### [NEW] [Dockerfile](file:///Users/freya/Documents/work/hackit/memrohq/memro-model-server/Dockerfile)
- Multi-stage build for efficient `llama-cpp-python` installation.
- Expose port 8000.
- Use a volume for the `models` directory to persist GGUF files.

---

### [MODIFY] memro-Acode-plugin

#### [MODIFY] [index.js](file:///Users/freya/Documents/work/hackit/memrohq/memro-Acode-plugin/index.js)
- **Precise Range Editing**:
    - Use `startLine` and `endLine` for all edits to prevent duplicate string matches and broken files.
- **Diff Preview UI**:
    - Implement a colored +/- diff view for user approval of all code changes.
- **Undo System**:
    - Build a state history stack to allow users to roll back changes.
- **File Indexing & Selection**:
    - **Step 1**: Agent selects relevant files (Top 2-5).
    - **Step 2**: Agent reads and plans changes.
    - **Step 3**: Agent executes edits.
- **Memory Ranking**: Implement `score = similarity + recency + frequency` (alpha version).
- **Explain Before Apply**: Show a brief explanation of *why* the changes are being made before the diff is shown.

## Metrics & Verification

### Performance Benchmarks
- **Time to Action**: Goal is < 5s total (Recall < 200ms, Model Response < 4s).
- **Recall Accuracy**: % of correct memory usage in model output.
- **Edit Accuracy**: % of edits that result in valid code (no syntax errors).

### Verification Steps
- **Adversarial Test Suite**: Run prompts with incomplete code, vague instructions, and syntax errors to verify reliability.
- **UI Walkthrough**: Record a session showing:
    1. Fix Pattern used for a bug.
    2. Range-based edit applied through Diff UI.
    3. State undo.
