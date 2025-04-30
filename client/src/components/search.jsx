import React, { useState} from "react";
import axios from "axios";
import { FaShareAlt, FaWhatsapp, FaEnvelope, FaLink } from "react-icons/fa";
import "../css/search.css";

const Search = () => {
  const [posts, setPosts] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [shareMenuVisible, setShareMenuVisible] = useState(null);
  const [enrollmentCounts, setEnrollmentCounts] = useState({}); // State for enrollment counts

  const handleSearchChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);

    if (query.length > 0) {
      axios
        .post("http://localhost:9001/search", { title: query })
        .then((res) => {
          if (res.data.success) {
            setPosts(res.data.existingPosts);
            setErrorMessage("");
            fetchEnrollmentCounts(res.data.existingPosts); // Fetch enrollment counts when posts are available
          } else {
            setErrorMessage(res.data.error);
            setPosts([]);
          }
        })
        .catch((error) => {
          console.error("Error searching for module or card:", error);
          setPosts([]);
        });
    } else {
      setPosts([]);
      setErrorMessage("");
    }
  };

  const fetchEnrollmentCounts = (posts) => {
    posts.forEach((post) => {
      axios
        .get(`http://localhost:9001/enrollment-count/${post.card_id}`) // Fetch count from the backend
        .then((res) => {
          if (res.data.card_id) {
            setEnrollmentCounts((prevCounts) => ({
              ...prevCounts,
              [post.card_id]: res.data.enrollmentCount, // Store the count by card_id
            }));
          }
        })
        .catch((error) => {
          console.error("Error fetching enrollment count:", error);
        });
    });
  };

  const toggleShareMenu = (cardId) => {
    setShareMenuVisible((prevId) => (prevId === cardId ? null : cardId));
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert("Link copied to clipboard!");
  };

  return (
    <div className="search">
      <div className="main">
        {/* Search Bar */}
        <form className="search-form">
          <input
            type="text"
            placeholder="Search Subject or Module Name..."
            value={searchQuery}
            onChange={handleSearchChange}
          />
        </form>

        {/* Display error message if search fails */}
        {errorMessage && <div className="error">{errorMessage}</div>}

        {/* Display the searched modules details */}
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
                  {/* Display the enrollment count */}
                  <p className="enrollment-count">
                    {enrollmentCounts[post.card_id] !== undefined
                      ? `Enrolled: ${enrollmentCounts[post.card_id]}`
                      : "Enrolled: Loading..."}
                  </p>
                </div>
              </a>

              {/* Share Icon */}
              <div className="share-icon">
                <FaShareAlt
                  color="white"
                  onClick={() => toggleShareMenu(post.card_id)}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Search;
