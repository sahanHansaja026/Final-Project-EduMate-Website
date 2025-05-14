import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "../css/weeks.css";
import Message from "./message";
import authService from "../services/authService";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  FaPlus,
  FaFileAlt,
  FaVideo,
  FaStickyNote,
  FaClipboardList,
  FaCog,
} from "react-icons/fa";

const AddPage = ({ setCardId }) => {
  const { id } = useParams();
  const [assignments, setAssignments] = useState([]);
  const [selectedMaterial, setSelectedMaterial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState("");
  const [post, setPost] = useState(null);
  const [setPostLoading] = useState(true);
  const [setErrorMessage] = useState("");
  const [setCmsName] = useState("");
  const [progress, setProgress] = useState({});
  const [view, setView] = useState("details"); // Tracks the current view: "details" or "message"
  const navigate = useNavigate();

  useEffect(() => {
    if (setCardId) {
      setCardId(id);
    }

    const fetchPostDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:9001/postes/${id}`);
        if (response.data.success) {
          setPost(response.data.post);
          setCmsName(response.data.post.cmsName || "");
        } else {
          setErrorMessage("Post not found");
        }
      } catch (error) {
        console.error("Error fetching post details:", error);
        setErrorMessage("Error fetching post details");
      } finally {
        setPostLoading(false);
      }
    };

    const fetchAssignments = async () => {
      try {
        const response = await axios.get(
          `http://localhost:9001/activities/${id}`
        );
        if (response.data.success) {
          setAssignments(response.data.posts);
          setSelectedMaterial(response.data.posts[0] || null); // Default to the first material
        } else {
          setAssignments([]);
        }
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        setErrorMessage("Error fetching assignments");
      } finally {
        setLoading(false);
      }
    };

    const fetchUserData = async () => {
      try {
        const userData = await authService.getUserData();
        setEmail(userData.email);

        // Fetch progress for each assignment
        const progressData = {};
        for (const assignment of assignments) {
          try {
            const res = await axios.get(
              `http://localhost:9001/user-activities/${userData.email}/${assignment._id}`
            );
            if (res.data.success) {
              progressData[assignment._id] = res.data.activity.completed;
            }
          } catch (error) {
            console.error(
              `Error fetching progress for ${assignment._id}:`,
              error
            );
          }
        }
        setProgress(progressData);
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        setErrorMessage("Failed to fetch user data");
      }
    };

    fetchPostDetails();
    fetchAssignments();
    fetchUserData();
  }, [id, setCardId]);

  const handleCreateActivity = () => {
    window.location.href = `/add/${id}`;
  };

  const handleMaterialClick = (material) => {
    setView("details"); // Switch back to details view
    setSelectedMaterial(material);
  };
  const handleCourseClick = (card_id) => {
    markProgress(card_id);
    navigate(`/teacherweek/${card_id}`);
  };
  const handleCourseGradeClick = (card_id) => {
    markProgress(card_id);
    navigate(`/corsegrade/${card_id}`);
  };
  const handleSettingsClick = (card_id) => {
    markProgress(card_id);
    navigate(`/settings/${card_id}`);
  };
  const handleQuizClick = (quiz_id) => {
    markProgress(quiz_id);
    navigate(`/quiz/${quiz_id}`);
  };
  const handleVedioEditClick = (video_id) => {
    markProgress(video_id);
    navigate(`/vdiosedit/${video_id}`);
  };
  const handlArticalEditClick = (article_id) => {
    markProgress(article_id);
    navigate(`/articaledit/${article_id}`);
  };
  const handlQuizEditClick = (quiz_id) => {
    markProgress(quiz_id);
    navigate(`/quizedit/${quiz_id}`);
  };
  const handlQuizGradeClick = (quiz_id) => {
    markProgress(quiz_id);
    navigate(`/quizgradeview/${quiz_id}`);
  };
  const handlCMSEditClick = (CMS_id) => {
    markProgress(CMS_id);
    navigate(`/CMSedit/${CMS_id}`);
  };
  const handlCMSGradeClick = (CMS_id) => {
    markProgress(CMS_id);
    navigate(`/CMSgradeview/${CMS_id}`);
  };
  const handleAssignmentEditClick = (assignment_id) => {
    markProgress(assignment_id);
    navigate(`/assgnmentedit/${assignment_id}`);
  };
  const handleCMSClick = (CMS_id) => {
    markProgress(CMS_id);
    navigate(`/WriteCMS/${CMS_id}`);
  };
  const handleMyGradeEditClick = (card_id) => {
    markProgress(card_id);
    navigate(`/mygrade/${card_id}`);
  };
  const handleclicknavigate = () => {
    setView("message"); // Switch to message view
  };
  const isTeacher = useMemo(() => post && post.email === email, [post, email]);
  // const isStudent = useMemo(() => post && email !== post.email, [post, email]);

  const markProgress = async (activity_id) => {
    try {
      await axios.post("http://localhost:9001/progress", {
        email,
        activity_id,
      });
      setProgress({ ...progress, [activity_id]: true });
    } catch (error) {
      console.error("Error marking progress:", error);
    }
  };
  return (
    <div className="page-container">
      <div className="sidebar">
        <h3>Course Materials</h3>
        <ul>
          {assignments.map((assignment) => (
            <li
              key={assignment._id}
              className={
                assignment._id === selectedMaterial?._id ? "active" : ""
              }
              onClick={() => handleMaterialClick(assignment)}
            >
              {assignment.assignment_name ||
                assignment.video_name ||
                assignment.note_name ||
                assignment.quiz_name ||
                assignment.CMS_name ||
                assignment.article_name ||
                "Untitled Material"}
            </li>
          ))}
          <li onClick={handleclicknavigate}>Chat & Feedback</li>
        </ul>
        {post && post.email === email && (
          <button className="btn-create" onClick={handleCreateActivity}>
            <FaPlus /> Create New Activity
          </button>
        )}
      </div>
      <div className="content">
        <div className="horizontalbar">

            <button className="three-dots-btn" onClick={() => handleMyGradeEditClick(selectedMaterial.card_id)}>
              <h4>My Grade</h4>
            </button>

          {isTeacher && (
            <>
              <button className="three-dots-btn" onClick={() => handleSettingsClick(selectedMaterial.card_id)}>
                <h4>Settings</h4>
              </button>
              <button className="three-dots-btn" onClick={() => handleCourseGradeClick(selectedMaterial.card_id)}>
                <h4>Grades</h4>
              </button>
            </>
          )}
          <button
            className="three-dots-btn"
            onClick={() => handleCourseClick(selectedMaterial.card_id)}
          >
            <h4>Course</h4>
          </button>
        </div>
        {view === "details" ? (
          loading ? (
            <p>Loading assignments...</p>
          ) : selectedMaterial ? (
            <div className="assignment-details">
              <div>
                <h2>{selectedMaterial.assignment_name}</h2>
                {selectedMaterial.assignment_url && (
                  <p>
                    {post && post.email === email && (
                      <button
                        className="three-dots-btn"
                        onClick={() =>
                          handleAssignmentEditClick(
                            selectedMaterial.assignment_id
                          )
                        }
                      >
                        <h4>Clik to Edit</h4>
                      </button>
                    )}
                    <FaFileAlt /> Assignment File:{" "}
                    <a
                      href={`${selectedMaterial.assignment_url}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Download Assignment
                    </a>
                  </p>
                )}
              </div>
              {selectedMaterial.video_name && selectedMaterial.video_url && (
                <div>
                  <div className="editandtitle">
                    {post && post.email === email && (
                      <button
                        className="three-dots-btn"
                        onClick={() =>
                          handleVedioEditClick(selectedMaterial.video_id)
                        }
                      >
                        <h4>Click to Edit</h4>
                      </button>
                    )}
                  </div>
                  <video
                    width="1000"
                    height="auto" // This adjusts the height automatically based on the width
                    controls
                    onPlay={() => markProgress(selectedMaterial._id)}
                  >
                    <source
                      src={selectedMaterial.video_url} // Use the video URL from MongoDB
                      type="video/mp4"
                    />
                    Your browser does not support the video tag.
                  </video>
                </div>
              )}
              {selectedMaterial.note_name && selectedMaterial.note && (
                <div>
                  <h3>
                    <FaStickyNote /> Notes: {selectedMaterial.note_name}
                  </h3>
                  <a
                    href={`http://localhost:9001/NotesFile/${selectedMaterial.note}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download Notes
                  </a>
                </div>
              )}
              {selectedMaterial.article_name && selectedMaterial.content && (
                <div>
                  <div className="editandtitle">
                    {post && post.email === email && (
                      <button
                        className="three-dots-btn"
                        onClick={() =>
                          handlArticalEditClick(selectedMaterial.article_id)
                        }
                      >
                        <h4>Click to Edit</h4>
                      </button>
                    )}
                  </div>
                  <h3>Notes: {selectedMaterial.article_name}</h3>
                  {/* Display article content using dangerouslySetInnerHTML */}
                  <div
                    className="article-content"
                    dangerouslySetInnerHTML={{
                      __html: selectedMaterial.content,
                    }}
                  />
                  {/* Link to download the article content */}
                  <a
                    href={`http://localhost:9001/NotesFile/${selectedMaterial.content}`} // Adjust this to point to the correct file if needed
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download Notes
                  </a>
                </div>
              )}
              {selectedMaterial.CMS_name && (
                <div>
                  <div className="editandtitle">
                    {post && post.email === email && (
                      <div className="assignment-card">
                        <div className="action-buttons">
                          <button
                            className="edit-btn"
                            onClick={() =>
                              handlCMSEditClick(selectedMaterial.CMS_id)
                            }
                          >
                            <i className="fas fa-edit"></i> Edit
                          </button>
                          <button
                            className="grade-btn"
                            onClick={() =>
                              handlCMSGradeClick(selectedMaterial.CMS_id)
                            }
                          >
                            <i className="fas fa-chart-bar"></i> View Grade
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                  <h3>
                    <FaClipboardList /> CMS: {selectedMaterial.CMS_name}
                  </h3>
                  <button
                    className="btn-action"
                    onClick={() => handleCMSClick(selectedMaterial.CMS_id)}
                  >
                    Open CMS
                  </button>
                </div>
              )}
              {selectedMaterial.quiz_name && (
                <div>
                  <div className="editandtitle">
                    {post && post.email === email && (
                      <div className="assignment-card">
                        <div className="action-buttons">
                          <button
                            className="edit-btn"
                            onClick={() =>
                              handlQuizEditClick(selectedMaterial.quiz_id)
                            }
                          >
                            <i className="fas fa-edit"></i> Edit
                          </button>
                          <button
                            className="grade-btn"
                            onClick={() =>
                              handlQuizGradeClick(selectedMaterial.quiz_id)
                            }
                          >
                            <i className="fas fa-chart-bar"></i> View Grade
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                  <h3>
                    <FaClipboardList /> Quiz: {selectedMaterial.quiz_name}
                  </h3>
                  <div className="parbox">
                    <p>{selectedMaterial.description}</p>
                  </div>
                  <button
                    className="btn-action"
                    onClick={() => handleQuizClick(selectedMaterial.quiz_id)}
                  >
                    Start Quiz
                  </button>
                </div>
              )}
            </div>
          ) : (
            <p>Select a material to view its details</p>
          )
        ) : (
          <Message id={id} /> // Render Message component with module ID
        )}
      </div>
    </div>
  );
};

export default AddPage;
