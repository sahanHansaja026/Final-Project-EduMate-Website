const express = require("express");
const Posts = require("../models/createstudent");

const router = express.Router();

// Save student details
router.post("/student/save", async (req, res) => {
  try {
    let newPost = new Posts(req.body);
    await newPost.save();
    return res.status(200).json({ success: "Post saved successfully" });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

// get posts
// Get posts by channelId
router.get('/studentget', async (req, res) => {
    try {
        const { channelId } = req.query;
        if (!channelId) {
            return res.status(400).json({ error: "Channel ID is required" });
        }
        const posts = await Posts.find({ channelId }).exec();
        if (posts.length === 0) {
            return res.status(404).json({ message: "No posts found for this channel ID" });
        }
        return res.status(200).json({ success: true, existingPosts: posts });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});


// get a specific post by ID
router.get("/student/:id", async (req, res) => {
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

// update post
router.put("/student/update/:id", async (req, res) => {
  try {
    await Posts.findByIdAndUpdate(req.params.id, { $set: req.body });
    return res.status(200).json({ success: "Post updated successfully" });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

// Delete a student by ID
router.delete("/student/delete/:id", async (req, res) => {
  try {
    const deletedPost = await Posts.findByIdAndDelete(req.params.id);
    if (!deletedPost) {
      return res.status(404).json({ message: "Student not found" });
    }
    res.status(200).json({ message: "Student deleted successfully" });
  } catch (error) {
    console.error("Error deleting student:", error);
    res.status(500).json({ message: "Internal Server Error", error: error.message });
  }
});




module.exports = router;
