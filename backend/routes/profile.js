const express = require("express");
const Posts = require("../models/profile");
const multer = require("multer");
const path = require("path");

const routerrees = express.Router();

// Configure multer for image uploads
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Route to save new profile with image
// Route to save new profile with image
routerrees.post(
  "/profile/save",
  upload.fields([{ name: "profileimage", maxCount: 1 }]),
  async (req, res) => {
    try {
      const { first_name, last_name, email, phone, DOB, job, about } = req.body;

      // Validate required fields
      if (
        !first_name ||
        !last_name ||
        !email ||
        !phone ||
        !job ||
        !DOB ||
        !about
      ) {
        return res.status(400).json({ error: "All fields are required" });
      }

      const imageFile = req.files.profileimage?.[0];

      const newPost = new Posts({
        first_name,
        last_name,
        email,
        phone,
        DOB,
        job,
        about,
        profileimage: imageFile
          ? {
              data: imageFile.buffer,
              contentType: imageFile.mimetype,
            }
          : null,
      });

      await newPost.save();
      return res.status(200).json({ success: "Profile saved successfully" });
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  }
);

// Route to get profile by email
routerrees.get("/profiles", async (req, res) => {
  try {
    const { email } = req.query;
    if (!email) {
      return res
        .status(400)
        .json({ success: false, message: "Email is required" });
    }

    const userProfile = await Posts.findOne({ email });

    if (!userProfile) {
      return res
        .status(404)
        .json({ success: false, message: "User not found" });
    }

    // Convert image buffer to base64 if it exists
    let userProfileWithImage = userProfile.toObject(); // clone to modify
    if (userProfile.profileimage && userProfile.profileimage.data) {
      userProfileWithImage.profileimage = `data:${
        userProfile.profileimage.contentType
      };base64,${userProfile.profileimage.data.toString("base64")}`;
    }

    return res.status(200).json({
      success: true,
      message: "User profile retrieved successfully",
      userProfile: userProfileWithImage,
    });
  } catch (error) {
    console.error("Error fetching user profile:", error.message);
    return res
      .status(500)
      .json({ success: false, message: "Internal server error" });
  }
});



routerrees.get("/profile/:id", async (req, res) => {
  try {
    const postId = req.params.id;

    const post = await Posts.findById(postId).exec();
    if (!post) {
      return res
        .status(404)
        .json({ success: false, message: "Profile not found" });
    }

    return res.status(200).json({ success: true, post });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});

routerrees.put(
  "/profile/update/email",
  upload.single("profileimage"),
  async (req, res) => {
    try {
      const { email, first_name, last_name, phone, DOB, job, about } = req.body;

      if (!email) {
        return res.status(400).json({ error: "Email is required" });
      }

      const updateData = {};
      if (first_name) updateData.first_name = first_name;
      if (last_name) updateData.last_name = last_name;
      if (phone) updateData.phone = phone;
      if (DOB) updateData.DOB = DOB;
      if (job) updateData.job = job;
      if (about) updateData.about = about;

      if (req.file) {
        updateData.profileimage = {
          data: req.file.buffer,
          contentType: req.file.mimetype,
        };
      }

      const updatedPost = await Posts.findOneAndUpdate(
        { email },
        { $set: updateData },
        { new: true }
      );

      if (!updatedPost) {
        return res
          .status(404)
          .json({ success: false, message: "User not found" });
      }

      return res.status(200).json({
        success: "Profile updated successfully",
        updatedPost,
      });
    } catch (error) {
      console.error("Error updating profile:", error.message);
      return res.status(500).json({ error: "Internal server error" });
    }
  }
);

// Route to get user profile summary (e.g., count students and admins)
routerrees.get("/userprofile/summary", async (req, res) => {
  try {
    const totalStudents = await Posts.countDocuments({ job: "Student" });
    const totalAdmins = await Posts.countDocuments({
      job: { $in: ["Teacher", "Lecturer"] },
    });
      if (req.file) {
        updateData.profileimage = {
          data: req.file.buffer,
          contentType: req.file.mimetype,
        };
      }
    return res.status(200).json({
      success: true,
      totalStudents,
      totalAdmins,
    });
    
  } catch (error) {
    console.error("Error fetching user summary:", error);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});

routerrees.get("/userprofile/summary/:email", async (req, res) => {
  try {
    const { email } = req.params;

    // Find the user profile by email
    const userProfile = await Posts.findOne({ email });

    if (!userProfile) {
      return res.status(404).json({ error: "User not found" });
    }

    // Prepare image in base64 format if available
    let imageData = "../client/src/images/default.png"; // Fallback if no image
    if (userProfile.profileimage && userProfile.profileimage.data) {
      imageData = `data:${
        userProfile.profileimage.contentType
      };base64,${userProfile.profileimage.data.toString("base64")}`;
    }

    // Return selected fields
    return res.status(200).json({
      success: true,
      first_name: userProfile.first_name,
      last_name: userProfile.last_name,
      job: userProfile.job,
      profileimage: imageData,
    });
  } catch (error) {
    console.error("Error fetching user profile:", error.message);
    return res.status(500).json({ error: "Server error, please try again" });
  }
});

module.exports = routerrees;
