const express = require("express");
const router = express.Router();
const Progress = require("../models/pogress"); // Ensure model name matches

router.post("/progress", async (req, res) => {
  const { email, activity_id } = req.body;

  if (!email || !activity_id) {
    return res.status(400).json({ success: false, message: "Email and activity ID are required" });
  }

  try {
    const progress = await Progress.findOneAndUpdate(
      { email, activity_id },
      { completed: true, date: new Date() },
      { upsert: true, new: true }
    );

    res.status(200).json({ success: true, message: "Progress updated", progress });
  } catch (error) {
    console.error("Error updating progress:", error);
    res.status(500).json({ success: false, message: "Internal server error" });
  }
});

// Fetch user activities by email and activity_id
router.get("/useractivities/:email/:activity_id", async (req, res) => {
  const { email, activity_id } = req.params;

  if (!email || !activity_id) {
    return res.status(400).json({ success: false, message: "Email and activity ID are required" });
  }

  try {
    const activity = await Progress.findOne({ email, activity_id });

    if (!activity) {
      return res.status(404).json({ success: false, message: "No activity found for the user" });
    }

    res.status(200).json({
      success: true,
      activity: {
        activity_id: activity.activity_id,
        completed: activity.completed,
        date: activity.date,
      },
    });
  } catch (error) {
    console.error("Error fetching user activity:", error);
    res.status(500).json({ success: false, message: "Internal server error" });
  }
});

module.exports = router;
