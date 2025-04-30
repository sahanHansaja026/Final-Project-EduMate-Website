const mongoose = require("mongoose");

const postSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
  phone: {
    type: String,
    required: true,
  },
  channelId: {
    type: String,
    required: true,
  },
  dateOfBirth: {
    type: String,
    required: true,
  },
});

module.exports = mongoose.model("chanel_subsribers", postSchema);
