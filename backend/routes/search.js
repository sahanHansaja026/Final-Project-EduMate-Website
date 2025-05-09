const express = require("express");
const Posts = require("../models/card"); // models import
const routee = express.Router();

// Search posts by partial title
// Search posts by partial title
routee.post("/search", (req, res) => {
  const { title } = req.body;

  if (!title) {
    return res.status(400).json({ error: "Module name is required" });
  }

  const regex = new RegExp(title, 'i'); // 'i' for case-insensitive, removed \b for broader match

  Posts.find({ title: { $regex: regex } })
    .then((posts) => {
      if (!posts || posts.length === 0) {
        return res.status(404).json({ error: "No Module is found" });
      }

      const processedPosts = posts.map((post) => {
        const postObject = {
          ...post._doc,
        };

        if (post.image && post.image.data) {
          postObject.image = `data:${post.image.contentType};base64,${post.image.data.toString("base64")}`;
        } else {
          postObject.image = null;
        }

        return postObject;
      });

      return res.status(200).json({ success: true, existingPosts: processedPosts });
    })
    .catch((err) => {
      return res.status(500).json({ error: err.message });
    });
});

// Search posts by tags
routee.get("/posts/tags/search", async (req, res) => {
  try {
    const { tags } = req.query; // Get the tags query parameter
    if (!tags) {
      return res.status(400).json({ error: "Tags parameter is required" });
    }

    const tagArray = tags.split(","); // Convert comma-separated tags into an array

    // Find posts that match any of the selected tags
    const posts = await Posts.find({ tags: { $in: tagArray } });

    if (posts.length === 0) {
      return res.status(404).json({ message: "No posts found for these tags" });
    }

    return res.status(200).json({ posts });
  } catch (error) {
    console.error("Error searching posts:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});



module.exports = routee; // export routee
