// src/components/TeacherViewAssignments.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/teacher.css"; // Ensure you create this CSS file

const TeacherViewAssignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const response = await axios.get("http://localhost:9001/cms/assignments");
        setAssignments(response.data.assignments);
      } catch (error) {
        console.error("Failed to fetch assignments:", error);
        setErrorMessage("Failed to load assignments.");
      }
    };

    fetchAssignments();
  }, []);

  return (
    <div className="teacher-view">
      <h2>Student Assignment Submissions</h2>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <div className="assignments-container">
        {assignments.length > 0 ? (
          assignments.map((assignment, index) => (
            <div key={index} className="assignment-card">
              <h3>{assignment.CMS_id} - {assignment.email}</h3>
              <p dangerouslySetInnerHTML={{ __html: assignment.content }} />
            </div>
          ))
        ) : (
          <p>No assignments submitted yet.</p>
        )}
      </div>
    </div>
  );
};

export default TeacherViewAssignments;
