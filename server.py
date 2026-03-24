import os
import json
from typing import List, Optional, Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from llama_cpp import Llama
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Memro AI v2 Model Server")

# Standard CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Configuration from Env
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf")
N_CTX = int(os.getenv("N_CTX", "4096"))
N_THREADS = int(os.getenv("N_THREADS", "4"))
N_BATCH = int(os.getenv("N_BATCH", "512"))

# Initialize Llama (Lazy load)
llm = None

def get_llm():
    global llm
    if llm is None:
        if not os.path.exists(MODEL_PATH):
            print(f"❌ Model not found at {MODEL_PATH}")
            raise HTTPException(status_code=500, detail="Model file not found. Run download_model.py first.")
        
        print(f"🚀 Loading model: {MODEL_PATH}")
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            n_batch=N_BATCH,
            verbose=False
        )
        print("✅ Model loaded successfully.")
    return llm

# OpenAI-compatible schemas
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.2
    top_p: float = 0.9
    max_tokens: int = 512
    stream: bool = False
    stop: Optional[Union[str, List[str]]] = None

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    instance = get_llm()
    
    # Construct DeepSeek-Coder Instruct Template
    # Format:
    # ### Instruction:
    # {system_message}
    # {user_message}
    # ### Response:
    
    prompt = ""
    for msg in request.messages:
        if msg.role == "system":
            prompt += f"### Instruction:\n{msg.content}\n"
        elif msg.role == "user":
            if "### Instruction:" not in prompt:
                 prompt += "### Instruction:\n"
            prompt += f"{msg.content}\n"
        elif msg.role == "assistant":
            prompt += f"### Response:\n{msg.content}\n"
    
    if not prompt.endswith("### Response:\n"):
        prompt += "### Response:\n"

    stop_tokens = request.stop or ["### Instruction:", "User:", "<|EOT|>", "###"]

    if request.stream:
        def stream_generator():
            output = instance(
                prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                stop=stop_tokens,
                stream=True
            )
            for chunk in output:
                delta = chunk['choices'][0]['text']
                data = {
                    "choices": [{"delta": {"content": delta}}]
                }
                yield f"data: {json.dumps(data)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    else:
        output = instance(
            prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            stop=stop_tokens
        )
        return {
            "id": "memro-agent-ds",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": output['choices'][0]['text']
                }
            }]
        }

@app.get("/health")
async def health():
    return {"status": "healthy", "model": MODEL_PATH}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
