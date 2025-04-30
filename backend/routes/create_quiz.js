const express = require("express");
const Quiz = require("../models/assignment"); // Assuming you named your model 'quiz.js'
const Router = express.Router();

// Save quiz
Router.post("/quiz/save", (req, res) => {
  const { quiz_id } = req.body;  // Check for quiz_id uniqueness

  Quiz.findOne({ quiz_id })
    .then(existingQuiz => {
      if (existingQuiz) {
        return res.status(400).json({
          error: "Quiz ID already exists",
        });
      }

      const newQuiz = new Quiz(req.body);  // Create new Quiz with the data from request body
      return newQuiz.save();
    })
    .then(() => {
      return res.status(200).json({
        success: "Quiz saved successfully",
      });
    })
    .catch((err) => {
      return res.status(400).json({
        error: err.message,
      });
    });
});

module.exports = Router;
