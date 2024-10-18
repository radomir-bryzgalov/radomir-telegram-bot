import openai
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Устанавливаем API-ключ OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Функция для общения с GPT через новый API
def generate_gpt_response(prompt):
    try:
        # Передаем системное сообщение, чтобы модель знала, что она Telegram-бот
        system_message = {
            "role": "system",
            "content": "Ты Telegram-бот, созданный Радомиром Брызгаловым. Отвечай кратко и по существу, чтобы экономить данные."
        }
        user_message = {
            "role": "user",
            "content": prompt
        }
        # Запрос к GPT-3.5-turbo с контекстом и ограничением токенов
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message, user_message],
            max_tokens=50,  # Ограничиваем количество токенов для экономии данных
            temperature=0.5  # Низкая температура для кратких и точных ответов
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Ошибка при генерации ответа: {e}"

# Стартовая команда для бота
async def start(update: Update, context):
    await update.message.reply_text('Привет! Я Telegram-бот, созданный Радомиром Брызгаловым. Напиши мне вопрос, и я постараюсь ответить кратко и по существу!')

# Обработка сообщений от пользователя
async def handle_message(update: Update, context):
    user_message = update.message.text
    # Получаем ответ от GPT
    response = generate_gpt_response(user_message)
    await update.message.reply_text(response)

# Основной код для создания и запуска Telegram-бота
if __name__ == '__main__':
    # Используй свой Telegram-токен
    app = ApplicationBuilder().token("7808928669:AAH_nqVRa9H7dfbh6pgrLl-ArSKcEg-ZirQ").build()

    # Команды и обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    app.run_polling()
