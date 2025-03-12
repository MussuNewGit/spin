from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request, jsonify
import random
import threading

# Flask app for serving the web app
app = Flask(__name__)

# Telegram Bot Token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Web App URL (replace with your HTTPS URL)
WEB_APP_URL = "https://yourdomain.com"

# Command handler for /start
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Open Spin Wheel", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Spin Wheel Bot! Click below to open the spin wheel.", reply_markup=reply_markup)

# Handle web app data
@app.route('/spin', methods=['POST'])
def handle_spin():
    data = request.json
    chat_id = data.get('chatId')
    prize = data.get('prize')
    # Send the prize to the user
    bot.send_message(chat_id=chat_id, text=f"You won: {prize}")
    return jsonify({"status": "success"})

# Main function to start the bot and Flask server
def main():
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    flask_thread.daemon = True
    flask_thread.start()

    # Create the Telegram bot application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
