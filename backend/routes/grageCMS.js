const express = require("express");
const router = express.Router();
const Score = require("../models/cmsscores");

// POST endpoint for submitting scores
router.post("/submitmark", (req, res) => {
  console.log("Received Payload:", req.body);

  const { score_id, email, CMS_id, score } = req.body;

  // Validate that the required fields are present and score is a valid number
  if (!score_id || !email || !CMS_id || score == null || isNaN(score)) {
    console.log("Validation failed: Missing or invalid fields.");
    return res.status(400).json({ error: "Invalid or missing fields" });
  }

  const newScore = new Score({
    score_id,
    email,
    CMS_id,
    score,
  });

  newScore
    .save()
    .then(() => {
      return res.status(200).json({ success: "Score saved successfully" });
    })
    .catch((err) => {
      console.error("Error saving score:", err);
      return res.status(400).json({ error: err.message });
    });
});


// GET /getscore/:CMS_id
// GET /getscore?CMS_id=xxx
router.get("/getscore", async (req, res) => {
  const { CMS_id } = req.query;

  if (!CMS_id) {
    return res.status(400).json({ message: "CMS_id is required" });
  }

  try {
    const scores = await Score.find({ CMS_id });

    if (scores.length === 0) {
      return res.status(404).json({ message: "No scores found for the given CMS_id" });
    }

    res.status(200).json({ scores });
  } catch (error) {
    console.error("Error fetching scores:", error);
    res.status(500).json({ message: "Server error while fetching scores" });
  }
});


router.get("/getscore/:CMS_id/:email", async (req, res) => {
  const { CMS_id, email } = req.params;

  if (!CMS_id || !email) {
    return res.status(400).json({ message: "CMS_id and email are required" });
  }

  try {
    const scoreDoc = await Score.findOne({ CMS_id, email });

    if (!scoreDoc) {
      return res
        .status(404)
        .json({ message: "Score not found for the given CMS_id and email" });
    }

    res.status(200).json({ score: scoreDoc.score }); // ✅ Corrected key
  } catch (error) {
    console.error("Error fetching score:", error);
    res.status(500).json({ message: "Server error while fetching score" });
  }
});

// PUT /updatescore?CMS_id=xxx&email=yyy
router.put("/updatescore", async (req, res) => {
  const { email, CMS_id, newScore } = req.body;

  if (!email || !CMS_id || newScore === undefined) {
    return res.status(400).json({ message: "Missing required fields" });
  }

  try {
    // Update the score in the database
    const updatedScore = await Score.findOneAndUpdate(
      { CMS_id, email },  // Find by CMS_id and email
      { score: newScore },  // Update the score field
      { new: true }         // Return the updated document
    );

    if (!updatedScore) {
      return res.status(404).json({ message: "Score not found" });
    }

    res.status(200).json({ score: updatedScore });
  } catch (error) {
    console.error("Error updating score:", error);
    res.status(500).json({ message: "Server error while updating score" });
  }
});



module.exports = router;
