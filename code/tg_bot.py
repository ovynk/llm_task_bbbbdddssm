import logging
import load_llm

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


API_KEY = '7343634046:AAG9GYyHvxSnvXbH_jpHTFMnWYy0XTejA6Y'
chat_engine = load_llm.load_chat_engine('../output/enhance_data_indexed')

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}. I have small database of car sellers. "
        rf'Ask me something about it and I will try tell you. Use /clear to clear LLM chat history',
        reply_markup=ForceReply(selective=True),
    )


async def clear_chat_llm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_engine.reset()
    await update.message.reply_text('History is cleaned')


async def llm_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(chat_engine.chat(update.message.text).response)


def main() -> None:
    application = Application.builder().token(API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear_chat_llm))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, llm_response))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
