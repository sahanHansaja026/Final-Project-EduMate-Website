const express = require("express");
const router = express.Router();
const Post = require("../models/card"); // Assuming the Post model is in the 'models' folder

// GET route for fetching posts by tags
router.get("/tags/search", async (req, res) => {
  const { tags } = req.query;

  // Check if tags are provided
  if (!tags) {
    return res.status(400).json({ error: "Tags are required." });
  }

  // Split tags by comma to get an array
  const tagsArray = tags.split(",");

  try {
    // Query to find posts with any of the selected tags
    const posts = await Post.find({ tags: { $in: tagsArray } }).lean();

    // Format posts to ensure tags is always an array
    const formattedPosts = posts.map((post) => ({
      ...post,
      tags: Array.isArray(post.tags) ? post.tags : [],
    }));

    res.json({ posts: formattedPosts });
  } catch (error) {
    console.error("Error fetching posts:", error);
    res
      .status(500)
      .json({ error: "Error fetching posts. Please try again later." });
  }
});

module.exports = router;
