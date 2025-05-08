/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import "../../css/curd.css";

const CurdsPage = () => {
  const { CMS_id } = useParams();
  const [posts, setPosts] = useState([]);
  const [scores, setScores] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch posts
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get(
          `http://localhost:9001/cmsget/${CMS_id}`
        );
        if (response.data.success) {
          setPosts(response.data.posts);
        } else {
          setError("Posts not found");
        }
      } catch (error) {
        console.error("Error fetching posts:", error);
        setError("Error loading posts");
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [CMS_id]);

  // Fetch scores for each post (email)
  useEffect(() => {
    const fetchScores = async () => {
      const newScores = {};

      for (const post of posts) {
        try {
          const response = await axios.get(
            `http://localhost:9001/getscore/${CMS_id}/${post.email}`
          );
          newScores[post.email] = response.data.score;
        } catch (err) {
          newScores[post.email] = "N/A";
        }
      }

      setScores(newScores);
    };

    if (posts.length > 0) {
      fetchScores();
    }
  }, [posts, CMS_id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="curd">
      <center>
        <h1>CMS SCORE VIEW</h1>
        <h3>CMS ID: {CMS_id}</h3>
      </center>

      {posts.length === 0 ? (
        <p>No posts found for this CMS ID.</p>
      ) : (
        <center>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Student Email</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {posts.map((post, index) => (
                <tr key={post._id}>
                  <td>{index + 1}</td>
                  <td>
                    <Link
                      to={`/CMSgradeadd/${post._id}`}
                      style={{ textDecoration: "none", color: "white" }}
                    >
                      {post.email}
                    </Link>
                  </td>
                  <td>{scores[post.email] ?? "Loading..."}</td>
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
