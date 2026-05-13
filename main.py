from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8729643272:AAGb3OZPU0TE1Q1uKsAitrctFwOdtsCMLXU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🥊 Assalomu alaykum!\nUmidov Boks Clubi botiga xush kelibsiz."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
