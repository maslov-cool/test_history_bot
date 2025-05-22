# Импортируем необходимые классы.
# @test_by_coding_lover_bot --> ник в тг
import logging
import random
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
import json


logger = logging.getLogger(__name__)
BOT_TOKEN = '7959374624:AAF30eaeCvVPbBt8aAR9u8IrHKneCn8LNtM'

A = []
with open('history_test.json', encoding='utf-8') as cat_file:
    data = json.load(cat_file)
for key, value in data.items():
    for i in value:
        A.append([i['question'], i['response'].lower()])
print(A)
random.shuffle(A)
print(A)

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


async def start(update, context):
    context.user_data['index'] = 0
    context.user_data['count'] = 0
    await update.message.reply_text(f'''👋 Привет! Готов проверить свои знания по истории?

📋 Я задам тебе 10 вопросов. Отвечай на них в чате — узнаем, насколько ты хорошо знаешь историю!
Напиши /stop, чтобы выйти.
❓ Вопрос {context.user_data['index'] + 1}/10:
{A[context.user_data['index']][0]}
''')
    return 1


async def get_next_question(update, context):
    text = update.message.text.lower()
    if text == A[context.user_data['index']][1]:
        await update.message.reply_text(f'''✅ Отлично!''')
        if context.user_data['index'] + 1 < len(A):
            context.user_data['index'] += 1
            context.user_data['count'] += 1
            await update.message.reply_text(f'''Продолжаем:
❓ Вопрос {context.user_data['index'] + 1}/10:
✍️{A[context.user_data['index']][0]}''')
            return 1
        else:
            await update.message.reply_text(f'''🎉 Тест завершён!
Ты набрал: {context.user_data['count']} из 10 баллов.
🔁 Хочешь попробовать ещё раз? Напиши /start
❌ Или завершить — /stop
''')
            return 1
    else:
        await update.message.reply_text(f'''❌ Увы, правильный ответ: {A[context.user_data['index']][1]}''')
        context.user_data['index'] += 1
        if context.user_data['index'] < len(A):
            await update.message.reply_text(f'''Продолжаем:
❓ Вопрос {context.user_data['index'] + 1}/10:
✍️{A[context.user_data['index']][0]}''')
        else:
            await update.message.reply_text(f'''🎉 Тест завершён!
Ты набрал: {context.user_data['count']} из 10 баллов.
🔁 Хочешь попробовать ещё раз? Напиши /start
❌ Или завершить — /stop''')


async def stop(update, context):
    await update.message.reply_text('''👋 До встречи!
Возвращайся /start, когда захочешь снова проверить свои знания.
''')
    return ConversationHandler.END


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_next_question),
                CommandHandler('stop', stop)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
