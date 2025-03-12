from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, jsonify
import threading
import os

# Flask app for serving the web app
app = Flask(__name__)

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8133253468:AAGrb9l3pk_Mh5t23XempObkmFmxtIRpXZA")

# Dynamic Web App URL (Set this in Render)
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://yourdomain.com")

# Home route to confirm Flask is working
@app.route('/')
def home():
    return "Flask Server is Running 🚀"

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Open Spin Wheel", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Spin Wheel Bot! Click below to open the spin wheel.", reply_markup=reply_markup)

# Handle web app data (spin results)
@app.route('/spin', methods=['POST'])
def handle_spin():
    data = request.json
    chat_id = data.get('chatId')
    prize = data.get('prize')

    if not chat_id or not prize:
        return jsonify({"error": "Missing chatId or prize"}), 400

    # Send the prize to the user
    application.bot.send_message(chat_id=chat_id, text=f"🎉 You won: {prize} 🎉")
    return jsonify({"status": "success"})

# Main function to start the bot and Flask server
def main():
    global application  # Make application accessible in Flask

    # Get Render-assigned port
    port = int(os.getenv("PORT", 5000))

    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": port})
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
