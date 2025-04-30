import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFileAlt,
  faFilePdf,
  faFileWord,
} from "@fortawesome/free-solid-svg-icons";
import "../../css/vedioedit.css";

const EditAssignment = () => {
  const { assignment_id } = useParams(); // Extract the assignment_id from the URL
  const navigate = useNavigate(); // For navigation after actions
  const [assignmentDetails, setAssignmentDetails] = useState({
    assignment_id: assignment_id || "",
    assignment_name: "",
    assignment: null,
    existingFile: "",
  });
  const [dragActive, setDragActive] = useState(false);

  // Fetch existing assignment details
  useEffect(() => {
    axios
      .get(`http://localhost:9001/assignment/get/${assignment_id}`)
      .then((response) => {
        const { assignment_name, file_url, assignment_id } = response.data;
        setAssignmentDetails({
          assignment_id,
          assignment_name,
          assignment: null,
          existingFile: file_url, // Store the current file's URL
        });
      })
      .catch((error) => {
        console.error("Error fetching assignment details:", error);
      });
  }, [assignment_id]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setAssignmentDetails((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleFileChange = (file) => {
    setAssignmentDetails((prevState) => ({
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
    formData.append("assignment_id", assignmentDetails.assignment_id);
    formData.append("assignment_name", assignmentDetails.assignment_name);
    if (assignmentDetails.assignment) {
      formData.append("assignment", assignmentDetails.assignment);
    }

    axios
      .put(
        `http://localhost:9001/assignment/update/${assignment_id}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      )
      .then((res) => {
        if (res.data.success) {
          console.log("Assignment updated successfully");
          navigate("/assignments"); // Redirect to assignments list
        } else {
          console.error("Error updating assignment:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error updating assignment:", error);
      });
  };

  const handleDelete = () => {
    if (window.confirm("Are you sure you want to delete this assignment?")) {
      axios
        .delete(`http://localhost:9001/assignment/delete/${assignment_id}`)
        .then((res) => {
          if (res.data.success) {
            console.log("Assignment deleted successfully");
            navigate("/assignments"); // Redirect to assignments list
          } else {
            console.error("Error deleting assignment:", res.data.error);
          }
        })
        .catch((error) => {
          console.error("Error deleting assignment:", error);
        });
    }
  };

  const getFileIcon = () => {
    if (assignmentDetails.assignment) {
      const fileType = assignmentDetails.assignment.name
        .split(".")
        .pop()
        .toLowerCase();
      if (fileType === "pdf") {
        return <FontAwesomeIcon icon={faFilePdf} className="file-icon-pdf" />;
      } else if (fileType === "doc" || fileType === "docx") {
        return <FontAwesomeIcon icon={faFileWord} className="file-icon-word" />;
      } else {
        return <FontAwesomeIcon icon={faFileAlt} className="default-icon" />;
      }
    } else if (assignmentDetails.existingFile) {
      return (
        <FontAwesomeIcon icon={faFileAlt} className="existing-file-icon" />
      );
    }
    return <FontAwesomeIcon icon={faFileAlt} className="default-icon" />;
  };

  return (
    <div className="assignment">
      <h1>Edit Your Assignment</h1>

      <div className="input-sub-container">
        <form onSubmit={handleSubmit} className="input-form">
          {/* Assignment Name Input */}
          <label>
            <input
              type="text"
              name="assignment_name"
              value={assignmentDetails.assignment_name || ""}
              placeholder="Enter Assignment Name"
              onChange={handleChange}
            />
          </label>

          {/* Drag-and-Drop File Area */}
          <div className="file-drop-area">
            <div
              className={`drop-area ${dragActive ? "active" : ""}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {assignmentDetails.assignment ? (
                <>
                  {getFileIcon()}
                  <p>{assignmentDetails.assignment.name}</p>
                </>
              ) : assignmentDetails.existingFile ? (
                <>
                  {getFileIcon()}
                  <p>
                    Current File:{" "}
                    {assignmentDetails.existingFile.split("/").pop()}
                  </p>
                </>
              ) : (
                <>
                  {getFileIcon()}
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
          </div>

          <button type="submit" className="submit-btn">
            Update Assignment
          </button>
          <button type="button" className="delete-btn" onClick={handleDelete}>
            Delete Assignment
          </button>
        </form>
      </div>
    </div>
  );
};

export default EditAssignment;
