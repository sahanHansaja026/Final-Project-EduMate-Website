import React, { Component } from "react";
import axios from "axios";
import "../css/home.css"; // Make sure the CSS is correctly linked
import { Link } from "react-router-dom";

export default class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      posts: [],
      currentPage: 1,
      totalPages: 1,
      postsPerPage: 3,
    };
  }

  componentDidMount() {
    this.retrievePosts();
  }

  retrievePosts(page = 1) {
    const { postsPerPage } = this.state;
    axios
      .get(`http://localhost:9001/posts?page=${page}&limit=${postsPerPage}`)
      .then((res) => {
        if (res.data.success) {
          this.setState({
            posts: res.data.existingPosts,
            currentPage: page,
            totalPages: Math.ceil(res.data.totalPosts / postsPerPage),
          });
        } else {
          console.error("Error fetching posts:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
      });
  }

  renderPagination() {
    const { currentPage, totalPages } = this.state;
    const pages = [];
    const maxVisiblePages = 2; // Number of page buttons to show on each side of the current page

    // Display first page
    if (currentPage > 1) {
      pages.push(
        <button
          key={1}
          className={`pagination-button ${1 === currentPage ? "active" : ""}`}
          onClick={() => this.retrievePosts(1)}
        >
          1
        </button>
      );
    }

    // Show ellipses if there are pages between the first and current page
    if (currentPage > maxVisiblePages + 1) {
      pages.push(<span key="left-ellipsis">...</span>);
    }

    // Display pages around the current page
    for (
      let i = Math.max(2, currentPage - maxVisiblePages);
      i <= Math.min(totalPages - 1, currentPage + maxVisiblePages);
      i++
    ) {
      pages.push(
        <button
          key={i}
          className={`pagination-button ${i === currentPage ? "active" : ""}`}
          onClick={() => this.retrievePosts(i)}
        >
          {i}
        </button>
      );
    }

    // Show ellipses if there are pages between the current and last page
    if (currentPage < totalPages - maxVisiblePages) {
      pages.push(<span key="right-ellipsis">...</span>);
    }

    // Display last page
    if (totalPages > 1) {
      pages.push(
        <button
          key={totalPages}
          className={`pagination-button ${totalPages === currentPage ? "active" : ""}`}
          onClick={() => this.retrievePosts(totalPages)}
        >
          {totalPages}
        </button>
      );
    }

    return (
      <div className="pagination">
        {currentPage > 1 && (
          <button onClick={() => this.retrievePosts(currentPage - 1)}>
            Previous
          </button>
        )}
        {pages}
        {currentPage < totalPages && (
          <button onClick={() => this.retrievePosts(currentPage + 1)}>
            Next
          </button>
        )}
      </div>
    );
  }

  // Helper function to truncate the summary
  truncateSummary(summary, maxLength = 100) {
    if (summary.length > maxLength) {
      return `${summary.substring(0, maxLength)}...`;
    }
    return summary;
  }

  render() {
    const { posts } = this.state;
  
    return (
      <div className="home">
        <h1 style={{ color: "black", fontWeight: "bold" }}>My Modules</h1> {/* This is the H1 */}
        <br />
        <div className="posts-list">
          {posts.length > 0 ? (
            posts.map((post) => (
              <div key={post._id} className="post-card">
                <h2>{post.title}</h2>
                <p>{this.truncateSummary(post.summary)}</p>
                <Link to={`/post/${post._id}`} className="view-more-link">
                  View More
                </Link>
              </div>
            ))
          ) : (
            <p>No posts available.</p>
          )}
        </div>
        {this.renderPagination()}
      </div>
    );
  }
}  