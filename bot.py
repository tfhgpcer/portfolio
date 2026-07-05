import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


# Загружаем переменные из файла .env для локального запуска.
# На хостинге Railway эта же переменная будет задана в панели проекта.
load_dotenv()


# Токен нельзя хранить прямо в коде: так его легко случайно показать другим.
# Поэтому бот читает его из переменной окружения BOT_TOKEN.
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Файл, куда будут сохраняться заявки пользователей.
ORDERS_FILE = Path("orders.txt")


# Состояния диалога /order: сначала спрашиваем имя, затем телефон.
ASK_NAME, ASK_PHONE = range(2)


# FAQ хранится в словаре: слева ключевое слово, справа ответ бота.
# Чтобы адаптировать бота под другой бизнес, достаточно изменить этот словарь.
FAQ = {
    "price": (
        "The price depends on the project. I usually estimate the cost after a "
        "short brief: scope of work, deadlines, and required features. Leave a "
        "request with /order, and I will contact you with a quote."
    ),
    "hours": (
        "Working hours: Monday to Friday, from 10:00 to 19:00. "
        "For urgent requests, I can reply in the evening by agreement."
    ),
    "address": (
        "I work online with clients from different cities. "
        "Meetings and calls are arranged in advance."
    ),
    "delivery": (
        "Final files and project materials are delivered online: by link, archive, "
        "Telegram, email, or another service convenient for the client."
    ),
}


# Настраиваем базовые логи, чтобы в консоли было видно запуск и возможные ошибки.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Убираем подробные HTTP-логи библиотек, чтобы в консоли случайно не показывался токен бота.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)


# Команда /start: приветствует пользователя и коротко объясняет возможности бота.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I am a freelancer portfolio bot.\n\n"
        "I can answer frequently asked questions by keywords: price, hours, "
        "address, delivery.\n"
        "I can also collect a client request with the /order command.\n\n"
        "To see the full list of commands, type /help."
    )


# Команда /help: показывает пользователю, что именно умеет бот.
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "What I can do:\n\n"
        "/start - greeting and short description\n"
        "/help - list of available features\n"
        "/order - leave a request\n\n"
        "You can also send a question with one of these keywords:\n"
        "- price\n"
        "- hours\n"
        "- address\n"
        "- delivery"
    )


# Команда /order: начинает диалог оформления заявки и спрашивает имя.
async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Let's create your request. What is your name?\n\n"
        "If you change your mind, type /cancel."
    )
    return ASK_NAME


# Первый шаг диалога: сохраняем имя во временную память пользователя.
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()

    if not name:
        await update.message.reply_text("Please send your name as text.")
        return ASK_NAME

    context.user_data["order_name"] = name
    await update.message.reply_text("Thank you! Now please send your phone number.")
    return ASK_PHONE


# Второй шаг диалога: получаем телефон, записываем заявку в orders.txt и завершаем диалог.
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = update.message.text.strip()

    if not phone:
        await update.message.reply_text("Please send your phone number.")
        return ASK_PHONE

    name = context.user_data.get("order_name", "Not specified")
    user = update.effective_user
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_line = (
        f"[{created_at}] "
        f"Name: {name}; "
        f"Phone: {phone}; "
        f"Telegram ID: {user.id}; "
        f"Username: @{user.username if user.username else 'not specified'}\n"
    )

    ORDERS_FILE.open("a", encoding="utf-8").write(order_line)
    context.user_data.pop("order_name", None)

    await update.message.reply_text(
        "Thank you! Your request has been saved. I will contact you soon."
    )
    return ConversationHandler.END


# Команда /cancel: позволяет пользователю выйти из оформления заявки.
async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("order_name", None)
    await update.message.reply_text(
        "The request has been canceled. If you want to leave a request later, type /order."
    )
    return ConversationHandler.END


# Обработка обычных сообщений: ищем ключевые слова из FAQ и отвечаем подходящим текстом.
async def answer_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.lower()

    for keyword, answer in FAQ.items():
        if keyword in user_text:
            await update.message.reply_text(answer)
            return

    await update.message.reply_text(
        "I could not find an exact answer to this question yet. "
        "Type /help to see what I can do, or leave a request with /order."
    )


# Главная функция: создает приложение, подключает обработчики команд и запускает бота.
def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN was not found. Add the token to the .env file "
            "or set it as an environment variable on your hosting."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    order_conversation = ConversationHandler(
        entry_points=[CommandHandler("order", order_start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel_order)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(order_conversation)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_faq))

    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
