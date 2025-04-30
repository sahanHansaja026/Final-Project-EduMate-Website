// routes/articleRouter.js
const express = require("express");
const Article = require("../models/assignment"); // Assuming you named your model 'article.js'
const Router = express.Router();
Router.post("/saveArticles", (req, res) => {
  const { card_id, article_name, content, article_id } = req.body;

  // Create a new Article document
  const newArticle = new Article({
    card_id,
    article_name,
    content, // Save the HTML content
    article_id,
  });

  // Save the article to the database
  newArticle
    .save()
    .then(() => {
      return res.status(200).json({
        success: "Article saved successfully",
      });
    })
    .catch((err) => {
      console.error("Error saving article:", err);
      if (!res.headersSent) {
        return res.status(400).json({
          error: err.message,
        });
      }
    });
});

Router.get("/getArticle/:card_id", (req, res) => {
  const { card_id } = req.params; // Extract card_id from URL parameter

  Article.findOne({ card_id }) // Find the article by card_id
    .then((article) => {
      if (!article) {
        return res.status(404).json({ error: "Article not found" });
      }
      res.status(200).json({ success: true, article });
    })
    .catch((err) => {
      console.error("Error fetching article:", err);
      res.status(500).json({ error: "Server error" });
    });
});

Router.get("/articles/:article_id", (req, res) => {
  const { article_id } = req.params; // Extract card_id from URL parameter

  Article.findOne({ article_id }) // Find the article by card_id
    .then((article) => {
      if (!article) {
        return res.status(404).json({ error: "Article not found" });
      }
      res.status(200).json({ success: true, article });
    })
    .catch((err) => {
      console.error("Error fetching article:", err);
      res.status(500).json({ error: "Server error" });
    });
});
// Update article using article_id
Router.put("/updateArticle/:article_id", async (req, res) => {
  const { article_name, content } = req.body;
  const { article_id } = req.params;

  try {
    const updatedArticle = await Article.findOneAndUpdate(
      { article_id: article_id },
      { article_name: article_name, content: content },
      { new: true } // Return the updated document
    );

    if (!updatedArticle) {
      return res.status(404).json({ success: false, message: "Article not found" });
    }

    return res.status(200).json({
      success: true,
      message: "Article updated successfully",
      article: updatedArticle,
    });
  } catch (error) {
    console.error("Error updating article:", error);
    if (!res.headersSent) {
      return res.status(500).json({ success: false, error: error.message });
    }
  }
});


module.exports = Router;
