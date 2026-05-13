from telegram.ext import Updater, CommandHandler

TOKEN = "8729643272:AAGb3OZPU0TE1Q1uKsAitrctFwOdtsCMLXU"

def start(update, context):
    update.message.reply_text("Bot ishladi ✅")

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()


