const mongoose = require("mongoose");

const portfolioSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  
  symbol: String,
  predicted: Number,
  actual: Number, // optional - update later
  date: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("Portfolio", portfolioSchema);
