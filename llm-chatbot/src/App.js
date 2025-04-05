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

    const userMessage = { sender: "user", text: prompt };
    setChatHistory((prev) => [...prev, userMessage]); // Add user's message to history
    setPrompt(""); // Reset input box
    setLoading(true); // Show loading state

    try {
      // Send message to backend
      const response = await axios.post("https://AI-man999-FastAPiWithdocker.hf.space/chat", { prompt });

      const botMessage = { sender: "bot", text: response.data.response };
      setChatHistory((prev) => [...prev, botMessage]); // Add bot's response to history
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Error: Could not connect to server." },
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

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode((prevMode) => !prevMode);
  };

  return (
    <div className={`app-container ${darkMode ? "dark" : ""}`}>
      {/* Navbar */}
      <div className={`navbar ${darkMode ? "dark" : ""}`}>
        <div className="navbar-title">AI_MAN.Ai</div>
        <button className="dark-mode-toggle" onClick={toggleDarkMode}>
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>

      {/* Chat History Section */}
      <div ref={chatContainerRef} className={`chat-box ${darkMode ? "dark" : ""}`}>
        {chatHistory.length === 0 ? (
          <p className="placeholder">Start chatting with the AI...</p>
        ) : (
          chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <span className="message-text">{msg.text}</span>
              <span className="message-time">
                {new Date().toLocaleTimeString()}
              </span>
            </div>
          ))
        )}
        {loading && <p className="loading">⏳ Response Generating...</p>}
      </div>

      {/* Input Section */}
      <div className="input-container">
        <textarea
          className="input-box"
          rows="3"
          placeholder="Type your message..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleChat();
            }
          }}
        ></textarea>

        <button className="send-button" onClick={handleChat} disabled={loading}>
          {loading ? "Generating..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
