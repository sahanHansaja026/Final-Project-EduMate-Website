const express = require("express");
const Posts = require("../models/assignment");
const multer = require("multer");
const path = require("path");

const router = express.Router();

// Multer storage configuration for assignment upload
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (file.fieldname === "note") {
      cb(null, path.join(__dirname, "../Notes")); // Correct path for storing assignments
    } else {
      cb(new Error("Invalid fieldname"), null);
    }
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname)); // Unique file name with timestamp
  },
});

const upload = multer({ storage: storage });

// Route for saving an assignment
router.post(
  "/note/save",
  upload.single("note"), // Handle a single assignment upload
  async (req, res) => {
    try {
      const { card_id, note_name } = req.body;

      // Check if all required fields are provided
      if (!card_id || !note_name || !req.file) {
        return res.status(400).json({ error: "All fields are required" });
      }

      // Store the assignment file path
      const assignmentPath = req.file.filename;

      // Create a new post with the provided data
      const newPost = new Posts({
        card_id,
        note_name,
        note: assignmentPath,
      });

      // Save the post to the database
      await newPost.save();
      return res.status(200).json({ success: "Assignment saved successfully" });
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  }
);

// Get all assignments with pagination
router.get("/note", async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 8;
    const startIndex = (page - 1) * limit;

    const posts = await Posts.find()
      .sort({ createdAt: -1 }) // Sort by createdAt in descending order
      .skip(startIndex)
      .limit(limit)
      .exec(); // Get the latest posts first
    const totalPosts = await Posts.countDocuments();

    return res.status(200).json({
      success: true,
      existingPosts: posts,
      totalPosts,
    });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

// Get a specific assignment by ID
router.get("/note/:id", async (req, res) => {
  try {
    const postId = req.params.id;
    const post = await Posts.findById(postId).exec();
    if (!post) {
      return res
        .status(404)
        .json({ success: false, message: "Assignment not found" });
    }
    return res.status(200).json({ success: true, post });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

// Update assignment
router.put("/note/update/:id", async (req, res) => {
  try {
    await Posts.findByIdAndUpdate(req.params.id, { $set: req.body });
    return res.status(200).json({ success: "Assignment updated successfully" });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

module.exports = router;
