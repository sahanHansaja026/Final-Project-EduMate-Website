const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const postSchema = new Schema({
  card_id: {
    type: String,
    required: true,
  },
  video_name: {
    type: String,
    required: true,
  },
  video_id: {
    type: String,
    required: true,
  },
  video: {
    type: String,
    required: true, // Since an assignment file is mandatory
  },
  createdAt: {
    type: Date,
    default: Date.now, // Automatically set the current date and time
  },
});

module.exports = mongoose.model("Assignment_details", postSchema);
