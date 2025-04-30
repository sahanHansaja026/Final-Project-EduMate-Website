const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const postSchema = new Schema({
  card_id: {
    type: String,
  },
  email: {
    type: String,
  },
  message: {
    type: String,
  },
});
module.exports = mongoose.model("messages", postSchema);
