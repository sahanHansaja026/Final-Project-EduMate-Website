import React, { useState } from "react";
import { FaBook, FaUsers } from "react-icons/fa"; // Import new icons
import Module from "./my_enrollement";
import Chanels from "./my_chanellEnrolle";
import "../css/searchcomponent.css";

// SearchTabs Component to toggle between Search and Tag Search
const EnrollementTabs = () => {
  const [activeTab, setActiveTab] = useState("search");

  // Change the active tab
  const handleTabChange = (tab) => setActiveTab(tab);

  return (
    <div className="search-tabs">
      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button
          onClick={() => handleTabChange("search")}
          className={`tab-button ${activeTab === "search" ? "active" : ""}`}
        >
          <FaBook /> My Modules
        </button>
        <button
          onClick={() => handleTabChange("tags")}
          className={`tab-button ${activeTab === "tags" ? "active" : ""}`}
        >
          <FaUsers /> My Subscriptions
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === "search" && <Module />}
        {activeTab === "tags" && <Chanels />}
      </div>
    </div>
  );
};

export default EnrollementTabs;
