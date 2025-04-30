// routes/card.js
const express = require("express");
const Posts = require("../models/card");
const multer = require("multer");
const path = require("path");

const routers = express.Router();

// Upload configuration (store file in memory)
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Save a new post
routers.post("/posts/save", upload.single("image"), async (req, res) => {
  try {
    const { email, card_id, title, tags, summery } = req.body;

    if (!email || !card_id || !title || !tags || !summery || !req.file) {
      return res.status(400).json({ error: "All fields are required" });
    }

    const newPost = new Posts({
      email,
      title,
      summery,
      tags,
      card_id,
      image: {
        data: req.file.buffer,
        contentType: req.file.mimetype,
      },
    });

    await newPost.save();
    return res.status(200).json({ success: "Post saved successfully" });
  } catch (error) {
    console.error("Error saving post:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});
// Get all posts
routers.get("/posts", async (req, res) => {
  try {
    const posts = await Posts.find().sort({ _id: -1 }).exec();

    const formattedPosts = posts.map((post) => {
      const postObject = post.toObject();
      if (post.image && post.image.data) {
        postObject.image = `data:${
          post.image.contentType
        };base64,${post.image.data.toString("base64")}`;
      } else {
        postObject.image = null;
      }
      return postObject;
    });

    return res.status(200).json({
      success: true,
      existingPosts: formattedPosts,
    });
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});

// get a specific post by ID
routers.get("/post/:id", async (req, res) => {
  try {
    const postId = req.params.id;
    const cardDetails = await Posts.findById(postId).exec();

    if (!cardDetails) {
      return res
        .status(404)
        .json({ success: false, message: "Post not found" });
    }

    // Convert image data to base64 if it exists
    if (cardDetails.image && cardDetails.image.data) {
      cardDetails.image = `data:${
        cardDetails.image.contentType
      };base64,${cardDetails.image.data.toString("base64")}`;
    }

    return res.status(200).json({ success: true, cardDetails });
  } catch (error) {
    return res.status(400).json({ success: false, error: error.message });
  }
});

//get a count
routers.get("/posts/count", async (req, res) => {
  try {
    const count = await Posts.countDocuments();
    return res.status(200).json({
      success: true,
      count: count,
    });
  } catch (error) {
    console.error("Error fetching post count:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});

routers.get("/postes/:card_id", async (req, res) => {
  try {
    const cardId = req.params.card_id;
    console.log("Card ID received:", cardId);

    // Fetch posts matching the card_id and sort by createdAt descending
    const posts = await Posts.find({ card_id: cardId })
      .sort({ createdAt: -1 })
      .exec();
    console.log("Posts found:", posts);

    if (!posts || posts.length === 0) {
      return res
        .status(200)
        .json({ success: true, message: "No posts found", post: null });
    }

    // Only handle the first post
    const cardDetails = posts[0].toObject(); // 🔥 important: convert Mongoose document to plain object

    // Format image if available
    cardDetails.image = cardDetails.image?.data
      ? `data:${
          cardDetails.image.contentType
        };base64,${cardDetails.image.data.toString("base64")}`
      : null;

    return res.status(200).json({ success: true, post: cardDetails });
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res
      .status(500)
      .json({ success: false, error: "Internal Server Error" });
  }
});

// Get posts by email (using URL parameter)
// routers.get("/posts/:email", async (req, res) => {
routers.get("/posts/:email", async (req, res) => {
  try {
    const { email } = req.params;
    const { page = 1, limit = 10 } = req.query; // Default to page 1 and limit 10

    const skip = (page - 1) * limit; // Calculate how many documents to skip

    // Find posts by email with pagination
    const posts = await Posts.find({ email: email })
      .skip(skip)
      .limit(parseInt(limit))
      .sort({ _id: -1 }) // Sort by most recent
      .exec();

    // Format posts to include Base64 image if available
    const formattedPosts = posts.map((post) => {
      const postObj = post.toObject(); // Convert Mongoose doc to plain object

      postObj.image = postObj.image?.data
        ? `data:${
            postObj.image.contentType
          };base64,${postObj.image.data.toString("base64")}`
        : null; // If no image, set null

      return postObj;
    });

    // Count total posts to calculate total pages
    const totalPosts = await Posts.countDocuments({ email: email });

    return res.status(200).json({
      success: true,
      existingPosts: formattedPosts, // ✅ sending formatted posts with image
      totalPosts,
      totalPages: Math.ceil(totalPosts / limit),
    });
  } catch (error) {
    console.error("Error fetching posts by email:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});


module.exports = routers;
