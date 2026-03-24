# Build stage
FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install llama-cpp-python with CPU optimizations (AVX2/FMA)
RUN CMAKE_ARGS="-DLLAMA_AVX=ON -DLLAMA_AVX2=ON -DLLAMA_F16C=ON -DLLAMA_FMA=ON" pip install --user llama-cpp-python==0.2.90
RUN pip install --user fastapi uvicorn huggingface-hub pydantic python-dotenv

# Final stage
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY server.py .
COPY download_model.py .

ENV PATH=/root/.local/bin:$PATH
# Default path for the 6.7B model
ENV MODEL_PATH=/app/models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf

VOLUME /app/models
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
