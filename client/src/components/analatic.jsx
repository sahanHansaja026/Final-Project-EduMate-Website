import React, { useEffect, useState } from "react";
import { Bar, Line } from "react-chartjs-2";
import axios from "axios";
import authService from "../services/authService";
import "../css/chart_bar.css";
import Card from "../images/card copy.png";
import Student from "../images/student copy.png";
import Teacher from "../images/teacher copy.png";

const CombinedDashboard = () => {
  const [ setUserChartData] = useState({});
  const [email, setEmail] = useState("");
  const [postCount, setPostCount] = useState(0);
  const [totalStudents, setTotalStudents] = useState(0);
  const [totalAdmins, setTotalAdmins] = useState(0);
  const [ setLoading] = useState(true);
  const [ setError] = useState(null);

  // Fetch user data
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await authService.getUserData();
        setEmail(userData.email);
      } catch (error) {
        console.error("Failed to fetch user data", error);
      }
    };
    fetchUserData();
  }, []);

  // Fetch scores and user summary data
  useEffect(() => {
    const fetchData = async () => {
      try {
        if (email) {
          const response = await axios.get("http://localhost:9001/scores", {
            params: { email },
          });
          const data = response.data;

          if (data.length > 0) {
            const labels = data.map((user) => user.username);
            const scores = data.map((user) => user.score);

            setUserChartData({
              labels: labels,
              datasets: [
                {
                  label: "Your Scores",
                  backgroundColor: "transparent",
                  borderColor: "rgba(75, 192, 192, 1)",
                  borderWidth: 4,
                  data: scores,
                  fill: true,
                },
              ],
            });
          } else {
            console.error("No data found for the user");
            setUserChartData({});
          }
        }

        const postResponse = await axios.get(
          "http://localhost:9001/posts/count"
        );
        if (postResponse.data.success) {
          setPostCount(postResponse.data.count);
        } else {
          setError("Failed to fetch the count of posts");
        }

        const userResponse = await axios.get(
          "http://localhost:9001/userprofile/summary"
        );
        if (userResponse.data.success) {
          setTotalStudents(userResponse.data.totalStudents);
          setTotalAdmins(userResponse.data.totalAdmins);
        } else {
          setError("Failed to fetch user summary");
        }
      } catch (err) {
        setError("Error fetching data: " + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [email]);

  // Fetch top card IDs and their titles
 

  return (
    <div className="charts">
      <div className="top_of_dash">
        <div className="dashbox1">
          <img src={Card} alt="Example" />
          <div className="info">
            <h4>{postCount}</h4>
            <br />
            <p>Total Modules</p>
          </div>
        </div>

        <div className="dashbox1">
          <img src={Student} alt="Example" />
          <div className="info">
            <h4>{totalStudents}</h4>
            <br />
            <p>Students</p>
          </div>
        </div>

        <div className="dashbox1">
          <img src={Teacher} alt="Example" />
          <div className="info">
            <h4>{totalAdmins}</h4>
            <br />
            <p>Module Owners</p>
          </div>
        </div>
      </div>
      <div className="tableshow">
        <div className="chart-container">

        </div>{" "}
        <div className="chart-container">

        </div>
      </div>
      <br />
      <center>
        <div className="add_sence">Google Ads</div>
      </center>
    </div>
  );
};

export default CombinedDashboard;
