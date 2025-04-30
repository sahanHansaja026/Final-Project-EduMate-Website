import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import authService from "../services/authService";
import PrimaryAdmin from "./PrimaryAdmin";
import SecondaryAdmin from "./SecondaryAdmin";
import AddStudentsAndTeachers from "./showstudent"; // Corrected import
import "../css/chenal_details.css";

const ChenalDetails = () => {
  const [post, setPost] = useState(null); // Set initial state to null
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeTab, setActiveTab] = useState("primaryAdmin"); // Set single default tab
  const [userProfile, setUserProfile] = useState(null); // State for user profile
  const { id } = useParams();

  // Fetch channel details
  useEffect(() => {
    axios
      .get(`http://localhost:9001/chnel/${id}`)
      .then((res) => {
        if (res.data.success) {
          setPost(res.data.post); // Set post data when available
        }
      })
      .catch((error) => {
        console.error("Error fetching post details:", error);
      });
  }, [id]);

  // Fetch user data and admin profile
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Fetch current user's data
        const userData = await authService.getUserData();
        setUsername(userData.username);
        setEmail(userData.email);

        // Fetch profile using Admin Email from post if available
        if (post?.email) {
          const profileResponse = await axios.get(
            `http://localhost:9001/userprofile/summary/${post.email}`
          );
          if (profileResponse.data.success) {
            setUserProfile(profileResponse.data);
          }
        }
      } catch (error) {
        console.error("Failed to fetch user data or profile", error);
      }
    };

    if (post?.email) {
      fetchUserData();
    }
  }, [post]);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleTabClick = (tabName) => {
    setActiveTab(tabName);
  };
  useEffect(() => {
    if (username) {
      console.log("Logged in Username:", username);
    }
  }, [username]);

  // Conditional checks for tabs
  const showPrimaryAdminTab = post?.email === email;

  if (!post) {
    return <div>Loading...</div>; // Show loading message while post is being fetched
  }

  return (
    <div className="channel-page">
      <div
        className="banner"
        style={{
          backgroundImage: `url(${
            userProfile?.image || "/images/default.png"
          })`, // Use profile image or default if not available
          backgroundSize: "cover", // Ensure the image covers the element
          backgroundPosition: "center",
        }}
      >
        <div className="banner-overlay">
          <h1 className="channel-title">{post.title}</h1>
        </div>

        <div className="chanelprofile">
          <Link to="/Profile">
            <img
              src={
                userProfile?.profileimage
                  ? userProfile.profileimage // Profile image from backend
                  : "/images/default.png"
              }
              alt="Profile"
              className="chaneldpimage"
            />
          </Link>
        </div>
      </div>

      <div className="channel-details">
        {/*}
        <p>User Email: {email}</p>

        <div className="admin-info">
          <h2>Channel Information</h2>
          <p>
            <strong>Admin Email:</strong> {post?.email}
          </p>
          <p>
            <strong>Channel ID:</strong> {post?.chenal_id}
          </p>
        </div>
          */}
        <div className="channel-summary">
          <h3>About This Channel</h3>
          <p className={isExpanded ? "expanded" : "collapsed"}>
            {post?.summery}
          </p>
          <button className="toggle-button" onClick={toggleExpand}>
            {isExpanded ? "See Less" : "See More"}
          </button>
        </div>
      </div>

      {/* Tab Buttons */}
      <div className="tab">
        {showPrimaryAdminTab && (
          <button
            className={`tablinks ${
              activeTab === "primaryAdmin" ? "active" : ""
            }`}
            onClick={() => handleTabClick("primaryAdmin")}
          >
            Admin
          </button>
        )}
        <button
          className={`tablinks ${
            activeTab === "secondaryAdmin" ? "active" : ""
          }`}
          onClick={() => handleTabClick("secondaryAdmin")}
        >
          Student
        </button>
        {showPrimaryAdminTab && (
          <button
            className={`tablinks ${activeTab === "addstudent" ? "active" : ""}`}
            onClick={() => handleTabClick("addstudent")}
          >
            Add Student and Teachers
          </button>
        )}
      </div>

      {/* Tab Content */}
      {activeTab === "primaryAdmin" && showPrimaryAdminTab && <PrimaryAdmin />}
      {activeTab === "addstudent" && showPrimaryAdminTab && (
        <AddStudentsAndTeachers
          chenalId={post?.chenal_id}
          adminEmail={post?.email}
        />
      )}

      {activeTab === "secondaryAdmin" && <SecondaryAdmin />}
    </div>
  );
};

export default ChenalDetails;
