import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "../css/showstudents.css"; // Assuming custom styles are defined here

function ShowStudents({ chenalId, adminEmail }) {
  const [students, setStudents] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Function to fetch students from the server
  const fetchStudents = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:9001/studentget?channelId=${chenalId}`
      );
      setStudents(response.data.existingPosts); // Assuming the response contains posts in 'existingPosts'
    } catch (err) {
      setError("No students have joined this channel yet.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (chenalId) {
      fetchStudents(); // Fetch students only if channelId is available
    }
  }, [chenalId]); // Re-run the fetch whenever the chenalId changes

  // Delete student function
  const handleDelete = async (id) => {
    try {
      const res = await axios.delete(
        `http://localhost:9001/student/delete/${id}`
      );
      if (res.data.message === "Post deleted successfully") {
        alert("Delete successful");
        fetchStudents(); // Refresh the student list
      } else {
        alert("Delete successful");
      }
    } catch (error) {
      console.error("Error deleting post:", error);
      alert("Error deleting post");
    }
  };

  return (
    <div className="add-students-container">
      <h2>Add Students and Teachers</h2>
      {/*}
      <p>Channel ID: {chenalId}</p>
      <p>Admin Email: {adminEmail}</p>
  */}

      {loading && <p>Loading students...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {students.length > 0 ? (
        <div>
          <h3>Student List</h3>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Date of Birth</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student._id}>
                  <td>{student.name}</td>
                  <td>{student.email}</td>
                  <td>{student.phone}</td>
                  <td>{student.dateOfBirth}</td>
                  <td>
                    <Link
                      className="btn btn-warning"
                      to={`/edit/${student._id}`}
                    >
                      <i className="fa fa-edit"></i>&nbsp;Edit
                    </Link>
                    &nbsp;
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(student._id)}
                    >
                      <i className="fa fa-trash"></i>&nbsp;Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No students found for this channel ID.</p>
      )}

      {/* Button to navigate to the 'Create New Details' page */}
      <button className="btn btn-success">
        <Link
          to={`/addstudent/${chenalId}`} // Ensure chenalId is passed properly
          style={{ textDecoration: "none", color: "purple" }}
        >
          <i className="fa fa-plus"></i>&nbsp;Create New Details
        </Link>
      </button>
    </div>
  );
}

export default ShowStudents;
