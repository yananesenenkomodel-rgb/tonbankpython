import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("", "").strip()
PORT = int(os.getenv("PORT", "10000"))

if not BOT_TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🎮 Привет!\n\n"
        "Это система из двух мини-приложений:\n\n"
        "TONE COIN — игра, где ты добываешь TON, ломаешь блоки и качаешь кирку.\n\n"
        "TON BANK — банк, где у тебя баланс, карта и переводы.\n\n"
        "👇 Выбирай:"
    )

    kb = InlineKeyboardBuilder()
    kb.button(
        text="🎮 Открыть игру",
        web_app=WebAppInfo(url="https://ton-bank.onrender.com/game")
    )
    kb.button(
        text="🏦 Открыть банк",
        web_app=WebAppInfo(url="https://ton-bank.onrender.com")
    )
    kb.adjust(1)

    await message.answer(text, reply_markup=kb.as_markup())


async def healthcheck(_):
    return web.Response(text="ok")


async def start_http():
    app = web.Application()
    app.router.add_get("/", healthcheck)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()


async def main():
    await start_http()
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
