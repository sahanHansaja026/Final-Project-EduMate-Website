// routes/messageRoutes.js
const express = require("express");
const router = express.Router();
const Message = require("../models/message");

// Route for saving a message
router.post("/saveMessage", async (req, res) => {
  const { card_id, email, message } = req.body;

  try {
    // Create a new message document in MongoDB
    const newMessage = new Message({
      card_id,
      email,
      message,
    });

    // Save the message to the database
    await newMessage.save();

    // Return success response
    res.status(201).json({
      success: true,
      message: "Message saved successfully",
      data: newMessage,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: "Error saving message",
      error: error.message,
    });
  }
});
// Route for getting messages by card_id
router.get("/getMessages/:card_id", async (req, res) => {
  const { card_id } = req.params; // Get the card_id from the request parameters

  try {
    // Find messages that match the card_id
    const messages = await Message.find({ card_id });

    if (messages.length === 0) {
      return res.status(404).json({
        success: false,
        message: "No messages found for this card_id",
      });
    }

    // Return the messages in the response
    res.status(200).json({
      success: true,
      messages,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: "Error retrieving messages",
      error: error.message,
    });
  }
});


module.exports = router;
