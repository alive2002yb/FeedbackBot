const mongoose = require("mongoose");
const pkg = require("telegraf");
const { Telegraf } = pkg;
const User = require("./user.js");
const fetch = require("node-fetch");
const { spawn } = require('child_process');

const BOT_TOKEN = `5995777962:AAFTx2BlzU2eqY7iI-gfGWmDAAcl9fWYYaM`;
const DB = `mongodb+srv://admin:admin@cluster0.wevqxmd.mongodb.net/?retryWrites=true&w=majority`;
mongoose
    .connect(DB, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .then(() => console.log("DB connection successful!"));

const bot = new Telegraf(BOT_TOKEN);

let prevMessageId = null;

function deletePreviousMessage(prevMessageId, chatID, currentMessageID) {
    if (prevMessageId) {
        ctx.deleteMessage(prevMessageId, chatID).catch((e) => console.log(e));
        console.log("Reached here");
    }
    prevMessageId = currentMessageID;
}
let data = '';

function runPythonScript(arg) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python3', ['-u', 'app.py', arg])
        pythonProcess.stdout.on('data', (chunk) => {
            data = chunk.toString();
        });
        pythonProcess.stderr.on('data', (error) => {
            reject(error.toString());
        });
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve(data);
            } else {
                reject(`Process exited with code: ${code}`);
            }
        });
    });
}

bot.start((ctx) => {
    ctx.reply(`Hi ${ctx.message.from.first_name}! Welcome to Feedback Bot , Please provide your feedback`);
    deletePreviousMessage(
        prevMessageId,
        ctx.message.chat.id,
        ctx.message.message_id
    );
});

bot.on("sticker", (ctx) => ctx.reply("Don't send me stickers! I can't understand them🥺"));

bot.on("text", async(ctx) => {
    const user = await User.findOne({ id: ctx.message.from.id });
    if (user === null) {
        try {
            const newUser = new User({
                id: ctx.message.from.id,
                fname: ctx.message.from.first_name,
                username: ctx.message.from.username,
                numberWarnings: 0,
            });
            await newUser.save();
            console.log("User Saved");
        } catch (e) {
            console.log(e);
        }
    } else {
        const currentUser = await User.findOne({ id: ctx.message.from.id });
        try {

            const prediction = await runPythonScript(ctx.message.text);
            console.log(ctx.message.text);
            result = parseInt(prediction.toString());
            if (result == 0) {
                currentUser.numberWarnings++;
                ctx.reply(`Please refrain from using Hatespeech 🚫⛔\nNumber of Warnings: ${currentUser.numberWarnings}\nFeedback not recieved`);
                ctx
                    .deleteMessage(ctx.message.message_id, ctx.message.chat.id)
                    .catch((e) => console.log(e));
                deletePreviousMessage(prevMessageId, ctx.message.chat.id, ctx.message.message_id);
            } else if (result == 1) {
                currentUser.numberWarnings++;
                ctx.reply(`Please refrain from using Abusive languages 🚫⛔\nNumber of Warnings: ${currentUser.numberWarnings}\nFeedback not recieved`);
                ctx
                    .deleteMessage(ctx.message.message_id, ctx.message.chat.id)
                    .catch((e) => console.log(e));

                deletePreviousMessage(prevMessageId, ctx.message.chat.id, ctx.message.message_id);
            } else if (result == 2) {
                currentUser.feedback = ctx.message.text;
                ctx.reply(`Thank you for your valuable feedback😃`);
            } else {
                ctx.reply(`Could not understand input😖`);
            }
        } catch (error) {
            console.log(error);
        }
        await currentUser.save();
    }
});
bot.launch();