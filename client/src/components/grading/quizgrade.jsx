/* eslint-disable react-hooks/rules-of-hooks */
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "../../css/curd.css";

const ShowQuizScore = () => {
  const { quiz_id } = useParams();
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScores = async () => {
      try {
        const response = await axios.get(
          `http://localhost:9001/score/quiz/${quiz_id}`
        );
        setScores(response.data);
      } catch (error) {
        console.error("Fetch error:", error);
        setError("Failed to fetch scores");
      } finally {
        setLoading(false);
      }
    };

    fetchScores();
  }, [quiz_id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="curd">
      <center>
        <h1>Quiz Score Board</h1>
        <h3>Quiz ID: {quiz_id}</h3>
      </center>
      {scores.length === 0 ? (
        <p>No scores found for this quiz.</p>
      ) : (
        <center>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Username</th>
                <th>Email</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {scores.map((score, index) => (
                <tr key={score._id}>
                  <td>{index + 1}</td>
                  <td>{score.username}</td>
                  <td>{score.email}</td>
                  <td>{score.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </center>
      )}
    </div>
  );
};

export default ShowQuizScore;
