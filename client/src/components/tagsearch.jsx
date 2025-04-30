import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaLink, FaWhatsapp, FaEnvelope, FaShareAlt } from "react-icons/fa";
import "../css/tags.css";

const categories = [
  "Science",
  "Maths",
  "Video",
  "Tutorial",
  "Learning",
  "Physics",
  "Chemistry",
  "Biology",
  "Computer Science",
  "History",
  "Literature",
  "Geography",
  "Art",
  "Engineering",
  "Psychology",
  "Economics",
  "Philosophy",
  "Music",
  "Languages",
  "Technology",
  "Health",
];

const TagSearch = ({ enrollmentCounts = {} }) => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState("");
  const [shareMenuVisible, setShareMenuVisible] = useState(null);

  const toggleShareMenu = (cardId) => {
    setShareMenuVisible(shareMenuVisible === cardId ? null : cardId);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert("URL copied to clipboard!");
  };

  const handleTagChange = (category) => {
    setSelectedTags((prevState) =>
      prevState.includes(category)
        ? prevState.filter((tag) => tag !== category)
        : [...prevState, category]
    );
  };

  const fetchPosts = async () => {
    if (selectedTags.length === 0) {
      setError("At least one tag is required.");
      return;
    }

    try {
const response = await axios.get("http://localhost:9001/posts/tags/search", {
  params: { tags: selectedTags.join(",") },
});

      if (response.data && Array.isArray(response.data.posts)) {
        setPosts(response.data.posts);
        setError(""); // Reset error if successful
      } else {
        setPosts([]);
        setError("No posts found for the selected tags.");
      }
    // eslint-disable-next-line no-unused-vars
    } catch (error) {
      setError("Error fetching posts. Please try again.");
    }
  };

  useEffect(() => {
    if (selectedTags.length > 0) {
      fetchPosts();
    } else {
      setPosts([]);
    }
  }, [selectedTags]);

  return (
    <div className="tag-search">
      <h3>Select Categories</h3>
      <div className="checkbox-group">
        {categories.map((category) => (
          <div key={category} className="checkbox-item">
            <input
              type="checkbox"
              id={category}
              checked={selectedTags.includes(category)}
              onChange={() => handleTagChange(category)}
            />
            <label htmlFor={category}>{category}</label>
          </div>
        ))}
      </div>

      <div className="selected-tags">
        <h4>Selected Tags:</h4>
        <ul>
          {selectedTags.length > 0 ? (
            selectedTags.map((tag) => <li key={tag}>{tag}</li>)
          ) : (
            <li>No tags selected</li>
          )}
        </ul>
      </div>

      {error && <div className="error">{error}</div>}

      {Array.isArray(posts) && posts.length > 0 ? (
        <div className="card-container">
          {posts.map((post) => (
            <div className="card" key={post.card_id}>
              <a href={`/enrollestudent/${post.card_id}`} className="card-link">
                {shareMenuVisible === post.card_id && (
                  <div className="share-options">
                    <button
                      onClick={() =>
                        copyToClipboard(
                          `${window.location.origin}/teacherweek/${post.card_id}`
                        )
                      }
                      className="share-option"
                    >
                      <FaLink color="white" /> Copy URL
                    </button>
                    <a
                      href={`https://wa.me/?text=Check out this module: ${window.location.origin}/teacherweek/${post.card_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="share-option"
                    >
                      <FaWhatsapp color="white" /> WhatsApp
                    </a>
                    <a
                      href={`mailto:?subject=Check out this module&body=Here is a link to the module: ${window.location.origin}/teacherweek/${post.card_id}`}
                      className="share-option"
                    >
                      <FaEnvelope color="white" /> Email
                    </a>
                  </div>
                )}
                <div className="card-image">
                  <img
                    src={
                      post.image
                        ? `http://localhost:9001/Uploads/${post.image}`
                        : ""
                    }
                    alt={post.image ? post.image : "No Image"}
                  />
                </div>
                <div className="card-header">
                  <h3>{post.title}</h3>
                  <p>{post.summery}</p>
                  <p className="enrollment-count">
                    {enrollmentCounts[post.card_id] !== undefined
                      ? `Enrolled: ${enrollmentCounts[post.card_id]}`
                      : "Enrolled: Loading..."}
                  </p>
                </div>
              </a>
              <div className="share-icon">
                <FaShareAlt
                  color="white"
                  onClick={() => toggleShareMenu(post.card_id)}
                />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-posts">No posts found for the selected tags.</div>
      )}
    </div>
  );
};

export default TagSearch;
