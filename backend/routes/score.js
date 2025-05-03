const express = require("express");
const Score = require("../models/score");
const router = express.Router();

// Route to save score
router.post("/score/save", async (req, res) => {
  const { quizId, score, username, email } = req.body;

  try {
    const newScore = new Score({
      quizId,
      score,
      username,
      email,
    });
    await newScore.save();
    res.status(201).json({ message: "Score saved successfully!" });
  } catch (error) {
    if (error.code === 11000) {
      res
        .status(400)
        .json({
          error: "The combination of Card ID and Username already exists",
        });
    } else {
      res.status(500).json({ error: "Failed to save score" });
    }
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


module.exports = router;
