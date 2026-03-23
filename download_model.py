from huggingface_hub import hf_hub_download
import os

repo_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF"
filename = "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
local_dir = "/Users/freya/Documents/work/hackit/memrohq/memro-model-server/models"

print(f"Downloading {filename} from {repo_id}...")
hf_hub_download(repo_id=repo_id, filename=filename, local_dir=local_dir)
print("Download complete.")
