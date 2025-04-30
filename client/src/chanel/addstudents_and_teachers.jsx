import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function AddStudentsAndTeachers() {
  const { chenalId } = useParams(); // Access chenalId from URL params
  const [formData, setFormData] = useState({
    channelId: chenalId, // Set default value to passed channelId prop
    email: "",
    phone: "",
    dateOfBirth: "",
    name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setFormData((prevState) => ({
      ...prevState,
      channelId: chenalId,
    }));
  }, [chenalId]); // Re-run this effect when chenalId changes

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { channelId, email, phone, dateOfBirth, name } = formData;

    if (!channelId || !email || !phone || !dateOfBirth || !name) {
      alert("All fields are required!");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await axios.post(
        "http://localhost:9001/student/save",
        formData
      );

      if (response.status === 200) {
        alert("Student/Teacher added successfully!");
        setFormData({
          channelId: chenalId,
          email: "",
          phone: "",
          dateOfBirth: "",
          name: "",
        });
      }
    } catch (error) {
      console.error("There was an error!", error);
      setError("An error occurred while adding the student/teacher.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-students-container">
      <h2>Add Students and Teachers</h2>
      <p>Channel ID: {formData.channelId}</p>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="channelId">Channel ID:</label>
          <input
            type="text"
            id="channelId"
            name="channelId"
            value={formData.channelId}
            onChange={handleChange}
            placeholder="Enter channel ID"
            readOnly
          />
        </div>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter name"
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter email"
            required
          />
        </div>
        <div>
          <label htmlFor="phone">Phone:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            placeholder="Enter phone number"
            required
          />
        </div>
        <div>
          <label htmlFor="dateOfBirth">Date of Birth:</label>
          <input
            type="date"
            id="dateOfBirth"
            name="dateOfBirth"
            value={formData.dateOfBirth}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add Student/Teacher"}
        </button>
      </form>
    </div>
  );
}

export default AddStudentsAndTeachers;
