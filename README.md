# 🤖 AI_MAN.Ai - Full Stack AI Chatbot (FastAPI + React)

Welcome to **AI_MAN.Ai**, your very own intelligent chatbot!  
Built with a powerful FastAPI backend and a sleek React frontend, this AI assistant lets you chat in real time with a language model — styled with modern design and dark mode support.

![AI_MAN.Ai Banner](https://img.shields.io/badge/Built%20With-FastAPI%20%2B%20React-4caf50?style=for-the-badge&logo=react)

---

## 📌 Features

- 🌐 **FastAPI Backend** — handles chat logic and communicates with the AI model.
- 💬 **Interactive React Frontend** — modern UI with message history, scroll, and auto-response.
- 🌗 **Dark Mode Toggle** — seamless switch between light and dark themes.
- 📱 **Responsive Design** — works great on mobile and desktop.
- ⚙️ **Docker Deployment-Ready** — easily deploy using Docker or on Hugging Face Spaces.
- 📡 **API Integrated** — connects with your hosted LLM backend (like Hugging Face Spaces).

---

## 🧠 Technologies Used

| Frontend         | Backend       | Styling       |
|------------------|---------------|----------------|
| React (Vite)     | FastAPI       | Pure CSS       |
| Axios            | Uvicorn       | Flexbox Layout |
| useRef + Hooks   | Pydantic      | Dark Mode      |

---

## 🚀 Live Demo

Check out the deployed version:  
**[AI_MAN.Ai on Hugging Face Spaces](your space link)**

---

## 🛠️ Project Structure
📁 project-root/ ├── backend/ │ └── app.py # FastAPI server ├── frontend/ │ ├── App.js # React frontend logic │ ├── App.css # Styling │ └── index.html # (Optional Vite entry) ├── README.md

---

## ⚙️ Setup Instructions

### 🖥️ Backend (FastAPI)

1. **Create virtual environment & install dependencies:**

```bash

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install fastapi uvicorn openai
Run the server locally:

bash
Copy
Edit
uvicorn app:app --reload
Your backend will be available at: http://127.0.0.1:8000

You can test it at: http://127.0.0.1:8000/docs

Note: Replace the OpenAI API call with your own model/backend if not using OpenAI.
🌐 Frontend (React)
Install dependencies:

bash
Copy
Edit
cd frontend
npm install
Start the React app:

bash
Copy
Edit
npm run dev
Update Backend URL in App.js:

js
Copy
Edit
const response = await axios.post("http://127.0.0.1:8000/chat", { prompt });
Change to your deployed backend (e.g., Hugging Face Spaces) if needed.

🎨 UI Preview
Light Mode	Dark Mode
📦 Deployment
🌍 Hugging Face Spaces
Use the following structure:

bash
Copy
Edit
/app.py  ➜ Backend
/requirements.txt ➜ Add FastAPI, Uvicorn, OpenAI
🐳 Docker (Optional)
dockerfile
Copy
Edit
# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app
RUN pip install openai
📄 License
This project is open-source under the MIT License.

🙌 Acknowledgements
Inspired by OpenAI’s GPT-3 playground

Powered by FastAPI and React.js

Styled with 💚 Material-inspired CSS

👨‍💻 Author
Developed by Aiman Ali Shezan
Always open for feedback, contributions, or collaboration!
