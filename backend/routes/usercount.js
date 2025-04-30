const express = require("express");
const User = require("../models/student");

const router = express.Router();

router.get("/count", async (req, res) => {
  try {
    const count = await User.countDocuments({});
    res.status(200).json({ success: true, count });
  } catch (error) {
    console.error("Error fetching user count:", error);
    res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
