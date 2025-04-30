const express = require('express');
const router = express.Router();
const Posts = require('../models/assignment'); // Replace with your model

// Route to fetch assignments based on card_id
router.get('/activities/:card_id', async (req, res) => {
  try {
    const cardId = req.params.card_id; 
    console.log("Card ID received:", cardId); // Check the card_id
    
    // Fetching posts related to card_id and sorting by createdAt (ascending)
    const posts = await Posts.find({ card_id: cardId })
                             .sort({ createdAt: 1 })  // Sort by createdAt field in ascending order
                             .exec();
    
    console.log("Posts found:", posts); // Log the results

    if (!posts || posts.length === 0) {
      return res.status(200).json({ success: true, posts: [] });
    }

    return res.status(200).json({ success: true, posts }); 
  } catch (error) {
    console.error("Error fetching posts:", error); 
    return res.status(500).json({ success: false, error: error.message }); 
  }
});


module.exports = router;
