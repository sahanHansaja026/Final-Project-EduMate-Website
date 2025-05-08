const express = require("express");
const multer = require("multer");
const mongoose = require("mongoose");
const Posts = require("../models/assignment");
const { bucket } = require("./firebase"); // ✅ Use shared config

const router = express.Router();
const storage = multer.memoryStorage();
const upload = multer({ storage });

router.post("/video/save", upload.single("video"), async (req, res) => {
  try {
    const { card_id, video_name, video_id } = req.body;
    const finalVideoId = video_id || new mongoose.Types.ObjectId().toString();

    if (!card_id || !video_name || !req.file) {
      return res.status(400).json({
        error: "All fields (card_id, video_name, video file) are required",
      });
    }

    const fileName = `videos/${finalVideoId}_${req.file.originalname}`;
    const file = bucket.file(fileName);

    await file.save(req.file.buffer, {
      metadata: { contentType: req.file.mimetype },
      public: true,
    });

    const videoUrl = `https://storage.googleapis.com/${bucket.name}/${file.name}`;

    const newVideo = new Posts({
      card_id,
      video_name,
      video_id: finalVideoId,
      video_url: videoUrl,
    });

    await newVideo.save();

    res.status(200).json({
      success: true,
      message: "Video uploaded and data saved successfully!",
    });
  } catch (error) {
    console.error("Error saving video:", error);
    res.status(500).json({ error: error.message });
  }
});


router.get("/video/:id", async (req, res) => {
  try {
    const videoId = req.params.id;
    const video = await Posts.findById(videoId).exec();
    if (!video) {
      return res
        .status(404)
        .json({ success: false, message: "Video not found" });
    }

    return res.status(200).json({ success: true, video });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

router.put(
  "/video/update/:video_id",
  upload.single("video"),
  async (req, res) => {
    try {
      const { video_id } = req.params; // Get video_id from the URL
      const { video_name } = req.body; // Get new video name from request body
      const { video_url } = req.body; // Current video URL if not uploading a new video
      let newVideoUrl = video_url; // Default to the existing video URL if no new file uploaded

      // Find the existing video in MongoDB by video_id
      const existingVideo = await Posts.findOne({ video_id });

      if (!existingVideo) {
        return res.status(404).json({ error: "Video not found" });
      }

      // If a new video file is uploaded, replace the old video in Firebase Storage
      if (req.file) {
        // Delete the old video from Firebase Storage
        const oldFileName = `videos/${existingVideo.video_id}_${existingVideo.video_name}`;
        const oldFile = bucket.file(oldFileName);

        try {
          await oldFile.delete(); // Delete old video from Firebase Storage
        } catch (error) {
          console.error("Error deleting old video:", error);
          return res
            .status(500)
            .json({ error: "Failed to delete the old video" });
        }

        // Upload the new video to Firebase Storage
        const newFileName = `videos/${video_id}_${req.file.originalname}`;
        const newFile = bucket.file(newFileName);

        await newFile.save(req.file.buffer, {
          metadata: {
            contentType: req.file.mimetype,
          },
          public: true, // Set to true for public access
        });

        // Generate the new public URL for the uploaded video
        newVideoUrl = `https://storage.googleapis.com/${bucket.name}/${newFile.name}`;
      }

      // Update the MongoDB document with the new video details
      const updatedVideo = await Posts.findOneAndUpdate(
        { video_id },
        {
          video_name: video_name || existingVideo.video_name, // Keep old name if not updated
          video_url: newVideoUrl, // Update video URL to the new one
        },
        { new: true } // Return the updated document
      );

      if (!updatedVideo) {
        return res.status(404).json({ error: "Video not found" });
      }

      return res.status(200).json({
        success: "Video updated successfully",
        updatedVideo,
      });
    } catch (error) {
      console.error("Error updating video:", error);
      return res.status(500).json({ error: error.message });
    }
  }
);

module.exports = router;
