import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";
import "../css/createquiz.css"; // Assuming this is where the CSS file is saved

const Create_quiz = ({ setCardId }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [quizId, setQuizId] = useState("");
  const [quizName, setQuizName] = useState("");
  const [description, setDescription] = useState("");
  const [attempt,setAttempt]=useState("");
  const [timeDuration,setTimeDuration]=useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (setCardId) {
      setCardId(id);
    }
    const newQuizId = uuidv4();
    setQuizId(newQuizId);
  }, [id, setCardId]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const quizData = {
      card_id: id,
      quiz_id: quizId,
      quiz_name: quizName,
      attempt:attempt,
      timeDuration:timeDuration,
      description: description,
    };

    try {
      const response = await axios.post(
        "http://localhost:9001/quiz/save",
        quizData
      );
      if (response.status === 200) {
        navigate(`/create/${quizId}`);
      }
    } catch (error) {
      if (error.response && error.response.data) {
        setMessage(error.response.data.error);
      } else {
        setMessage("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="quiz">
      <div className="container">
        <h1>Create Quiz</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Quiz Name</label>
            <input
              type="text"
              value={quizName}
              onChange={(e) => setQuizName(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Attempt</label>
            <input
              type="number"
              value={attempt}
              onChange={(e) => setAttempt(e.target.value)}
              required
            />
          </div>
          <div>
            <label>timeDuration</label>
            <input
              type="time"
              value={timeDuration}
              onChange={(e) => setTimeDuration(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <button type="submit">Create Quiz</button>
        </form>

        {message && (
          <p className={message.includes("successfully") ? "success" : "error"}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default Create_quiz;
