import React, { useRef, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom"; // Import useParams
import "../css/notewritter.css";
import { v4 as uuidv4 } from "uuid"; // Import uuid

function Editor() {
  const contentRef = useRef(null);
  const [isSaving] = useState(false);
  const [articleName, setArticleName] = useState("");
  const { id } = useParams(); // Extract the `card_id` from the URL

  // Handle text formatting
  const formatText = (command, value = null) => {
    document.execCommand(command, false, value);
  };

  // Handle font size change
  const setFontSize = (size) => {
    document.execCommand("fontSize", false, "7");
    const fontElements = document.getElementsByTagName("font");
    for (let font of fontElements) {
      if (font.size === "7") {
        font.removeAttribute("size");
        font.style.fontSize = `${size}px`;
      }
    }
  };

  // Handle color change
  const changeColor = (color) => {
    document.execCommand("foreColor", false, color);
  };

const saveArticle = async () => {
  if (!articleName.trim()) {
    alert("Please provide an article name.");
    return;
  }

  const content = contentRef.current.innerHTML; // Get the HTML content from the editor

  try {
    const response = await axios.post(
      "http://localhost:9001/saveArticles",
      {
        card_id: id, // Ensure this is correctly passed (from useParams())
        article_name: articleName,
        content,
        article_id: uuidv4(),
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (response.data.success) {
      alert("Article saved successfully!");
    } else {
      alert("Failed to save article.");
    }
  } catch (error) {
    console.error("Error saving article:", error.response || error); // Log the full error
    alert("An error occurred while saving the article.");
  }
};

  return (
    <div className="editor-container">
      <div className="toolbar">
        <input
          type="text"
          value={articleName}
          onChange={(e) => setArticleName(e.target.value)}
          placeholder="Enter article name"
          className="article-name-input"
        />
        <button onClick={() => formatText("bold")}>Bold</button>
        <button onClick={() => formatText("italic")}>Italic</button>
        <button onClick={() => formatText("underline")}>Underline</button>
        <button onClick={() => formatText("justifyLeft")}>Align Left</button>
        <button onClick={() => formatText("justifyCenter")}>Center</button>
        <button onClick={() => formatText("justifyRight")}>Align Right</button>
        <button onClick={() => formatText("insertUnorderedList")}>
          Bullet List
        </button>
        <select onChange={(e) => setFontSize(e.target.value)}>
          <option value="11">11px</option>
          <option value="12">12px</option>
          <option value="14">14px</option>
          <option value="16">16px</option>
          <option value="18">18px</option>
          <option value="20">20px</option>
          <option value="22">22px</option>
          <option value="25">25px</option>
        </select>
        <select onChange={(e) => formatText("formatBlock", e.target.value)}>
          <option value="p">Paragraph</option>
          <option value="h1">Heading 1</option>
          <option value="h2">Heading 2</option>
          <option value="h3">Heading 3</option>
          <option value="h4">Heading 4</option>
          <option value="h5">Heading 5</option>
          <option value="h6">Heading 6</option>
        </select>
        <input
          type="color"
          onChange={(e) => changeColor(e.target.value)}
          title="Choose Text Color"
        />
        <button onClick={saveArticle} disabled={isSaving}>
          {isSaving ? "Saving..." : "Save Article"}
        </button>
      </div>

      {/* Display the card id */}
      <div>
        <h3>Editing Article with ID: {id}</h3>
      </div>

      <div
        ref={contentRef}
        className="editable-content"
        contentEditable
        placeholder="Write your content here..."
      ></div>
    </div>
  );
}

export default Editor;
