TOKEN = 'bot_token'

import aioschedule as schedule
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import time
import datetime
from datetime import date
from datetime import timedelta
from time import sleep
import sqlite3

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello! Are you ready to work and make money ?")
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Every morning i will send a conclusion of analyze stocks. Just one word which can make you a rich guy.")

async def conclusion():
	today = date.today()
	d1 = today.strftime("%d/%m/%Y")
	conn = sqlite3.connect("trades.db")
	db = conn.cursor() 
	query = "SELECT global_conclusion FROM trades WHERE dateoftrade = ?"
	db.execute(query, [(d1)])
	conclusion = db.fetchone()
	await bot.send_message(***REMOVED***, conclusion)

async def scheduler():
    schedule.every().minutes.do(conclusion)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(x):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)