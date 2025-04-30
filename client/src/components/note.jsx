import React, { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFileAlt,
  faFilePdf,
  faFileWord,
} from "@fortawesome/free-solid-svg-icons";
import "../css/assignment.css"; // Updated to note-related CSS file

const InputNote = () => {
  const { id } = useParams(); // Extract the 'id' from the URL
  const [newNote, setNewNote] = useState({
    card_id: id || "", // Initialize card_id with id from URL
    note_name: "",
    note: null,
  });
  const [dragActive, setDragActive] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setNewNote((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleFileChange = (file) => {
    setNewNote((prevState) => ({
      ...prevState,
      note: file, // Updated to 'note' instead of 'assignment'
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
    for (let key in newNote) {
      formData.append(key, newNote[key]);
    }

    const { note_name, note, card_id } = newNote;
    if (!note_name || !note || !card_id) {
      alert("Please fill in all required fields.");
      return;
    }

    axios
      .post("http://localhost:9001/note/save", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.data.success) {
          console.log("Note added successfully");
          setNewNote({
            card_id: id || "",
            note_name: "",
            note: null,
          });
        } else {
          console.error("Error adding note:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error adding note:", error);
      });
  };

  const getFileIcon = () => {
    if (!newNote.note) {
      return <FontAwesomeIcon icon={faFileAlt} className="default-icon" />;
    }

    // Detect the file type
    const fileType = newNote.note.name.split(".").pop().toLowerCase();
    if (fileType === "pdf") {
      return <FontAwesomeIcon icon={faFilePdf} className="file-icon-pdf" />;
    } else if (fileType === "doc" || fileType === "docx") {
      return <FontAwesomeIcon icon={faFileWord} className="file-icon-word" />;
    } else {
      return <FontAwesomeIcon icon={faFileAlt} className="default-icon" />;
    }
  };

  return (
    <div className="note-submission">
      <h1>Submit Your Notes</h1>
      <div className="input-note-container">
        <form onSubmit={handleSubmit} className="input-form">
          <label>
            <br />
            <input
              type="text"
              name="note_name"
              value={newNote.note_name}
              placeholder="Your Note Name"
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
              {newNote.note ? (
                <>
                  {getFileIcon()}
                  <p>{newNote.note.name}</p>
                </>
              ) : (
                <>
                  {getFileIcon()}
                  <br />
                  <p>Drag & Drop Note (PDF/Word) or Click to Select</p>
                </>
              )}
            </div>
            <input
              type="file"
              name="note"
              accept=".pdf, .doc, .docx"
              onChange={(event) => handleFileChange(event.target.files[0])}
              className="file-input"
            />
          </label>
          <br />
          <button type="submit" className="submit-btn">
            Submit Note
          </button>
        </form>
      </div>
    </div>
  );
};

export default InputNote;
