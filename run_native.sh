#!/bin/bash
# Memro AI - Native macOS (Metal) Accelerator
# This script runs the model server natively on your Mac for 7x faster speed.

echo "🚀 Memro AI: Starting Native Accelerator..."

# 1. Setup Python Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# 2. Install dependencies with METAL support
echo "🛠️ Installing optimized llama-cpp-python (Metal)..."
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python==0.2.90
pip install fastapi uvicorn pydantic python-dotenv

# 3. Create models directory if missing
mkdir -p models

# 4. Check for model file
MODEL_FILE="models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
if [ ! -f "$MODEL_FILE" ]; then
    echo "⚠️ Model file not found at $MODEL_FILE"
    echo "Please copy it from the Docker volume or run download_model.py natively."
fi

# 5. Run Server
echo "🔥 Running Native Server on port 8001..."
# We use port 8001 directly to match our ADB tunnel
MODEL_PATH=$MODEL_FILE uvicorn server:app --host 0.0.0.0 --port 8001
