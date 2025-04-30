import React, { useRef, useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import "../css/notewritter.css";

function Editor() {
  const contentRef = useRef(null);
  const [isSaving, setIsSaving] = useState(false);
  const [articleName, setArticleName] = useState("");
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const { article_id } = useParams();

  // Fetch article when the page loads
  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const res = await axios.get(
          `http://localhost:9001/articles/${article_id}`
        );
        if (res.data.success) {
          setArticleName(res.data.article.article_name);
          setContent(res.data.article.content);
        } else {
          console.error("Failed to fetch article");
        }
      } catch (error) {
        console.error("Error fetching article:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchArticle();
  }, [article_id]);

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

  // Save (Update) the article
  const saveArticle = async () => {
    if (!articleName.trim()) {
      alert("Please provide an article name.");
      return;
    }

    const updatedContent = contentRef.current.innerHTML;
    setIsSaving(true);

    try {
      const response = await axios.put(
        `http://localhost:9001/updateArticle/${article_id}`,
        {
          article_name: articleName,
          content: updatedContent,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.data.success) {
        alert("✅ Article updated successfully!");
      } else {
        alert("❌ Failed to update article.");
      }
    } catch (error) {
      console.error("Error updating article:", error);
      alert("An error occurred while updating the article.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <div className="loading">Loading article...</div>;
  }

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
          {isSaving ? "Updating..." : "Update Article"}
        </button>
      </div>

      <div className="editing-info">
        <h3>Editing Article ID: {article_id}</h3>
      </div>

      <div
        ref={contentRef}
        className="editable-content"
        contentEditable
        placeholder="Write your content here..."
        dangerouslySetInnerHTML={{ __html: content }}
      ></div>
    </div>
  );
}

export default Editor;
