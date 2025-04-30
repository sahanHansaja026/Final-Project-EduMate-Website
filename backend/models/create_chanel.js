const mongoose = require("mongoose");

const postSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
  },
  chenal_id: {
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
});

module.exports = mongoose.model("Chenal", postSchema);
