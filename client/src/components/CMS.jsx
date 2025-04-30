import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../css/cms.css";
import authService from "../services/authService";
import axios from "axios";

const CMS = () => {
  const [fontColor, setFontColor] = useState("#333");
  const [bgColor, setBgColor] = useState("#fff");
  const [userEmail, setUserEmail] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [assignmentData, setAssignmentData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const { CMS_id } = useParams();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await authService.getUserData();
        setUserEmail(userData.email);
      } catch (error) {
        console.error("Failed to fetch user data", error);
        setErrorMessage("Failed to fetch user data.");
      }
    };

    const fetchAssignmentData = async () => {
      try {
        const response = await axios.get(`http://localhost:9001/cms/${CMS_id}`);
        console.log("Fetched data:", response.data);

        if (response.data.success) {
          setAssignmentData(response.data.posts[0]);
        } else {
          setErrorMessage(response.data.message || "Failed to fetch assignment data.");
        }
      } catch (error) {
        console.error("Failed to fetch assignment data", error);
        setErrorMessage(error.response ? error.response.data.message : "Failed to fetch assignment data.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserData();
    fetchAssignmentData();
  }, [CMS_id]);

  const execCmd = (command, value = null) => {
    document.execCommand(command, false, value);
  };

  const handleSave = async () => {
    const content = document.querySelector(".content-area").innerHTML;

    try {
      const response = await axios.post("http://localhost:9001/save-assignment", {
        email: userEmail,
        CMS_id: CMS_id,
        content: content,
      });

      if (response.data.success) {
        alert("Assignment saved successfully!");
      } else {
        setErrorMessage(response.data.message || "Failed to save assignment.");
      }
    } catch (error) {
      console.error("Failed to save assignment", error);
      setErrorMessage(error.response ? error.response.data.message : "Failed to save assignment.");
    }
  };

  return (
    <div className="CMS">
      <div className="user-info">
        {errorMessage && <div className="error-message">{errorMessage}</div>}
        <p>
          <strong>Email:</strong> {userEmail}
        </p>
        <p>
          <strong>CMS ID:</strong> {CMS_id}
        </p>
        {isLoading ? (
          <p>Loading assignment details...</p>
        ) : (
          assignmentData ? (
            <div>
              <h3>{assignmentData.CMS_name}</h3>
              <p>{assignmentData.description}</p>
            </div>
          ) : (
            <p>No assignment details available.</p>
          )
        )}
      </div>

      <div className="cms-container">
        <h2>Your Platform for Academic Expression</h2>

        <div className="toolbar">
          <button onClick={() => execCmd("bold")}>
            <i className="fas fa-bold" title="Bold"></i>
          </button>
          <button onClick={() => execCmd("italic")}>
            <i className="fas fa-italic" title="Italic"></i>
          </button>
          <button onClick={() => execCmd("underline")}>
            <i className="fas fa-underline" title="Underline"></i>
          </button>
          <button onClick={() => execCmd("strikeThrough")}>
            <i className="fas fa-strikethrough" title="Strikethrough"></i>
          </button>
          <button onClick={() => execCmd("insertOrderedList")}>
            <i className="fas fa-list-ol" title="Ordered List"></i>
          </button>
          <button onClick={() => execCmd("insertUnorderedList")}>
            <i className="fas fa-list-ul" title="Unordered List"></i>
          </button>
          <button onClick={() => execCmd("justifyLeft")}>
            <i className="fas fa-align-left" title="Align Left"></i>
          </button>
          <button onClick={() => execCmd("justifyCenter")}>
            <i className="fas fa-align-center" title="Align Center"></i>
          </button>
          <button onClick={() => execCmd("justifyRight")}>
            <i className="fas fa-align-right" title="Align Right"></i>
          </button>

          <select onChange={(e) => execCmd("fontSize", e.target.value)} className="font-size">
            <option value="2">Small</option>
            <option value="4">Normal</option>
            <option value="5">Large</option>
            <option value="6">X-Large</option>
          </select>

          <input
            type="color"
            onChange={(e) => {
              execCmd("foreColor", e.target.value);
              setFontColor(e.target.value);
            }}
            className="color-picker"
            title="Font Color"
          />
          <input
            type="color"
            onChange={(e) => setBgColor(e.target.value)}
            className="color-picker"
            title="Background Color"
          />
        </div>

        <div
          className="content-area"
          contentEditable="true"
          style={{ backgroundColor: bgColor, color: fontColor }}
          placeholder="Start writing your assignment..."
        ></div>

        <button onClick={handleSave} className="save-button">
          Save Assignment
        </button>
      </div>
    </div>
  );
};

export default CMS;
