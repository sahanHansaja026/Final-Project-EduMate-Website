import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";
import "../css/createquiz.css"; // Assuming this is where the CSS file is saved

const Add_CMS = ({ setCardId }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [cmsId, setCmsId] = useState("");
  const [cmsName, setCmsName] = useState("");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const newCmsId = uuidv4(); // Generate a new CMS ID on component mount
    setCmsId(newCmsId);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const cmsData = {
      card_id: id,
      CMS_id: cmsId,
      CMS_name: cmsName,
      description: description,
    };

    try {
      const response = await axios.post("http://localhost:9001/cms/save", cmsData);
      setMessage("CMS assignment created successfully!"); // Update success message
      // Optionally, redirect after a successful submission
      navigate(`/teacherweek/${id}`); // Change to your desired path
    } catch (error) {
      if (error.response && error.response.data) {
        setMessage(error.response.data.error);
      } else {
        setMessage("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="quiz">
      <div className="container">
        <h1>Create Online Writing Assignment</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Assignment Name</label>
            <input
              type="text"
              value={cmsName}
              onChange={(e) => setCmsName(e.target.value)} // Updated from setQuizName to setCmsName
              required
            />
          </div>
          <div>
            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <button type="submit">Create Writing Assignment</button>
        </form>

        {message && (
          <p className={message.includes("successfully") ? "success" : "error"}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default Add_CMS;
