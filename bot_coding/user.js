const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    id: {
        type: Number,
        required: true,
        trim: true,
    },
    fname: {
        type: String,
        required: true,
        trim: true,
    },
    feedback: {
        type: String,
        required: true,
        trim: true,
    },
    username: {
        type: String,
        required: false,
        trim: true,
    },
    numberWarnings: {
        type: Number,
        required: true,
        trim: true,
        default: 0,
    },
    timeout: {
        type: Number,
        required: false,
        trim: true,
    },
});

const User = mongoose.model("User", userSchema);
module.exports = User;