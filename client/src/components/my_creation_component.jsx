import React, { useState } from "react";
import { FaBook, FaYoutube } from "react-icons/fa";
import SearchBar from "./my_module";
import TagSearch from "../chanel/mychenal";
import "../css/searchcomponent.css";

// SearchTabs Component to toggle between Search and Tag Search
const MYCreations_components = () => {
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
          <FaBook /> Modules
        </button>
        <button
          onClick={() => handleTabChange("tags")}
          className={`tab-button ${activeTab === "tags" ? "active" : ""}`}
        >
          <FaYoutube /> Chanels
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === "search" && <SearchBar />}
        {activeTab === "tags" && <TagSearch />}
      </div>
    </div>
  );
};

export default MYCreations_components;
