const express = require("express");
const Posts = require("../models/chanelmodule");
const multer = require("multer");
const path = require("path");

const routers = express.Router();

// Upload configuration (store file in memory)
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Save post
routers.post("/chenelsposts/save", upload.single("image"), async (req, res) => {
  try {
    const { email, channel_id, owneremail, card_id,tags, title, summery } = req.body;

    if (!email || !tags || !channel_id || !card_id || !owneremail || !title || !summery || !req.file) {
      return res.status(400).json({ error: "All fields are required" });
    }

    const newPost = new Posts({
      email,
      owneremail,
      title,
      summery,
      card_id,
      channel_id,
      tags,
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
/* routers.get("/chenalposts", async (req, res) => {
  try {
    const posts = await Posts.find().sort({ _id: -1 }).exec();
    return res.status(200).json({
      success: true,
      existingPosts: posts,
    });
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});*/
// Get all posts
routers.get("/chenalposts", async (req, res) => {
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
/*
routers.get("/chenalpost/:id", async (req, res) => {
  try {
    const postId = req.params.id;
    const post = await Posts.findById(postId).exec();
    if (!post) {
      return res
        .status(404)
        .json({ success: false, message: "Post not found" });
    }
    return res.status(200).json({ success: true, post });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});
*/
routers.get("/chenalpost/:id", async (req, res) => {
  try {
    const cardId = req.params.id;
    console.log("Card ID received:", cardId);

    // Fetch posts matching the card_id and sort by createdAt descending
    const posts = await Posts.find({channel_id: cardId,
    })
      .sort({ createdAt: -1 })
      .exec();
    console.log("Posts found:", posts);

    if (!posts || posts.length === 0) {
      return res
        .status(200)
        .json({ success: true, message: "No posts found", post: null });
    }

    // Only handle the first post
    const post = posts[0].toObject(); // 🔥 important: convert Mongoose document to plain object

    // Format image if available
    post.image = post.image?.data
      ? `data:${post.image.contentType};base64,${post.image.data.toString(
          "base64"
        )}`
      : null;

    return res.status(200).json({ success: true, post: post });
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res
      .status(500)
      .json({ success: false, error: "Internal Server Error" });
  }
});

//get a count
routers.get("/chenalposts/count", async (req, res) => {
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

routers.get("/chenalpostes/:card_id", async (req, res) => {
  try {
    const cardId = req.params.card_id;
    console.log("Card ID received:", cardId); // Log the card_id for debugging

    // Fetching posts related to card_id and sorting by createdAt (descending)
    const posts = await Posts.find({ card_id: cardId })
      .sort({ createdAt: -1 })
      .exec();

    console.log("Posts found:", posts); // Log the results for debugging

    if (!posts || posts.length === 0) {
      return res
        .status(200)
        .json({ success: true, message: "No posts found", posts: [] });
    }
    // Only handle the first post
    const cardDetails = posts[0].toObject(); // 🔥 important: convert Mongoose document to plain object

    // Format image if available
    cardDetails.image = cardDetails.image?.data
      ? `data:${
          cardDetails.image.contentType
        };base64,${cardDetails.image.data.toString("base64")}`
      : null;
    
    return res.status(200).json({ success: true, post: cardDetails }); // Return only the first post
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res.status(500).json({ success: false, error: error.message });
  }
});

// Get posts by email (using URL parameter)
// routers.get("/posts/:email", async (req, res) => {
routers.get("/chenalposts/:email", async (req, res) => {
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

    // Count total posts to calculate total pages
    const totalPosts = await Posts.countDocuments({ email: email });

    return res.status(200).json({
      success: true,
      existingPosts: posts,
      totalPosts,
      totalPages: Math.ceil(totalPosts / limit),
    });
  } catch (error) {
    console.error("Error fetching posts by email:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});

module.exports = routers;
