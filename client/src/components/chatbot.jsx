import React from "react";
import "../css/chatbot.css";

const ChatbotPopup = ({ visible, closeChat }) => {
  if (!visible) return null;

  return (
    <div className="chatbot-popup">
      <div className="chatbot-header">
        <h2>Chatbot</h2>
        <button onClick={closeChat} className="close-button">
          ✖
        </button>
      </div>
      <div className="chatbot-body">
        <p>Hello! How can I help you?</p>
      </div>
      <div className="chatbot-input">
        <input type="text" placeholder="Type your message..." />
      </div>
    </div>
  );
};

export default ChatbotPopup;
