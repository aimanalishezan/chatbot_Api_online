from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import login

# Use your Hugging Face token here
login(token="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")

app = FastAPI()

# Load model with optimization
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
model, tokenizer = None, None  # Initialize to None in case of error

try:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, 
        device_map="auto",  # Distributes across CPU/GPU
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    print("✅ Model Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")

class RequestData(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: RequestData):
    if model is None or tokenizer is None:
        return {"error": "Model failed to load. Check logs."}

    # Tokenize the prompt
    inputs = tokenizer(request.prompt, return_tensors="pt")

    # Move input tensors to GPU if available
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    try:
        # Generate a response from the model
        output = model.generate(**inputs, max_length=100)
        response_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return {"response": response_text}
    except Exception as e:
        return {"error": f"Error during model generation: {e}"}
