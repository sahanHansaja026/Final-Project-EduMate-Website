const express = require("express");
const Quiz = require("../models/CMS"); // Assuming you named your model 'assignment.js'
const Router = express.Router();

// Route to get assignment data based on CMS_id
Router.get('/cmsget/:CMS_id', async (req, res) => {
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

// get a specific question by ID
Router.get("/cmsid/:id", async (req, res) => {
  try {
    const postId = req.params.id;
    const post = await Quiz.findById(postId).exec();
    if (!post) {
      return res
        .status(404)
        .json({ success: false, message: "Post not found" });
    }
    return res.status(200).json({ success: true, post });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

// Get a single quiz post by MongoDB _id
Router.get("/cmsget/:id", async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ success: false, message: "Invalid ID" });
    }

    const post = await Quiz.findById(id).exec();

    if (!post) {
      return res.status(404).json({ success: false, message: "Post not found" });
    }

    return res.status(200).json({ success: true, post });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ success: false, message: "Server error" });
  }
});




module.exports = Router;
