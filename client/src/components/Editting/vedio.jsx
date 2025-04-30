import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faVideo } from "@fortawesome/free-solid-svg-icons";
import "../../css/vedioedit.css";

const EditVideo = () => {
  const { video_id } = useParams(); // Extract the 'video_id' from the URL
  const navigate = useNavigate(); // For navigation after successful update
  const [videoDetails, setVideoDetails] = useState({
    video_id: video_id || "", // Initialize video_id with id from URL
    video_name: "",
    video: null,
    existingVideo: "",
  });
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    // Fetch existing video details from the server
    axios
      .get(`http://localhost:9001/video/get/${video_id}`)
      .then((response) => {
        const { video_id, video_name, video_url } = response.data;
        setVideoDetails({
          video_id,
          video_name,
          video: null,
          existingVideo: video_url, // Store existing video URL for reference
        });
      })
      .catch((error) => {
        console.error("Error fetching video details:", error);
      });
  }, [video_id]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setVideoDetails((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleFileChange = (file) => {
    setVideoDetails((prevState) => ({
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
    formData.append("video_id", videoDetails.video_id);
    formData.append("video_name", videoDetails.video_name);
    if (videoDetails.video) {
      formData.append("video", videoDetails.video); // Only append if a new file is selected
    }

    // Submit update request to the server
    axios
      .put(`http://localhost:9001/video/update/${video_id}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.data.success) {
          console.log("Video updated successfully");
          navigate("/videos"); // Redirect to the video list page or another relevant page
        } else {
          console.error("Error updating video:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error updating video:", error);
      });
  };

  const handleDelete = () => {
    // Confirm before deletion
    if (window.confirm("Are you sure you want to delete this video?")) {
      // Send DELETE request to the server
      axios
        .delete(`http://localhost:9001/video/delete/${video_id}`)
        .then((res) => {
          if (res.data.success) {
            console.log("Video deleted successfully");
            navigate("/videos"); // Redirect to the video list page or another relevant page
          } else {
            console.error("Error deleting video:", res.data.error);
          }
        })
        .catch((error) => {
          console.error("Error deleting video:", error);
        });
    }
  };

  const getFileIcon = () => {
    if (videoDetails.video) {
      return <FontAwesomeIcon icon={faVideo} className="file-icon-video" />;
    } else if (videoDetails.existingVideo) {
      return <FontAwesomeIcon icon={faVideo} className="existing-file-icon" />;
    } else {
      return <FontAwesomeIcon icon={faVideo} className="default-icon" />;
    }
  };

  const renderVideoPreview = () => {
    if (videoDetails.video) {
      return (
        <video
          controls
          className="video-preview"
          src={URL.createObjectURL(videoDetails.video)}
        />
      );
    } else if (videoDetails.existingVideo) {
      return (
        <video
          controls
          className="video-preview"
          src={videoDetails.existingVideo}
        />
      );
    }
    return null;
  };

  return (
    <div className="video-upload">
      <h1 className="page-title">Edit Your Video</h1>

      <div className="input-video-container">
        <form onSubmit={handleSubmit} className="input-form">
          {/* Video Name Input */}
          <label>
            <input
              type="text"
              name="video_name"
              value={videoDetails.video_name || ""}
              placeholder="Enter Video Name"
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
              {videoDetails.video ? (
                <>
                  {getFileIcon()}
                  <p>{videoDetails.video.name}</p>
                </>
              ) : videoDetails.existingVideo ? (
                <>
                  {getFileIcon()}
                  <p>
                    Current Video: {videoDetails.existingVideo.split("/").pop()}
                  </p>
                  <p>Drag & Drop to Replace</p>
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

          {/* Video Preview */}
          <div className="video-preview-container">{renderVideoPreview()}</div>

          {/* Submit Button */}
          <button type="submit" className="submit-btn">
            Update Video
          </button>
        </form>

        {/* Delete Button */}
        <button className="delete-btn" onClick={handleDelete}>
          Delete Video
        </button>
      </div>
    </div>
  );
};

export default EditVideo;
