const mongoose = require("mongoose");

const cmsscoreSchema = new mongoose.Schema(
  {
    email: String,
    CMS_id: String,
    score: Number,
    score_id: String,
  },
  {
    collection: "scores", // 👈 use the same collection name
  }
);

module.exports =
  mongoose.models.CMSScore || mongoose.model("cmsscores", cmsscoreSchema);
