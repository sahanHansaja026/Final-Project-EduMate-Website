import React, { useState } from "react";
import { FaSearch, FaTags } from "react-icons/fa";
import SearchBar from "./search";
import TagSearch from "./tagsearch";
import "../css/searchcomponent.css"

// SearchTabs Component to toggle between Search and Tag Search
const SearchTabs = () => {
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
          <FaSearch /> Search
        </button>
        <button
          onClick={() => handleTabChange("tags")}
          className={`tab-button ${activeTab === "tags" ? "active" : ""}`}
        >
          <FaTags /> Search by Tags
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

export default SearchTabs;
