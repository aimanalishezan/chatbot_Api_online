import os
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import login
from fastapi.middleware.cors import CORSMiddleware

# Use the environment variable for the Hugging Face token securely
# Log in using the HF_TOKEN secret automatically
hf_token = os.getenv("Tk")  # Get the token from Hugging Face Space secrets

if not hf_token:
    raise ValueError("HF_TOKEN secret not found. Please set the Hugging Face API token in your Space secrets.")
# Force Hugging Face Transformers to use a custom cache directory

custom_cache = "/app/cache"
os.makedirs(custom_cache, exist_ok=True)  # Ensure directory exists
os.environ["TRANSFORMERS_CACHE"] = custom_cache
app = FastAPI()

# Middleware to allow CORS from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-react-app.vercel.app"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Ensure that the device is set correctly (GPU/CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model with device allocation
model_name = "meta-llama/Llama-3.2-1B-Instruct"
model = None
tokenizer = None

try:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",  # Distributes across CPU/GPU
        trust_remote_code=True,
        cache_dir=custom_cache,
        token=hf_token
    ).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, cache_dir=custom_cache,token=hf_token)
    print(" Model Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")

class RequestData(BaseModel):
    prompt: str

# Initialize conversation history globally (could be improved with user sessions)
chat_history = []
@app.get("/")
def home():
    return {"message": "FastAPI is running! Visit /docs to test."}
@app.post("/chat")
def chat(request: RequestData):
    global chat_history
    
    if model is None or tokenizer is None:
        return {"error": "Model failed to load. Check logs."}

    # Add the user's prompt to the history
    user_message = {"role": "user", "content": request.prompt}
    chat_history.append(user_message)
    
    # Tokenize the prompt
    inputs = tokenizer(request.prompt, return_tensors="pt")

    # Move input tensors to the correct device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    try:
        # Generate a response from the model
        output = model.generate(**inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
        response_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Add the AI's response to the history
        bot_message = {"role": "bot", "content": response_text}
        chat_history.append(bot_message)

        return {"response": response_text}
    except Exception as e:
        return {"error": f"Error during model generation: {e}"}