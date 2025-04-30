import React, { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { v4 as uuidv4 } from "uuid"; // Import uuid
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFileAlt,
  faFilePdf,
  faFileWord,
} from "@fortawesome/free-solid-svg-icons";
import "../css/assignment.css";

const InputSub = () => {
  const { id } = useParams(); // Extract the 'id' from the URL
  const [newPost, setNewPost] = useState({
    card_id: id || "", // Initialize card_id with id from URL
    assignment_name: "",
    assignment: null,
    assignment_id:uuidv4(),
  });
  const [dragActive, setDragActive] = useState(false);

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
      assignment: file,
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

    const { assignment_name, assignment, card_id,assignment_id } = newPost;
    if (!assignment_name || !assignment || !card_id) {
      alert("Please fill in all required fields.");
      return;
    }

    axios
      .post("http://localhost:9001/assignment/save", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.data.success) {
          console.log("Post added successfully");
          setNewPost({
            card_id: id || "",
            assignment_name: "",
            assignment: null,
            assignment_id:uuidv4(),
          });
        } else {
          console.error("Error adding post:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error adding post:", error);
      });
  };

  const getFileIcon = () => {
    if (!newPost.assignment) {
      return <FontAwesomeIcon icon={faFileAlt} className="default-icon" />;
    }

    // Detect the file type
    const fileType = newPost.assignment.name.split(".").pop().toLowerCase();
    if (fileType === "pdf") {
      return <FontAwesomeIcon icon={faFilePdf} className="file-icon-pdf" />;
    } else if (fileType === "doc" || fileType === "docx") {
      return <FontAwesomeIcon icon={faFileWord} className="file-icon-word" />;
    } else {
      return <FontAwesomeIcon icon={faFileAlt} className="default-icon" />;
    }
  };

  return (
    <div className="assignment">
      <h1>Add Your Assignment</h1>
      <div className="input-sub-container">
        <form onSubmit={handleSubmit} className="input-form">
          <label>
            <br />
            <input
              type="text"
              name="assignment_name"
              value={newPost.assignment_name}
              placeholder="Your File Name"
              onChange={handleChange}
            />
          </label>
          <br />

          <label className="file-drop-area">
            <div
              className={`drop-area ${dragActive ? "active" : ""}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {newPost.assignment ? (
                <>
                  {getFileIcon()}
                  <p>{newPost.assignment.name}</p>
                </>
              ) : (
                <>
                  {getFileIcon()}
                  <br />
                  <p>Drag & Drop Assignment (PDF/Word) or Click to Select</p>
                </>
              )}
            </div>
            <input
              type="file"
              name="assignment"
              accept=".pdf, .doc, .docx"
              onChange={(event) => handleFileChange(event.target.files[0])}
              className="file-input"
            />
          </label>
          <br />
          <button type="submit" className="submit-btn">
            Store in the System
          </button>
        </form>
      </div>
    </div>
  );
};

export default InputSub;
