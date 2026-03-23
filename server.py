import os
import json
from typing import List, Optional, Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from llama_cpp import Llama
import uvicorn

app = FastAPI(title="Memro Coding Model Server")

# Enable AGGRESSIVE CORS (Final Resort)
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    if request.method == "OPTIONS":
        response = StreamingResponse(iter(["OK"]), status_code=200)
    else:
        response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

# Model Configuration
MODEL_PATH = "/app/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
N_CTX = 4096
N_THREADS = 4  # Optimized for M-series Performance Cores

# Initialize Llama (Lazy load)
llm = None

def get_llm():
    global llm
    if llm is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=500, detail="Model file not found. Run download_model.py first.")
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            n_batch=512,
            verbose=False
        )
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
    
    prompt = ""
    for msg in request.messages:
        prompt += f"<|im_start|>{msg.role}\n{msg.content}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"

    if request.stream:
        def stream_generator():
            output = instance(
                prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                stop=request.stop or ["<|im_end|>"],
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
            stop=request.stop or ["<|im_end|>"]
        )
        return {
            "id": "memro-agent-cb",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": output['choices'][0]['text']
                }
            }]
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
