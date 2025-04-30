const express = require("express");
const Quiz = require("../models/assignment"); // Assuming you named your model 'assignment.js'
const Router = express.Router();

// Save quiz
Router.post("/cms/save", (req, res) => {
  const { CMS_id, card_id, CMS_name, description } = req.body; // Adjusted for new data structure

  // Check for CMS_id uniqueness
  Quiz.findOne({ CMS_id })
    .then((existingQuiz) => {
      if (existingQuiz) {
        return res.status(400).json({
          error: "CMS ID already exists",
        });
      }

      const newQuiz = new Quiz({
        CMS_id,
        card_id,
        CMS_name,
        description,
      }); // Create new Quiz with the updated data structure

      return newQuiz.save();
    })
    .then(() => {
      return res.status(200).json({
        success: "CMS assignment saved successfully",
      });
    })
    .catch((err) => {
      return res.status(400).json({
        error: err.message,
      });
    });
});


// Get quiz by CMS_id route

// Route to get assignment data based on CMS_id
Router.get('/cms/:CMS_id', async (req, res) => {
  try {
    const CMS_id = req.params.CMS_id; 
    console.log("Received CMS_id:", CMS_id);
    
    // Find posts associated with the given CMS_id
    const posts = await Quiz.find({ CMS_id: CMS_id }).exec(); 
    console.log("Posts found:", posts);
    
    // Check if posts are found
    if (posts.length === 0) {
      return res.status(404).json({ success: false, message: "No posts found" });
    }
    
    // Respond with the posts found
    return res.status(200).json({ success: true, posts }); 
  } catch (error) {
    console.error(error); 
    return res.status(500).json({ success: false, error: error.message }); 
  }
});



module.exports = Router;
