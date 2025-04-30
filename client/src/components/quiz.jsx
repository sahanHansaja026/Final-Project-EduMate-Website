import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "../css/quiz.css";

const Quiz = () => {
  const { quizId } = useParams(); // Get quizId from URL params
  const navigate = useNavigate();

  const [posts, setPosts] = useState([]); // Quiz questions
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [results, setResults] = useState([]); // Stores correct/incorrect answers
  const [timeDuration, setTimeallocate] = useState(""); // Quiz metadata
  const [answered, setAnswered] = useState(false);
  const [showCorrectAnswer, setShowCorrectAnswer] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0); // Timer countdown state

  // Fetch quiz data
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get(
          `http://localhost:9001/post/card/${quizId}`
        );
        console.log("Quiz Questions:", response.data.posts); // Debugging
        if (response.data.success) {
          setPosts(response.data.posts);
          setResults(new Array(response.data.posts.length).fill(null)); // Initialize results array
        } else {
          setError("Failed to load quiz questions.");
        }
      } catch (err) {
        console.error("Error fetching quiz data:", err);
        setError("Error fetching quiz data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    const fetchQuizDetails = async () => {
      try {
        const response = await axios.get(
          `http://localhost:9001/quiz_details/${quizId}`
        );

        if (response.data.success) {
          const duration = parseInt(response.data.quiz.timeDuration, 10); // Convert string to number
          setTimeallocate(duration); // Set timeDuration in minutes
          setTimeLeft(duration * 60); // Convert minutes to seconds for countdown
        }
      } catch (error) {
        console.error("Error fetching quiz details:", error);
        setError("Error fetching quiz details. Please try again later.");
      } finally {
        setLoading(false);
      }
    };


    // Fetch quiz data and details
    fetchPosts();
    fetchQuizDetails();
  }, [quizId]);
  // Countdown timer logic
  // Countdown timer logic
  useEffect(() => {
    let timer;
    if (timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
    }

    return () => clearInterval(timer); // Cleanup on component unmount
  }, [timeLeft]);

  // Format time in hh:mm:ss
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(
      remainingSeconds
    ).padStart(2, "0")}`;
  };

  // Move to the next question or finish the quiz
  const handleNext = () => {
    if (answered) {
      if (currentIndex < posts.length - 1) {
        setCurrentIndex(currentIndex + 1);
        resetQuestionState();
      } else {
        // Calculate the final score
        const score = results.filter((result) => result === true).length;
        navigate(`/score/${quizId}`, { state: { score, total: posts.length } });
      }
    } else {
      const post = posts[currentIndex];
      const isCorrect = selectedAnswer === post.correct_answer;

      // Update results
      const updatedResults = [...results];
      updatedResults[currentIndex] = isCorrect;
      setResults(updatedResults);

      setAnswered(true);
      setShowCorrectAnswer(true);
    }
  };

  // Move to the previous question
  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      resetQuestionState();
    }
  };

  // Reset question state when moving between questions
  const resetQuestionState = () => {
    setAnswered(false);
    setShowCorrectAnswer(false);
    setSelectedAnswer("");
  };

  const handleAnswerChange = (e) => {
    setSelectedAnswer(e.target.value);
  };

  const handleQuestionClick = (index) => {
    setCurrentIndex(index);
    resetQuestionState();
  };

  if (loading) {
    return <p className="loading">Loading...</p>;
  }

  if (error) {
    return <p className="error">Error: {error}</p>;
  }

  if (posts.length === 0) {
    return <p>No questions found for this quiz ID.</p>;
  }

  const post = posts[currentIndex];

  return (
    <div className="quiz-container">
      <h1 className="quiz-title">Quiz Page</h1>
      <h3 className="quiz-metadata">Time Duration: {timeDuration || "N/A"}</h3>
      <h3 className="quiz-metadata">
        Time Remaining: {formatTime(timeLeft) || "00:00"}
      </h3>

      {/* Question Numbers */}
      <div className="question-numbers">
        {posts.map((_, index) => (
          <button
            key={index}
            className={`question-number ${
              results[index] === true
                ? "correct"
                : results[index] === false
                ? "incorrect"
                : ""
            }`}
            onClick={() => handleQuestionClick(index)}
          >
            {index + 1}
          </button>
        ))}
      </div>

      {/* Current Question */}
      <div className="quiz-question">
        <h2>
          <b>{post.question}</b>
        </h2>
        <div className="quiz-answers">
          {[post.answer_1, post.answer_2, post.answer_3, post.answer_4].map(
            (answer, index) => (
              <label key={index}>
                <input
                  type="radio"
                  name="answer"
                  value={answer}
                  checked={selectedAnswer === answer}
                  onChange={handleAnswerChange}
                  disabled={answered}
                />
                {answer}
              </label>
            )
          )}
        </div>

        {/* Show Correct Answer */}
        {showCorrectAnswer && (
          <p className="correct-answer">
            Correct Answer: {post.correct_answer}
          </p>
        )}
      </div>

      {/* Navigation Buttons */}
      <div className="navigation-buttons">
        <button
          className="previous-button"
          onClick={handlePrevious}
          disabled={currentIndex === 0}
        >
          Previous
        </button>

        <button
          className="next-button"
          onClick={handleNext}
          disabled={!selectedAnswer && !answered}
        >
          {answered
            ? currentIndex === posts.length - 1
              ? "Finish"
              : "Next"
            : "Submit"}
        </button>
      </div>
    </div>
  );
};

export default Quiz;
