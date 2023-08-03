TOKEN = '***REMOVED***'

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from time import sleep

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello! Are you ready to work and make money ?")
    chat_id = message.chat.id
    import trader
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Every morning i will send a conclusion of analyze stocks. Just one word which can make you a rich guy.")

def decision(id, d1, hd, md, conclusion, sevenprice, sixprice, rep):
    bot.send_message(id, "Conclusion: "+conclusion)   

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)