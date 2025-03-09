import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleChat = async () => {
    const res = await axios.post("http://127.0.0.1:8000/chat", { prompt });
    setResponse(res.data.response);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>AI Chatbot</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows="4"
        cols="50"
        placeholder="Type a message..."
      />
      <br />
      <button onClick={handleChat}>Send</button>
      <h2>Response:</h2>
      <p>{response}</p>
    </div>
  );
}

export default App;
