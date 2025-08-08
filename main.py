import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# ------------------ تنظیمات ------------------
BOT_TOKEN = "7926487692:AAHrGVT8be4oI29vIdhVnEQKeAcueS4491s"# از BotFather بگیر
OPENAI_API_KEY = "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"  # از OpenAI بگیر
MODEL_NAME = "gpt-3.5-turbo"  # میتونی gpt-4 بزاری اگه داری

# ------------------ لاگ‌گیری ------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

openai.api_key = OPENAI_API_KEY

# ------------------ دستورات ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 🤖\n"
        "من دستیار هوش مصنوعی هستم. هر چی بخوای می‌تونی ازم بپرسی.\n"
        "شروع کن!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 راهنما:\n"
        "فقط پیام بده، من جواب میدم.\n"
        "/start → شروع گفتگو\n"
        "/help → راهنما"
    )

# ------------------ پردازش پیام کاربر ------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    try:
        # درخواست به OpenAI
        completion = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "تو یک دستیار فارسی‌زبان هستی و باید پاسخ‌ها رو دوستانه بدی."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500,
            temperature=0.7
        )

        answer = completion.choices[0].message["content"].strip()
        await update.message.reply_text(answer)

    except Exception as e:
        logging.error(f"خطا: {e}")
        await update.message.reply_text("❌ مشکلی پیش اومد، بعداً دوباره امتحان کن.")

# ------------------ اجرای ربات ------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
