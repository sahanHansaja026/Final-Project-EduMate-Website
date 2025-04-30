import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import "../../css/curd.css"; // Import your CSS file

const CurdsPage = () => {
  const { quiz_id } = useParams(); // Get the quiz_id from URL
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        console.log("Fetching posts for quiz_id:", quiz_id);
        const response = await axios.get(
          `http://localhost:9001/post/quiz/${quiz_id}`
        );

        if (response.data.success) {
          setPosts(response.data.posts);
        } else {
          setError("post not found");
        }
      } catch (error) {
        if (error.response) {
          console.error("Server error:", error.response.data);
          setError(error.response.data.message || "Server error");
        } else if (error.request) {
          console.error("No response from server:", error.request);
          setError("No response from server");
        } else {
          console.error("Error setting up request:", error.message);
          setError("Request setup error");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [quiz_id]);

  const onDelete = (postId) => {
    if (window.confirm("Are you sure you want to delete this question?")) {
      axios
        .delete(`http://localhost:9001/post/delete/${postId}`)
        .then((res) => {
          if (res.data.message === "Post deleted successfully") {
            alert("Delete successful");
            setPosts(posts.filter((post) => post._id !== postId)); // Remove deleted post from UI
          } else {
            alert("Error deleting post");
          }
        })
        .catch((error) => {
          console.error("Error deleting post:", error);
          alert("Error deleting post");
        });
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="curd">
      <center>
        <h1>Question Management Board</h1>
        <h3>Quiz ID: {quiz_id}</h3> {/* Display Quiz ID here */}
      </center>
      {posts.length === 0 ? (
        <p>No posts found for this quiz.</p>
      ) : (
        <center>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Question</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {posts.map((post, index) => (
                <tr key={post._id}>
                  <td>{index + 1}</td>
                  <td>
                    <Link
                      to={`/getquestion/${post._id}`}
                      style={{ textDecoration: "none", color: "white" }}
                    >
                      {post.question}
                    </Link>
                  </td>
                  <td>
                    <Link className="btn btn-warning" to={`/qedit/${post._id}`}>
                      <i className="fa fa-edit"></i>&nbsp;Edit
                    </Link>
                    &nbsp;
                    <button
                      className="btn btn-danger"
                      onClick={() => onDelete(post._id)}
                    >
                      <i className="fa fa-trash"></i>&nbsp;Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </center>
      )}
    </div>
  );
};

export default CurdsPage;
