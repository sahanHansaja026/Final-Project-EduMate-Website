const express = require("express");
const Score = require("../models/score");
const router = express.Router();

// Save or update a user's score for a quiz
router.post("/score/save", async (req, res) => {
  try {
    const quizId = req.body.quizId?.trim();
    const score = req.body.score;
    const username = req.body.username?.trim();
    const email = req.body.email?.trim().toLowerCase(); // normalize email

    if (!quizId || !score || !username || !email) {
      return res.status(400).json({ error: "All fields are required" });
    }

    // Check for existing score with same quizId and email
    const existingScore = await Score.findOne({ quizId, email });

    if (existingScore) {
      // Update existing
      existingScore.score = score;
      existingScore.username = username; // Optional
      await existingScore.save();
      return res.status(200).json({ message: "Score updated successfully!" });
    } else {
      // Create new
      const newScore = new Score({ quizId, score, username, email });
      await newScore.save();
      return res.status(201).json({ message: "Score saved successfully!" });
    }
  } catch (error) {
    console.error("Score save error:", error);
    return res.status(500).json({ error: "Failed to save or update score" });
  }
});

// Route to get all scores by quizId
router.get("/score/quiz/:quizId", async (req, res) => {
  const { quizId } = req.params;

  try {
    // Find scores with the matching quizId
    const scores = await Score.find({ quizId });

    if (scores.length === 0) {
      return res.status(200).json({ message: "No scores found for this quiz" });
    }

    res.status(200).json(scores);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch scores" });
  }
});


// Route to get top 5 most used cardId
router.get("/top-card-ids", async (req, res) => {
  try {
    const topCardIds = await Score.aggregate([
      {
        // Group by cardId and count occurrences
        $group: {
          _id: "$cardId",
          count: { $sum: 1 },
        },
      },
      {
        // Sort by count in descending order
        $sort: { count: -1 },
      },
      {
        // Limit to top 5
        $limit: 5,
      },
    ]);

    res.status(200).json(topCardIds);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch top card IDs" });
  }
});

router.get("/getquizscore/:quizId/:email", async (req, res) => {
  const { quizId, email } = req.params;

  if (!quizId || !email) {
    return res.status(400).json({ message: "quizId and email are required" });
  }

  try {
    const scoreDoc = await Score.findOne({ quizId, email });

    if (!scoreDoc) {
      return res
        .status(404)
        .json({ message: "Score not found for the given quizId and email" });
    }

    res.status(200).json({ score: scoreDoc.score }); // ✅ Corrected key
  } catch (error) {
    console.error("Error fetching score:", error);
    res.status(500).json({ message: "Server error while fetching score" });
  }
});

module.exports = router;
