from huggingface_hub import hf_hub_download
import os
from dotenv import load_dotenv

# Load .env if exists
load_dotenv()

REPO_ID = os.getenv("REPO_ID", "TheBloke/deepseek-coder-6.7B-instruct-GGUF")
FILENAME = os.getenv("MODEL_FILE", "deepseek-coder-6.7b-instruct.Q4_K_M.gguf")
LOCAL_DIR = os.getenv("LOCAL_DIR", "./models")

def download():
    print(f"🚀 Downloading {FILENAME} from {REPO_ID}...")
    print(f"📁 Target Directory: {os.path.abspath(LOCAL_DIR)}")
    
    try:
        path = hf_hub_download(
            repo_id=REPO_ID, 
            filename=FILENAME, 
            local_dir=LOCAL_DIR,
            local_dir_use_symlinks=False
        )
        print(f"✅ Download complete: {path}")
    except Exception as e:
        print(f"❌ Error downloading model: {e}")

if __name__ == "__main__":
    download()
