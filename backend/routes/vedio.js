const express = require("express");
const Posts = require("../models/assignment"); // Assuming you have a Video model
const multer = require("multer");
const path = require("path");

const router = express.Router();

// Multer storage configuration for video upload
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Store videos in 'client/src/Videos' folder
    if (file.fieldname === "video") {
      cb(null, path.join(__dirname, "../Vedios")); // Correct path for storing videos
    } else {
      cb(new Error("Invalid fieldname"), null); // Reject invalid fieldnames
    }
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname)); // Unique filename based on timestamp
  },
});

const upload = multer({ storage: storage });

// Route for saving a video
router.post(
  "/video/sav",
  upload.single("video"), // Handle a single video upload
  async (req, res) => {
    try {
      const { card_id, video_name, video_id } = req.body;

      // Check if all required fields are provided
      if (!card_id || !video_name || !video_id|| !req.file) {
        return res.status(400).json({ error: "All fields are required" });
      }

      // Store the video file path (filename)
      const videoPath = req.file.filename;

      // Create a new video post
      const newVideo = new Posts({
        card_id,
        video_name,
        video_id,
        video: videoPath, // Store the file name or relative path in the database
      });

      // Save the video to the database
      await newVideo.save();
      return res.status(200).json({ success: "Video saved successfully" });
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  }
);

// Get all videos with pagination
router.get("/video", async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 8;
    const startIndex = (page - 1) * limit;

    const videos = await Posts.find()
      .sort({ createdAt: -1 }) // Sort videos by creation date in descending order
      .skip(startIndex)
      .limit(limit)
      .exec(); // Get the latest videos first
    const totalVideos = await Posts.countDocuments();

    return res.status(200).json({
      success: true,
      existingVideos: videos,
      totalVideos,
    });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});



// Route to retrieve video details
router.put(
  "/video/updatet/:video_id",
  upload.single("video"),
  async (req, res) => {
    try {
      const { video_id } = req.params; // Get video_id from the URL
      const { video_name } = req.body;
      let videoPath = req.body.video_path; // Existing video path if no new file is uploaded

      // If a new video file is uploaded, update the video path
      if (req.file) {
        videoPath = req.file.filename;
      }

      // Find and update the video by video_id
      const updatedVideo = await Posts.findOneAndUpdate(
        { video_id: video_id }, // Use video_id to find the video
        {
          video_name: video_name || undefined,
          video: videoPath || undefined,
        },
        { new: true } // Return the updated document
      );

      if (!updatedVideo) {
        return res.status(404).json({ error: "Video not found" });
      }

      return res
        .status(200)
        .json({ success: "Video updated successfully", updatedVideo });
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  }
);



// Update video details
router.delete("/video/delete/:video_id", async (req, res) => {
  try {
    const { video_id } = req.params; // Get video_id from the URL

    // Find and delete the video by video_id
    const video = await Posts.findOneAndDelete({ video_id: video_id });

    if (!video) {
      return res.status(404).json({ error: "Video not found" });
    }

    // Delete the video file from the server (if needed)
    const videoPath = path.join(__dirname, "../Videos", video.video); // Assuming your video files are stored in the 'Videos' folder
    fs.unlinkSync(videoPath); // Synchronously delete the video file from the server

    return res.status(200).json({ success: "Video deleted successfully" });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});


router.get("/video/get/:video_id", async (req, res) => {
  try {
    const { video_id } = req.params; // Get video_id from the URL

    // Find the video by video_id
    const video = await Posts.findOne({ video_id: video_id });

    if (!video) {
      return res.status(404).json({ error: "Video not found" });
    }

    return res.status(200).json(video); // Return the video details
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});







module.exports = router;
