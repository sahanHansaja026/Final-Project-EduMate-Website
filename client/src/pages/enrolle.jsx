import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import authService from "../services/authService";
import axios from "axios";
import "../css/enrolle.css"; // Import the CSS file

const Enrolle = ({ setCardId }) => {
  const [email, setEmail] = useState("");
  const [setMessage] = useState("");
  const [cardDetails, setCardDetails] = useState({});
  const [enrollmentCount, setEnrollmentCount] = useState(0); // State for enrollment count
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
          navigate(`/teacherweek/${id}`);
        }
      } catch (error) {
        console.error("Failed to fetch user data or check enrollment", error);
      }
    };

    fetchUserData();
  }, [id, navigate]);

  // Fetch card details and enrollment count
  useEffect(() => {
    const fetchCardDetails = async () => {
      try {
        const card_id = id;
        const response = await axios.get(
          `http://localhost:9001/postes/${card_id}`
        );
        if (response.data.success) {
          setCardDetails(response.data.post);
        }
      } catch (error) {
        console.error("Failed to fetch card details", error);
      }
    };

    const fetchEnrollmentCount = async () => {
      try {
        const response = await axios.get(
          `http://localhost:9001/enrollment-count/${id}`
        );
        if (response.data.success) {
          setEnrollmentCount(response.data.count);
        }
      } catch (error) {
        console.error("Failed to fetch enrollment count", error);
      }
    };

    fetchCardDetails();
    fetchEnrollmentCount();
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
      setEnrollmentCount((prevCount) => prevCount + 1); // Update count immediately on successful enrollment
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setMessage("You have already enrolled in this course.");
        navigate(`/teacherweek/${id}`);
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
            <div className="showdetails">
              {cardDetails.image ? (
                <img src={cardDetails.image} alt="Post" />
              ) : (
                <img
                  src="/images/400 Error Bad Request-rafiki.png"
                  alt="Fallback"
                />
              )}
              <div className="a">
                <p>{cardDetails.summery}</p>
              </div>
            </div>
          </div>
        </div>
      )}
      <div className="enp">{enrollmentCount} already enrolled</div>
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
