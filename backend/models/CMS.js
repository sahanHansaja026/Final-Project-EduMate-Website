const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const postSchema = new Schema({
  CMS_id: {
    type: String,
  },
  content: {
    type: String,
  },
  email: {
    type: String,
  },
});
module.exports = mongoose.model("CMS_DEATAILS", postSchema);
