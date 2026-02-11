import json
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

with open("statements.json", "r", encoding="utf-8") as f:
    STATEMENTS = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Official Political Reference Bot.\nAsk a question."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()

    for s in STATEMENTS:
        if any(tag in query for tag in s["tags"]):
            await update.message.reply_text(
                f"{s['answer']}\n\n— {s['date']}"
            )
            return

    await update.message.reply_text("No official position recorded on that.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
