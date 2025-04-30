import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../css/landin.css";
import Student from "../images/Online test (1).gif";
import Teacher from "../images/job_teacher_classroom_teacher-removebg-preview.png";
import People from "../images/users-solid.svg";
import Cloud from "../images/cloud-solid.svg";
import Laptop from "../images/laptop-solid.svg";

const Landing = () => {
  const navigate = useNavigate();
  const [totalQuizzes, setTotalQuizzes] = useState(0);
  const [totalUsers, setTotalUsers] = useState(0);
  const [quizError, setQuizError] = useState(null);
  const [userError, setUserError] = useState(null);

  // Fetch total quizzes count
  useEffect(() => {
    const fetchTotalQuizzes = async () => {
      try {
        const response = await axios.get("http://localhost:9001/posts/count");
        if (response.data.success) {
          setTotalQuizzes(response.data.count);
        } else {
          setQuizError("Failed to fetch the total quizzes");
        }
      } catch (err) {
        setQuizError("Error fetching quizzes: " + err.message);
      }
    };
    fetchTotalQuizzes();

    const fetchTotalUsers = async () => {
      try {
        const response = await axios.get("http://localhost:9001/count");
        if (response.data.success) {
          setTotalUsers(response.data.count);
        } else {
          setUserError("Failed to fetch the total users");
        }
      } catch (err) {
        setUserError("Error fetching users: " + err.message);
      }
    };
    fetchTotalUsers();
  }, []);

  const handleClick = () => {
    navigate("/login");
  };

  return (
    <div className="landing">
      <div className="title">
        <div className="hedder">
          <h1>ModuleMate</h1>
        </div>
        <button onClick={handleClick}>Login Now</button>
      </div>
      <div className="maincontainer">
        <div className="silinder">
          <img src={Student} alt="Student illustration" />
        </div>
        <div className="subcontainer">
          <div className="circle1">
            <img src={Teacher} alt="Teacher illustration" />
          </div>
          <div className="circle2">
            <h2>100%</h2>
            <p>Free and Accessible</p>
          </div>
        </div>
        <div className="mainheddr">
          <h1>Create, Share, and Learn Anytime, Anywhere!</h1>
          <p>
            Welcome to ModuleMate, an innovative platform where creativity meets
            education! Whether you’re an aspiring educator or a passionate
            learner, ModuleMate empowers you to design engaging courses and
            activities on any subject. Experience collaborative learning by
            challenging friends, testing your skills, and discovering new
            knowledge all without complicated sign-ups. Jump in, create, share,
            and start your educational adventure today!
          </p>
        </div>
      </div>
      <div className="boxcontainer">
        <div className="box">
          <h2>Our Core Features</h2>
          <hr />
          <div className="iconscontainer">
            <div className="iconscontainer1">
              <center>
                <img src={People} alt="Real-Time Collaboration icon" />
                <h3>Real-Time Collaboration</h3>
                <p>
                  Invite friends or classmates to create and take quizzes
                  together in real-time, enhancing the learning experience
                </p>
              </center>
            </div>
            <div className="iconscontainer1">
              <center>
                <img src={Cloud} alt="Cloud-Based Database icon" />
                <h3>Cloud-Based Database</h3>
                <p>
                  Store and manage your quizzes securely in the cloud, ensuring
                  fast access from anywhere at any time
                </p>
              </center>
            </div>
          </div>
          <center>
            <div className="iconscontainer1">
              <center>
                <img src={Laptop} alt="Mobile & Web Access icon" />
                <h3>Mobile & Web Access</h3>
                <p>
                  100% mobile-friendly design allows you to create and take
                  quizzes seamlessly on any device, whether it's your phone,
                  tablet, or computer
                </p>
              </center>
            </div>
          </center>
        </div>
        <div className="landbox">
          <div className="boxland0">
            <div className="quiz-count">
              <h3>{quizError ? quizError : totalQuizzes}</h3>
              <h3>Total Modules</h3>
            </div>
            <div className="quiz-count">
              <h3>{userError ? userError : totalUsers}</h3>
              <h3>Total Users</h3>
            </div>
            <div className="vertical-bar"></div>
            <p>
              Be part of a vibrant global network filled with enthusiastic users
              who are eager to share knowledge, and in an inspiring educational
              community!
            </p>
          </div>
          <div className="subboxland">
            <div className="boxland1"></div>
            <div className="boxland2"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
