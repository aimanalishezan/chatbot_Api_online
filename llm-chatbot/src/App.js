import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css"; // Importing CSS for styles

function App() {
  const [prompt, setPrompt] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false); // Dark mode state
  const chatContainerRef = useRef(null);

  // Handle sending chat and updating history
  const handleChat = async () => {
    if (!prompt.trim()) return;

    const userMessage = { sender: "user", text: prompt, time: new Date().toLocaleTimeString() };
    setChatHistory((prev) => [...prev, userMessage]); // Add user's message to history
    setPrompt(""); // Reset input box
    setLoading(true); // Show loading state

    try {
      // Send message to backend
      const response = await axios.post("http://localhost:8000/chat", { prompt });
      const botMessage = { sender: "bot", text: response.data.response, time: new Date().toLocaleTimeString() };
      setChatHistory((prev) => [...prev, botMessage]); // Add bot's response to history
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Error: Could not connect to server.", time: new Date().toLocaleTimeString() },
      ]);
    } finally {
      setLoading(false); // Hide loading state
    }
  };

  // Auto-scroll to the latest message
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Handle Enter key to send the chat message
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { // Prevent Enter key from adding a new line
      e.preventDefault();
      handleChat();
    }
  };

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`app-container ${darkMode ? 'dark' : ''}`}>
      <h1 className="app-title">AI Chatbot</h1>

      {/* Dark Mode Toggle Button */}
      <button className="dark-mode-toggle" onClick={toggleDarkMode}>
        {darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
      </button>

      {/* Chat History Section */}
      <div ref={chatContainerRef} className="chat-box">
        {chatHistory.length === 0 ? (
          <p className="placeholder">Start chatting with the AI...</p>
        ) : (
          chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <div className="message-text">
                {msg.sender === "user" ? "🙂" : "🤖"} {/* Add emoji */}
                <span className="text">{msg.text}</span>
              </div>
              <div className="message-time">{msg.time}</div>
            </div>
          ))
        )}
        {loading && <p className="loading">⏳ AI is thinking...</p>}
      </div>

      {/* Input Section */}
      <div className="input-container">
        <textarea
          className="input-box"
          rows="3"
          placeholder="Type your message..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown} // Listen for Enter key
        ></textarea>

        <button className="send-button" onClick={handleChat} disabled={loading}>
          {loading ? "Generating..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
