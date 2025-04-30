// models/Enrollment.js
const mongoose = require("mongoose");

const enrollmentSchema = new mongoose.Schema({
  card_id: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
  date: {
    type: Date,
    default: Date.now, // Automatically store the current date and time
  },
});

// Add a unique compound index to prevent duplicate enrollments for the same course and user
enrollmentSchema.index({ card_id: 1, email: 1 }, { unique: true });

const Enrollment = mongoose.model("Enrollment", enrollmentSchema);

module.exports = Enrollment;
