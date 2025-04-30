import React, { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faVideo, faSpinner } from "@fortawesome/free-solid-svg-icons"; // Import spinner icon
import { v4 as uuidv4 } from "uuid"; // Import uuid
import "../css/video.css";

const InputVideo = () => {
  const { id } = useParams(); // Extract the 'id' from the URL
  const [newPost, setNewPost] = useState({
    card_id: id || "", // Initialize card_id with id from URL
    video_name: "",
    video: null,
    video_id: uuidv4(), // Generate unique video_id
  });
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false); // <-- NEW loading state

  const handleChange = (event) => {
    const { name, value } = event.target;
    setNewPost((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleFileChange = (file) => {
    setNewPost((prevState) => ({
      ...prevState,
      video: file,
    }));
  };

  const handleDrag = (event) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.type === "dragenter" || event.type === "dragover") {
      setDragActive(true);
    } else if (event.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      handleFileChange(event.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData();
    for (let key in newPost) {
      formData.append(key, newPost[key]);
    }

    const { video_name, video, card_id, video_id } = newPost;
    if (!video_name || !video || !card_id) {
      alert("Please fill in all required fields.");
      return;
    }
    console.log("Video ID:", video_id); // this counts as using the variable
    setLoading(true); // Start loading
    axios
      .post("http://localhost:9001/video/save", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.data.success) {
          console.log("Video added successfully");
          setNewPost({
            card_id: id || "",
            video_name: "",
            video: null,
            video_id: uuidv4(), // Reset video_id to a new unique value
          });
        } else {
          console.error("Error adding video:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error adding video:", error);
      });
  };

  const getFileIcon = () => {
    if (!newPost.video) {
      return <FontAwesomeIcon icon={faVideo} className="default-icon" />;
    }

    const fileType = newPost.video.name.split(".").pop().toLowerCase();
    if (fileType === "mp4") {
      return <FontAwesomeIcon icon={faVideo} className="file-icon-video" />;
    } else {
      return <FontAwesomeIcon icon={faVideo} className="file-icon-video" />;
    }
  };

  return (
    <div className="video-upload">
      <h1>Add Your Video</h1>
      <div className="input-video-container">
        <form onSubmit={handleSubmit} className="input-form">
          {/* Video Name Input */}
          <label>
            <input
              type="text"
              name="video_name"
              value={newPost.video_name}
              placeholder="Video Name"
              onChange={handleChange}
              className="video-name-input"
            />
          </label>

          {/* Drag-and-Drop Video Area */}
          <div className="file-drop-area">
            <div
              className={`drop-area ${dragActive ? "active" : ""}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {newPost.video ? (
                <>
                  {getFileIcon()}
                  <p>{newPost.video.name}</p>
                </>
              ) : (
                <>
                  {getFileIcon()}
                  <p>Drag & Drop Video (MP4) or Click to Select</p>
                </>
              )}
            </div>
            <input
              type="file"
              name="video"
              accept=".mp4"
              onChange={(event) => handleFileChange(event.target.files[0])}
              className="file-input"
            />
          </div>

          {/* Submit Button */}
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              <FontAwesomeIcon
                icon={faSpinner}
                spin
                style={{ marginRight: "8px" }}
              />
            ) : (
              "Upload Video"
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default InputVideo;
