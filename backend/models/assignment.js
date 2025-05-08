const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const postSchema = new Schema({
  card_id: {
    type: String,
  },
  assignment_name: {
    type: String,
  },
  assignment_url: {
    type: String,
  },
  assignment: {
    type: String,
  },
  assignment_id: {
    type: String,
  },
  note_name: {
    type: String,
  },
  note: {
    type: String,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  video_name: {
    type: String,
  },
  video_url: {
    type: String,
  },
  video_id: {
    type: String,
  },
  quiz_id: {
    type: String,
  },
  quiz_name: {
    type: String,
  },
  description: {
    type: String,
  },
  timeDuration: {
    type: String,
  },
  attempt: {
    type: String,
  },
  CMS_id: {
    type: String,
  },
  CMS_name: {
    type: String,
  },
  article_name: {
    type: String,
  },
  content: {
    type: String,
  },
  article_id: {
    type: String,
  },
});

module.exports = mongoose.model("Assignment_details", postSchema);
