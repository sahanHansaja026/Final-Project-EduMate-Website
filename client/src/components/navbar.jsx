import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import authService from "../services/authService";
import axios from "axios";
import "../css/navbar.css";
import chatbot from "/src/images/chatbot.gif";
import ChatbotPopup from "./chatbot"; // Import the chatbot popup

function Navbar() {
  const [user, setUser] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [showChatbot, setShowChatbot] = useState(false); // Visibility state

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await authService.getUserData();
        setUser(userData);
        if (userData && userData.email) {
          fetchUserProfile(userData.email);
        } else {
          setUserProfile(null);
        }
      } catch (error) {
        console.error("Failed to fetch user data", error);
        setUserProfile(null);
      }
    };

    fetchUserData();
  }, []);

  const fetchUserProfile = async (email) => {
    try {
      const response = await axios.get(
        `http://localhost:9001/profiles?email=${email}`
      );
      if (response.data.success && response.data.userProfile) {
        setUserProfile(response.data.userProfile);
      } else {
        setUserProfile(null);
      }
    } catch (error) {
      console.error("Failed to fetch user profile:", error);
      setUserProfile(null);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        {user && (
          <div className="user-info">
            <div className="user-profile">
              <Link to="/Profile">
                <img
                  src={
                    userProfile?.profileimage?.trim()
                      ? userProfile.profileimage
                      : "../images/default.png"
                  }
                  alt="Profile"
                  className="profile-image"
                />
              </Link>
              <br />
            </div>
          </div>
        )}
        <div className="navbar-links">
          {user ? (
            <>
              <Link to="/home">Home</Link>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/about">About Us</Link>
              <Link to="/">Logout</Link>
              {/* Chatbot trigger */}
              <button
                onClick={() => setShowChatbot(true)}
                className="chatbotes-button"
              >
                <img src={chatbot} alt="Chatbot" />
              </button>
            </>
          ) : (
            <>
              <Link to="/">Login</Link>
              <Link to="/register">Signup</Link>
            </>
          )}
        </div>
      </div>

      {/* Conditionally render the chatbot popup */}
      <ChatbotPopup
        visible={showChatbot}
        closeChat={() => setShowChatbot(false)}
      />
    </nav>
  );
}

export default Navbar;
