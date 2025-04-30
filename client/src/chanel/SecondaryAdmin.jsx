import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { FaShareAlt, FaWhatsapp, FaEnvelope, FaLink } from "react-icons/fa";
import "../css/my_enrollement.css";
import authService from "../services/authService";

const ModuleView = () => {
  const { id } = useParams(); // This is where the channel ID comes from
  const [posts, setPosts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const postsPerPage = 3;
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [shareMenuVisible, setShareMenuVisible] = useState(null);
  const [searchTerm, setSearchTerm] = useState(""); // New state for search input

  useEffect(() => {
    retrievePosts();
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const userData = await authService.getUserData();
      setUsername(userData.username);
      setEmail(userData.email);
    } catch (error) {
      console.error("Failed to fetch user data", error);
    }
  };

 const retrievePosts = (page = 1) => {
   axios
     .get(
       `http://localhost:9001/chenalpost/${id}?page=${page}&limit=${postsPerPage}`
     )
     .then((res) => {
       if (res.data.success) {
         setPosts(res.data.post ? [res.data.post] : []); // Only use the first post from response
         setCurrentPage(page);
         setTotalPages(Math.ceil(res.data.totalPosts / postsPerPage)); // Ensure you handle pagination if needed
       } else {
         console.error("Error fetching posts:", res.data.error);
       }
     })
     .catch((error) => {
       console.error("Error fetching posts:", error);
     });
 };


  const toggleShareMenu = (cardId) => {
    setShareMenuVisible(shareMenuVisible === cardId ? null : cardId);
  };

  useEffect(() => {
    if (username) {
      console.log("Logged in Username:", username);
    }
  }, [username]);

  useEffect(() => {
    if (email) {
      console.log("Logged in Username:", username);
    }
  }, [email]);

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert("Link copied to clipboard!");
  };

  const renderPagination = () => {
    const pages = [];
    const maxVisiblePages = 3;

    if (currentPage > 1) {
      pages.push(
        <button
          key={1}
          className={`pagination-button ${1 === currentPage ? "active" : ""}`}
          onClick={() => retrievePosts(1)}
        >
          1
        </button>
      );
    }

    if (currentPage > maxVisiblePages + 1) {
      pages.push(<span key="left-ellipsis">...</span>);
    }

    for (
      let i = Math.max(2, currentPage - maxVisiblePages);
      i <= Math.min(totalPages - 1, currentPage + maxVisiblePages);
      i++
    ) {
      pages.push(
        <button
          key={i}
          className={`pagination-button ${i === currentPage ? "active" : ""}`}
          onClick={() => retrievePosts(i)}
        >
          {i}
        </button>
      );
    }

    if (currentPage < totalPages - maxVisiblePages) {
      pages.push(<span key="right-ellipsis">...</span>);
    }

    if (totalPages > 1) {
      pages.push(
        <button
          key={totalPages}
          className={`pagination-button ${
            totalPages === currentPage ? "active" : ""
          }`}
          onClick={() => retrievePosts(totalPages)}
        >
          {totalPages}
        </button>
      );
    }

    return (
      <div className="pagination">
        {currentPage > 1 && (
          <button onClick={() => retrievePosts(currentPage - 1)}>
            Previous
          </button>
        )}
        {pages}
        {currentPage < totalPages && (
          <button onClick={() => retrievePosts(currentPage + 1)}>Next</button>
        )}
      </div>
    );
  };

  const truncateSummary = (summary, maxLength = 100) => {
    if (summary.length > maxLength) {
      return `${summary.substring(0, maxLength)}...`;
    }
    return summary;
  };

  return (
    <div className="enrolle">
      {/* Search Bar with Channel ID */}
      <div className="search-bar">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder={`Search for channel ID: ${id}`} // Displaying the channel ID in the placeholder
        />
      </div>

      <div className="cards-container">
        {posts
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .map((post) => (
            <div className="cards flex" key={post.card_id}>
              <a
                href={`/chenalenrollement/${post.card_id}`}
                className="textlink"
              >
                {shareMenuVisible === post.card_id && (
                  <div className="share-options">
                    <button
                      onClick={() =>
                        copyToClipboard(
                          `${window.location.origin}/chenalenrollement/${post.card_id}`
                        )
                      }
                      className="share-option"
                    >
                      <FaLink color="white" /> URL
                    </button>
                    <a
                      href={`https://wa.me/?text=Check out this module: ${window.location.origin}/enrollestudent/${post.card_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="share-option"
                    >
                      <FaWhatsapp color="white" /> WhatsApp
                    </a>
                    <a
                      href={`mailto:?subject=Check out this module&body=Here is a link to the module: ${window.location.origin}/enrollestudent/${post.card_id}`}
                      className="share-option"
                    >
                      <FaEnvelope color="white" /> Email
                    </a>
                  </div>
                )}
                <div className="cards-image">
                  <img
                    src={post.image} // Base64 string
                    alt="Post"
                  />
                </div>
                <div className="cards-content flex-col">
                  <h3>{post.title}</h3>
                  <p>{truncateSummary(post.summery, 100)}</p>
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
      {renderPagination()}
    </div>
  );
};

export default ModuleView;
