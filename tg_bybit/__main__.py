import sys
import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, Router
from aiogram.types import (
                    CallbackQuery,
                    InlineKeyboardMarkup,
                    InlineKeyboardButton,
                    Message
                )
from aiogram.types.input_file import InputFile, BufferedInputFile
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import ContentType
from aiogram import F
from dotenv import dotenv_values

from utils.visualization import generate_plot

from ta import add_all_ta_features
from ta.volatility import BollingerBands

import pandas as pd

config = dotenv_values('.env')

bot = Bot(token = config['TG_API_TOKEN'])

dp = Dispatcher()
router = Router()

pair = 'BTCUSDT'

async def get_bybit_data(pair, interval='1'):
    url = f"https://api-testnet.bybit.com/v5/market/kline?category=inverse&symbol={pair}&interval={interval}&limit=15"
    response = requests.get(url)
    data = response.json()
    return data

def calculate_statistics(data):
    closes = [float(candle[4]) for candle in data['result']['list']]
    opens = [float(candle[1]) for candle in data['result']['list']]
    highs = [float(candle[2]) for candle in data['result']['list']]
    lows = [float(candle[3]) for candle in data['result']['list']]
    volumes = [float(candle[5]) for candle in data['result']['list']]

    return {
        'open': opens[0],
        'high': max(highs),
        'low': min(lows),
        'close': closes[-1],
        'volume': sum(volumes)
    }

@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.reply('Use `stats` to get statistics on BTCUSDT pair in 15 minutes window')

@dp.message(Command('stats'))
async def send_stats(message: Message):
    data = await get_bybit_data(pair)

    stats = calculate_statistics(data)
    plot_buf = generate_plot(data, pair)

    response_message = (
        f"Statistics for the last 15 minutes for {pair}:\n"
        f"▫️ Open: {stats['open']}\n"
        f"🟢 High: {stats['high']}\n"
        f"🔴 Low: {stats['low']}\n"
        f"▪️ Close: {stats['close']}\n"
        f"📊 Volume: {stats['volume']}"
    )

    

    #photo = BufferedInputFile(plot_buf, filename='temp/plot.png')
    photo = FSInputFile("temp/plot.png")

    await message.reply(response_message, parse_mode=ParseMode.MARKDOWN)
    await bot.send_photo(message.chat.id, photo=photo)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())