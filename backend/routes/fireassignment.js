const express = require("express");
const Posts = require("../models/assignment");
const multer = require("multer");
const mongoose = require("mongoose");
const { bucket } = require("./firebase"); // ✅ Use shared bucket
const path = require("path");

const router = express.Router();

// Multer configuration
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Save assignment route
router.post(
  "/assignment/save",
  upload.single("assignment"),
  async (req, res) => {
    try {
      const { card_id, assignment_name, assignment_id } = req.body;
      const finalAssignmentId =
        assignment_id || new mongoose.Types.ObjectId().toString();

      if (!card_id || !assignment_name || !req.file) {
        return res.status(400).json({
          error:
            "All fields (card_id, assignment_name, assignment file) are required",
        });
      }

      const fileName = `assignment/${finalAssignmentId}_${req.file.originalname}`;
      const file = bucket.file(fileName);

      await file.save(req.file.buffer, {
        metadata: {
          contentType: req.file.mimetype,
        },
        public: true,
      });

      const assignmentUrl = `https://storage.googleapis.com/${bucket.name}/${file.name}`;

      const newAssignment = new Posts({
        card_id,
        assignment_name,
        assignment_id: finalAssignmentId,
        assignment_url: assignmentUrl,
      });

      await newAssignment.save();

      res.status(200).json({
        success: true,
        message: "Assignment uploaded and data saved successfully!",
      });
    } catch (error) {
      console.error("Error saving assignment:", error);
      res.status(500).json({ error: error.message });
    }
  }
);

// Get a specific assignment by ID
router.get("/assignment/:id", async (req, res) => {
  try {
    const postId = req.params.id;
    const post = await Posts.findById(postId).exec();

    if (!post) {
      return res
        .status(404)
        .json({ success: false, message: "Assignment not found" });
    }

    // Return the assignment URL and other details
    return res.status(200).json({
      success: true,
      post: {
        assignment_name: post.assignment_name,
        assignment_url: post.assignment_url, // <- Firebase download URL
        assignment_id: post.assignment_id,
        card_id: post.card_id,
      },
    });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});


module.exports = router;
