import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import authService from "../services/authService";
import axios from "axios";
import "../css/enrolle.css"; // Import the CSS file

const Enrolle = ({ setCardId }) => {
  const [email, setEmail] = useState("");
  const [ setMessage] = useState("");
  const [cardDetails, setCardDetails] = useState({}); // State to store card details
  const { id } = useParams();
  const navigate = useNavigate();

  // Fetch user data and check enrollment
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await authService.getUserData();
        setEmail(userData.email);

        const enrollmentData = {
          card_id: id,
          email: userData.email,
        };

        const response = await axios.post(
          "http://localhost:9001/check-enrollment",
          enrollmentData
        );

        if (response.data.isEnrolled) {
          navigate(`/moduleowner/${id}`);
        }
      } catch (error) {
        console.error("Failed to fetch user data or check enrollment", error);
      }
    };

    fetchUserData();
  }, [id, navigate]);

  // Fetch card details
  useEffect(() => {
    const fetchCardDetails = async () => {
      try {
        const card_id = id;
        const response = await axios.get(
          `http://localhost:9001/chenalpostes/${card_id}`
        );
        if (response.data.success) {
          setCardDetails(response.data.post);
        }
      } catch (error) {
        console.error("Failed to fetch card details", error);
      }
    };

    fetchCardDetails();
  }, [id]);

  useEffect(() => {
    if (setCardId) {
      setCardId(id);
    }
  }, [id, setCardId]);

  // Handle enroll button click
  const handleEnrollClick = async () => {
    try {
      const enrollmentData = {
        card_id: id,
        email: email,
      };

      await axios.post("http://localhost:9001/enroll", enrollmentData);
      setMessage("Enrollment successful");
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setMessage("You have already enrolled in this course.");
        navigate(`/moduleowner/${id}`);
      } else {
        setMessage("Failed to enroll. Please try again later.");
      }
    }
  };

  return (
    <div className="enrolle-container">
      {cardDetails && (
        <div className="enrole_deatails">
          <div className="showingcard">
            <h2>{cardDetails.title}</h2>
            <img
              src={
                cardDetails.image
                  ? cardDetails.image
                  : ""
              }
              alt={cardDetails.image ? cardDetails.image : "No Image"}
            />
          </div>
          <div className="a">
            <p>{cardDetails.summery}</p>
          </div>
        </div>
      )}
      <button onClick={handleEnrollClick}>Enroll</button>
      <div className="commengidelines">
        <h3>
          Community Comment Guidelines: Fostering a Positive Learning Space
        </h3>
        <div className="b">
          <p>
            At ModuleMate, we strive to create an inclusive and respectful
            learning environment where students and instructors can engage in
            thoughtful discussions. To maintain the quality of interactions
            across all courses, we ask that users adhere to our comment
            guidelines. Always be respectful and courteous in your
            communications, avoiding offensive or inappropriate language. Keep
            discussions relevant to the course material and provide constructive
            feedback that helps others learn. Refrain from spamming or posting
            promotional content, and avoid sharing quiz answers or assignments.
            We encourage you to ask meaningful questions and contribute
            positively to the community. For privacy reasons, please do not
            share personal information, and if you encounter any inappropriate
            behavior, report it to our support team. Failure to comply with
            these guidelines may result in your comments being removed or
            account suspension. Let’s work together to build a positive learning
            experience for everyone at ModuleMate!
          </p>
        </div>
      </div>
    </div>
  );
};

export default Enrolle;
