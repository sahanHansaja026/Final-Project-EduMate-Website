const mongoose = require("mongoose");

const postSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
  },
  owneremail: {
    type: String,
    required: true,
  },
  card_id: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  summery: {
    type: String,
    required: true,
  },
  image: {
    data: Buffer,
    contentType: String,
  },
  channel_id: {
    type: String,
    required: true,
  },
  tags: {
    type: String,
    require: true,
  },
});

module.exports = mongoose.model("chenalModules", postSchema);
