const express = require("express");
const Quiz = require("../models/CMS"); // Assuming you named your model 'assignment.js'
const Router = express.Router();

// Route to save assignment
Router.post("/save-assignment", async (req, res) => {
  const { email, CMS_id, content } = req.body;

  if (!email || !CMS_id || !content) {
    return res.status(400).json({ success: false, message: "All fields are required." });
  }

  try {
    const assignment = new Quiz({ email, CMS_id, content }); // Use 'Quiz' as per the model import
    await assignment.save();
    res.status(201).json({ success: true, message: "Assignment saved successfully!" });
  } catch (error) {
    console.error("Error saving assignment:", error);
    res.status(500).json({ success: false, message: "Failed to save assignment." });
  }
});

// Route to get all assignments for the teacher
Router.get("/cms/assignments", async (req, res) => {
  try {
    const assignments = await Quiz.find();
    res.status(200).json({ success: true, assignments });
  } catch (error) {
    console.error("Error fetching assignments:", error);
    res.status(500).json({ success: false, message: "Failed to load assignments." });
  }
});

module.exports = Router;
