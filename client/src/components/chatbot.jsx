/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import axios from "axios";
import "../css/chatbot.css";

const ChatbotPopup = ({ visible, closeChat }) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I help you?" },
  ]);

  if (!visible) return null;

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: input,
      });
      setMessages((prev) => [...prev, { sender: "bot", text: res.data.reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, the chatbot service is unavailable." },
      ]);
    }
  };

  return (
    <div className="chatbot-popup">
      <div className="chatbot-header">
        <h2>Chatbot</h2>
        <button onClick={closeChat} className="close-button">
          ✖
        </button>
      </div>
      <div className="chatbot-body">
        {messages.map((msg, i) => (
          <p key={i} className={msg.sender}>
            {msg.text}
          </p>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatbotPopup;
