const express = require("express");
const Posts = require("../models/assignment");
const multer = require("multer");
const mongoose = require("mongoose");

const path = require("path");

const router = express.Router();

// Multer storage configuration for assignment upload
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (file.fieldname === "assignment") {
      cb(null, path.join(__dirname, "../Assignments")); // Correct path for storing assignments
    } else {
      cb(new Error("Invalid fieldname"), null);
    }
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname)); // Unique file name with timestamp
  },
});

const upload = multer({ storage: storage });


// Get all assignments with pagination
router.get("/assignment", async (req, res) => {
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
router.get("/assignment/:id", async (req, res) => {
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



router.get("/assignment/get/:assignment_id", async (req, res) => {
  try {
    const { assignment_id } = req.params; // Get assignment_id from the URL

    // Find the video by video_id
    const Assignment = await Posts.findOne({ assignment_id: assignment_id });

    if (!Assignment) {
      return res.status(404).json({ error: "assignment not found" });
    }

    return res.status(200).json(Assignment); // Return the video details
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

router.put(
  "/assignment/update/:assignment_id",
  upload.single("assignment"), // Handles the assignment file
  async (req, res) => {
    try {
      const { assignment_id } = req.params;
      const { card_id, assignment_name } = req.body;

      // Validate input
      if (!assignment_id || !card_id || !assignment_name) {
        return res.status(401).json({ error: "All fields are required" });
      }

      // Find the existing assignment by assignment_id
      const existingAssignment = await Posts.findOne({ assignment_id });
      if (!existingAssignment) {
        return res.status(404).json({ error: "Assignment not found" });
      }

      let updatedAssignmentPath = existingAssignment.assignment; // Default to the current file path

      // If a new file is uploaded, handle the file update
      if (req.file) {
        const newFilePath = req.file.filename;

        // Delete the old file
        const oldFilePath = path.join(
          __dirname,
          "../Assignments",
          existingAssignment.assignment
        );
        fs.unlink(oldFilePath, (err) => {
          if (err) {
            console.error("Error deleting old file:", err);
          } else {
            console.log("Old file deleted successfully:", oldFilePath);
          }
        });

        // Update the file path
        updatedAssignmentPath = newFilePath;
      }

      // Update the assignment in the database
      existingAssignment.card_id = card_id;
      existingAssignment.assignment_name = assignment_name;
      existingAssignment.assignment = updatedAssignmentPath;

      // Save the updated record
      await existingAssignment.save();

      return res
        .status(200)
        .json({ success: "Assignment updated successfully" });
    } catch (error) {
      console.error("Error updating assignment:", error);
      return res.status(500).json({ error: error.message });
    }
  }
);

// Delete assignment route
router.delete("/assignment/delete/:assignment_id", async (req, res) => {
  try {
    const { assignment_id } = req.params;

    // Validate input
    if (!assignment_id) {
      return res.status(400).json({ error: "assignment_id is required" });
    }

    // Find the assignment by assignment_id
    const assignment = await Posts.findOne({ assignment_id });
    if (!assignment) {
      return res.status(404).json({ error: "Assignment not found" });
    }

    // Delete the file from storage if it exists
    const filePath = path.join(
      __dirname,
      "../Assignments",
      assignment.assignment
    );
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error("Error deleting file:", err);
      } else {
        console.log("File deleted successfully:", filePath);
      }
    });

    // Remove the database record
    await Posts.deleteOne({ assignment_id });
    return res.status(200).json({ success: "Assignment deleted successfully" });
  } catch (error) {
    console.error("Error deleting assignment:", error);
    return res.status(500).json({ error: error.message });
  }
});

module.exports = router;
