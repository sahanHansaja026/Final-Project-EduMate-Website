const mongoose = require("mongoose");

const scoreSchema = new mongoose.Schema(
  {
    quizId: {
      type: String,
      required: true,
    },
    score: {
      type: Number,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    email: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
    collection: "scores",
  }
);

// ❌ This line was causing the error
// scoreSchema.index({ cardId: 1, username: 1 });

const Score = mongoose.model("Score", scoreSchema);
module.exports = Score;
