import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { v4 as uuidv4 } from "uuid"; // Import the uuidv4 function

const CMSDataDisplay = () => {
  const { id } = useParams(); // Get `id` from URL
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [score, setScore] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const fetchPostData = async () => {
      try {
        const response = await axios.get(`http://localhost:9001/cmsid/${id}`);
        if (response.data.success) {
          setPost(response.data.post);
        } else {
          setError("Post not found");
        }
      } catch (err) {
        setError("Failed to fetch post: " + err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchPostData();
    }
  }, [id]);

  const handleScoreSubmit = async () => {
    // Validate the score input
    if (!score || isNaN(score)) {
      setError("Please enter a valid score.");
      return;
    }

    try {
      const score_id = uuidv4(); // Generate the unique score_id on the frontend

      const payload = {
        CMS_id: post.CMS_id,
        email: post.email,
        score: parseFloat(score), // Ensure score is a valid number
        score_id, // Include the generated score_id
      };

      console.log("Submitting score with payload:", payload);

      const response = await axios.post(
        "http://localhost:9001/submitmark",
        payload
      );

      if (response.data.success) {
        setSuccessMessage(`Score added successfully! Score ID: ${score_id}`);
        setScore(""); // Clear the score input after success
      } else {
        setError("Failed to add score.");
      }
    } catch (err) {
      setError("Error submitting score: " + err.message);
    }
  };

  return (
    <div>
      <h2>Post ID: {id}</h2>

      {loading && <p>Loading post data...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}

      {post && (
        <div>
          <h3>Email: {post.email}</h3>
          <p>CMS_id: {post.CMS_id}</p>
          <p>Content: {post.content}</p>

          <div style={{ marginTop: "20px" }}>
            <input
              type="number"
              placeholder="Enter score"
              value={score}
              onChange={(e) => setScore(e.target.value)}
            />
            <button onClick={handleScoreSubmit} style={{ marginLeft: "10px" }}>
              Submit Score
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CMSDataDisplay;
