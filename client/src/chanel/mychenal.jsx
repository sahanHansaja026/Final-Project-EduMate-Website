import React, { useState, useEffect } from "react";
import authService from "../services/authService";
import axios from "axios";
import { FaShareAlt, FaWhatsapp, FaEnvelope, FaLink } from "react-icons/fa";
import "../css/mychanel.css";

const MyModule = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [shareMenuVisible, setShareMenuVisible] = useState(null); // Track which post’s share menu is open

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userData = await authService.getUserData();
        setUsername(userData.username);

        setEmail(userData.email);
        const response = await axios.get(
          `http://localhost:9001/ch/${userData.email}?page=${currentPage}&limit=1`
        );
        setPosts(response.data.existingPosts);
        setTotalPages(response.data.totalPages);

        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch data", error);
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage]);

  const truncateSummary = (text, length) => {
    return text.length > length ? text.substring(0, length) + "..." : text;
  };
  useEffect(() => {
    if (username) {
      console.log("Logged in Username:", username);
    }
  }, [username]);
  useEffect(() => {
    if (username) {
      console.log("Logged in Username:", username);
    }
  }, [email]);
  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const toggleShareMenu = (postId) => {
    setShareMenuVisible((prevId) => (prevId === postId ? null : postId));
  };

  const copyToClipboard = (url) => {
    navigator.clipboard.writeText(url);
    alert("Link copied to clipboard!");
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="mychanel">
      <div className="card-container1">
        {posts
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .map((post) => (
            <div className="card" key={post.chenal_id}>
              <a href={`/chenalhome/${post._id}`} className="card-link">
                <div className="card-image">
                  <img
                    src={post.image ? post.image : ""}
                    alt={post.image ? post.image : "No Image"}
                  />
                </div>
                <div className="card-header">
                  <h3>{post.title}</h3>
                  <p>{truncateSummary(post.summery, 100)}</p>
                </div>
              </a>

              {/* Share Icon */}
              <div className="share-icon">
                <FaShareAlt
                  color="white"
                  onClick={() => toggleShareMenu(post.chenal_id)}
                />
              </div>

              {/* Share Menu */}
              {shareMenuVisible === post.chenal_id && (
                <div className="share-options">
                  <button
                    onClick={() =>
                      copyToClipboard(
                        `${window.location.origin}/teacherweek/${post.chenal_id}`
                      )
                    }
                    className="share-option"
                  >
                    <FaLink color="white" /> URL
                  </button>
                  <a
                    href={`https://wa.me/?text=Check out this module: ${window.location.origin}/teacherweek/${post.chenal_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="share-option"
                  >
                    <FaWhatsapp color="white" /> WhatsApp
                  </a>
                  <a
                    href={`mailto:?subject=Check out this module&body=Here is a link to the module: ${window.location.origin}/teacherweek/${post.chenal_id}`}
                    className="share-option"
                  >
                    <FaEnvelope color="white" /> Email
                  </a>
                </div>
              )}
            </div>
          ))}
      </div>

      {/* Pagination Controls */}
      <div className="pagination">
        <button
          disabled={currentPage === 1}
          onClick={() => handlePageChange(currentPage - 1)}
        >
          Previous
        </button>
        {[...Array(totalPages).keys()].map((page) => (
          <button
            key={page + 1}
            className={currentPage === page + 1 ? "active" : ""}
            onClick={() => handlePageChange(page + 1)}
          >
            {page + 1}
          </button>
        ))}
        <button
          disabled={currentPage === totalPages}
          onClick={() => handlePageChange(currentPage + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default MyModule;
