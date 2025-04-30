import React, { useState, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import authService from "../services/authService";
import axios from 'axios';
import "../css/score.css";

const ScorePage = () => {
  const { quizId: quizIdFromParams } = useParams(); // Get quiz_id from the URL
  const { state } = useLocation(); // Get the state passed from the Quiz component
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [isScoreSaved, setIsScoreSaved] = useState(false); // Track if score has been saved

  const score = state?.score || 0; // Default to 0 if no score is passed
  const total = state?.total || 0;
  const quizId = state?.quizId || quizIdFromParams; // Use state quizId or fallback to URL param

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await authService.getUserData();
        setUsername(userData.username);
        setEmail(userData.email);

        // Save score data only if it hasn't been saved yet
        if (!isScoreSaved) {
          await saveScoreData(quizId, score, userData.username, userData.email);
          setIsScoreSaved(true); // Mark score as saved
        }
      } catch (error) {
        console.error("Failed to fetch user data", error);
      }
    };

    fetchUserData();
  }, [quizId, score, isScoreSaved]); // Add isScoreSaved to dependencies

  const saveScoreData = async (quizId, score, username, email) => {
    try {
      const response = await axios.post("http://localhost:9001/score/save", {
        quizId,
        score,
        username,
        email,
      });
      console.log(response.data.message);
    } catch (error) {
      console.error("Failed to save score data", error);
    }
  };

  return (
    <div className="score-page">
      <div className="score-card">
        <h2>Quiz Completed!</h2>
        <p className="score">Your Score: {score} / {total}</p>
      </div>
    </div>
  );
};

export default ScorePage;
