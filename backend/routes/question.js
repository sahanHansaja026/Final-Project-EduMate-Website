const express = require("express");
const Posts = require('../models/question');

const router = express.Router();

// save questions
router.post('/question/save', async (req, res) => {
    try {
        let newPost = new Posts(req.body);
        await newPost.save();
        return res.status(200).json({ success: "Post saved successfully" });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});

// get question
router.get('/get_question', async (req, res) => {
    try {
        const posts = await Posts.find().exec();
        return res.status(200).json({ success: true, existingPosts: posts });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});

// get a specific question by ID
router.get('/question/:id', async (req, res) => {
    try {
        const postId = req.params.id;
        const post = await Posts.findById(postId).exec();
        if (!post) {
            return res.status(404).json({ success: false, message: "Post not found" });
        }
        return res.status(200).json({ success: true, post });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});


// update question
router.put('/question/update/:id', async (req, res) => {
    try {
        await Posts.findByIdAndUpdate(req.params.id, { $set: req.body });
        return res.status(200).json({ success: "Post updated successfully" });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});

// delete question
router.delete('/question/delete/:id', async (req, res) => {
    try {
        const deletedPost = await Posts.findByIdAndRemove(req.params.id);
        if (!deletedPost) {
            return res.status(404).json({ message: "Post not found" });
        }
        return res.json({ message: "Post deleted successfully", deletedPost });
    } catch (error) {
        return res.status(400).json({ message: "Error deleting post", error: error.message });
    }
});

// Get all posts by quiz_id
router.get("/post/quiz/:quiz_id", async (req, res) => {
  try {
    const quizId = req.params.quiz_id;
    console.log("Incoming quiz_id:", quizId);

    const posts = await Posts.find({ quiz_id: quizId });

    if (posts.length === 0) {
      return res.status(404).json({ success: false, message: "No posts found for this quiz_id" });
    }

    return res.status(200).json({ success: true, posts });
  } catch (error) {
    console.error("Error fetching posts:", error);
    return res.status(500).json({ success: false, message: "Server error", error: error.message });
  }
});

// Delete a post by post_id
router.delete("/post/delete/:postId", async (req, res) => {
  try {
    const { postId } = req.params;
    await Posts.findByIdAndDelete(postId);
    return res.status(200).json({ message: "Post deleted successfully" });
  } catch (error) {
    console.error("Error deleting post:", error);
    return res.status(500).json({ message: "Server error", error: error.message });
  }
});

// Get all posts by card_id
router.get('/post/card/:quiz_id', async (req, res) => {
    try {
        const quizId = req.params.quiz_id; 
        const posts = await Posts.find({ quiz_id: quizId }).exec(); 
        
        if (posts.length === 0) {
            return res.status(404).json({ success: false, message: "No posts found" });
        }
        return res.status(200).json({ success: true, posts }); 
    } catch (error) {
        console.error(error); 
        return res.status(500).json({ success: false, error: error.message }); 
    }
});




module.exports = router;
