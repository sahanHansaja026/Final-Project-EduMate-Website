const express = require("express");
const Posts = require("../models/create_chanel");
const multer = require("multer");
const path = require("path");

const routers = express.Router();

// Upload configuration (store file in memory)
const storage = multer.memoryStorage();
const upload = multer({ storage });


// Save post
routers.post("/chanel/save", upload.single("image"), async (req, res) => {
  try {
    const { email, chenal_id, title, summery } = req.body;

    if (!email || !chenal_id || !title || !summery || !req.file) {
      return res.status(400).json({ error: "All fields are required" });
    }

    const imagePath = req.file.filename;

    const newPost = new Posts({
      email,
      title,
      summery,
      chenal_id,
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
routers.get("/ch", async (req, res) => {
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
});

routers.get("/chnel/:id", async (req, res) => {
  try {
    const postId = req.params.id;
    const userProfile = await Posts.findById(postId).lean();

    if (!userProfile) {
      return res
        .status(404)
        .json({ success: false, message: "Post not found" });
    }

    if (userProfile.image && userProfile.image.data) {
      userProfile.image = `data:${
        userProfile.image.contentType
      };base64,${Buffer.from(userProfile.image.data).toString("base64")}`;
    }

    return res.status(200).json({ success: true, userProfile });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});



//get a count
routers.get("/chenel/count", async (req, res) => {
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

routers.get("/chenel/:chenal_id", async (req, res) => {
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

    return res.status(200).json({ success: true, post: posts[0] }); // Return only the first post
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res.status(500).json({ success: false, error: error.message });
  }
});

routers.get("/ch/:email", async (req, res) => {
  try {
    const { email } = req.params;
    const { page = 1, limit = 10 } = req.query;

    const skip = (page - 1) * limit;

    // Fetch posts by email with pagination
    const posts = await Posts.find({ email })
      .skip(skip)
      .limit(parseInt(limit))
      .sort({ _id: -1 })
      .exec();

    // Convert image data to base64 for each post
    const postsWithImages = posts.map((post) => {
      const postObj = post.toObject(); // Convert Mongoose doc to plain object
      if (postObj.image && postObj.image.data) {
        postObj.image = `data:${
          postObj.image.contentType
        };base64,${postObj.image.data.toString("base64")}`;
      }
      return postObj;
    });

    const totalPosts = await Posts.countDocuments({ email });

    return res.status(200).json({
      success: true,
      existingPosts: postsWithImages,
      totalPosts,
      totalPages: Math.ceil(totalPosts / limit),
    });
  } catch (error) {
    console.error("Error fetching posts by email:", error.message);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});


module.exports = routers;
