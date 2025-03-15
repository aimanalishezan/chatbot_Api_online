import os
import torch
import fitz  # PyMuPDF for PDF processing
import psycopg2  # PostgreSQL connection
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Variables
hf_token = os.getenv("HF_TOKEN")
db_url = os.getenv("DATABASE_URL")  # PostgreSQL URL
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Load Model & Tokenizer
model_name = "meta-llama/Llama-3.2-1B-Instruct"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Load Embedding Model for RAG
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("llm-data-index")

# Database Connection
def get_db_connection():
    return psycopg2.connect(db_url)

class QueryRequest(BaseModel):
    prompt: str

# Extract text from PDF
async def extract_text_from_pdf(pdf_file: UploadFile):
    doc = fitz.open(stream=await pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Retrieve relevant data from database using Pinecone
def search_database(query: str):
    query_embedding = embed_model.encode(query).tolist()
    results = index.query(query_embedding, top_k=3, include_metadata=True)
    return [match["metadata"]["text"] for match in results.matches]

@app.post("/chat")
async def chat(request: QueryRequest):
    user_query = request.prompt
    retrieved_data = search_database(user_query)
    
    if retrieved_data:
        context = " ".join(retrieved_data)
    else:
        context = ""
    
    inputs = tokenizer(f"Context: {context} Query: {user_query}", return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=150)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return {"response": response_text}

@app.post("/upload_pdf")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    extracted_text = await extract_text_from_pdf(pdf_file)
    vector = embed_model.encode(extracted_text).tolist()
    index.upsert([(pdf_file.filename, vector, {"text": extracted_text})])
    return {"message": "PDF content indexed successfully"}

@app.get("/")
def home():
    return {"message": "LLM API is running!"}
