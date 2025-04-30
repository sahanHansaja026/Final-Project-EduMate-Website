import React, { useState, useEffect } from "react";
import { Link, Route, Routes, Navigate } from "react-router-dom";
import "../css/dashboard.css";
import GiftCard from "../components/GiftCard";
import Subscriptionplane from "./upgrade";
import Create from "../components/create_card";
import Search from "../components/searchcomponent";
import SearchBar from "../components/search";
import TagSearch from "../components/tagsearch";
import authService from "../services/authService";
import axios from "axios";
import Enroll from "../components/my_enrollementcomponent";
import MyModule from "../components/my_creation_component";
import Chanel from "../chanel/chanel";
import Mychenal from "../chanel/mychenal";
import Chart from "../components/analatic";
import Home from "../pages/home_page";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faUserGraduate,
  faSearch,
  faGift,
  faPlusCircle,
  faFolderOpen,
  faChartArea,
  faTv,
} from "@fortawesome/free-solid-svg-icons";

const Dashboard = () => {
  const [isGiftCardOpen, setIsGiftCardOpen] = useState(false);
  const [isSubscriptionOpen, setIsSubscriptionOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [setProfileSummary] = useState(null);
  const [isSearchDropdownOpen, setIsSearchDropdownOpen] = useState(false);

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

  useEffect(() => {
    if (email) {
      const fetchProfileSummary = async () => {
        try {
          const response = await axios.get(
            `http://localhost:9001/userprofile/summary/${email}`
          );
          setProfileSummary(response.data);
        } catch (error) {
          console.error("Failed to fetch profile information", error);
        }
      };
      fetchProfileSummary();
    }
  }, [email]);

  const openGiftCardModal = () => setIsGiftCardOpen(true);
  const closeGiftCardModal = () => setIsGiftCardOpen(false);
  const openSubscriptionModal = () => setIsSubscriptionOpen(true);
  const closeSubscriptionModal = () => setIsSubscriptionOpen(false);

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <ul>
          <li>
            <Link to="/dashboard/analytics">
              <FontAwesomeIcon icon={faChartArea} /> Analytics
            </Link>
          </li>
          <li>
            <Link to="/dashboard/myenrollement">
              <FontAwesomeIcon icon={faUserGraduate} /> My Enrollment
            </Link>
          </li>

          {/* Search Module with Dropdown */}
          <li>
            <div
              onClick={() => setIsSearchDropdownOpen(!isSearchDropdownOpen)}
              style={{
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
              }}
            >
              <FontAwesomeIcon icon={faSearch} /> Smart Search
            </div>
            {isSearchDropdownOpen && (
              <ul className="dropdown-menu">
                <li>
                  <Link to="/dashboard/search">Keyword Search</Link>
                </li>
                <li>
                  <Link to="/dashboard/TagSearch">Filter by Tags</Link>
                </li>
              </ul>
            )}
          </li>
          <li>
            <Link to="/dashboard/create_card">
              <FontAwesomeIcon icon={faPlusCircle} /> Create Module
            </Link>
          </li>
          <li>
            <Link to="/dashboard/my_modules">
              <FontAwesomeIcon icon={faFolderOpen} /> My Creation
            </Link>
          </li>
          <li>
            <Link to="/dashboard/chenal">
              <FontAwesomeIcon icon={faTv} /> Create Channel
            </Link>
          </li>
          <li>
            <button
              className="subscription-btn"
              onClick={openSubscriptionModal}
            >
              Upgrade Plan
            </button>
          </li>
          <li>
            <button className="open-modal-btn" onClick={openGiftCardModal}>
              <FontAwesomeIcon icon={faGift} /> Open Gift Card
            </button>
          </li>
        </ul>
      </aside>

      <main className="main-content">
        <Routes>
          <Route path="/create_card" element={<Create />} />
          <Route path="/searchcomponent" element={<Search />} />
          <Route path="*" element={<Navigate to="/dashboard/analytics" />} />
          <Route path="/myenrollement" element={<Enroll />} />
          <Route path="/analytics" element={<Chart />} />
          <Route path="/my_modules" element={<MyModule />} />
          <Route path="/chenal" element={<Chanel />} />
          <Route path="/mychenal" element={<Mychenal />} />
          <Route path="/search" element={<SearchBar />} />
          <Route path="/tagsearch" element={<TagSearch />} />
        </Routes>
      </main>

      {isGiftCardOpen && <GiftCard closeModal={closeGiftCardModal} />}
      {isSubscriptionOpen && (
        <Subscriptionplane closeModal={closeSubscriptionModal} />
      )}
    </div>
  );
};

export default Dashboard;
