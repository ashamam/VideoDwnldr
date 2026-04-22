import asyncio
import logging
import sys
import yt_dlp
from os import getenv
from aiogram.utils.keyboard import InlineKeyboardBuilder
from linkCheck import is_valid_link
import glob
from dotenv import load_dotenv

from os import path, remove
from aiogram.types import FSInputFile, URLInputFile
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

# Bot token can be obtained via https://t.me/BotFather

load_dotenv()
TOKEN = getenv("TOKEN")

# All handlers should be attached to the Router (or Dispatcher)


dp = Dispatcher()


class Quality(StatesGroup):
    quality = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(
        f"Привет, {message.from_user.full_name}!🎉\n\nОтправь сслыку на видео которое нужно скачать"
    )


@dp.message()
async def echo_handler(message: Message, state: FSMContext) -> None:

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    builder = InlineKeyboardBuilder()

    if is_valid_link(message.text):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = 0

            coro = asyncio.to_thread(ydl.extract_info, message.text, download=False)
            task = asyncio.create_task(coro)

            info = await task

            res = []
            allowed_res = [144, 360, 720, 1080, 1440, 2160]

            # Access common metadata fields
            formats = info.get("formats")
            for f in formats:
                if f.get("height") is not None:
                    res.append(f.get("height"))
                    common_res = list(set(res) & set(allowed_res))
            common_res.sort()

            for index in range(0, len(common_res)):
                builder.button(
                    text=f"🎬 {common_res[index]}",
                    callback_data=f"btn_{common_res[index]}",
                )

            builder.button(
                text=f"🔊 Аudio",
                callback_data=f"btn_audio",
            )

            builder.adjust(1, 1)

            await message.answer(
                "Выберите качество видео", reply_markup=builder.as_markup()
            )

        await state.update_data(
            link=message.text,
            title=info.get("title"),
            artist=info.get("artist"),
            thumbnail=info.get("thumbnail"),
        )

        await state.set_state(Quality.quality)

    else:
        await message.answer(
            """Кажется, я не обнаружил ссылки😥\n\nПопробуйте еще раз"""
        )


@dp.callback_query(Quality.quality)
async def videoSend(call: CallbackQuery, state: FSMContext) -> None:

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()

    try:
        mess = await call.message.answer("Идет скачивание, подождите...")

        data = await state.get_data()

        if call.data == "btn_audio":
            ydl_opts = {
                "format": "m4a/bestaudio/best",
                "outtmpl": f"./files/{call.message.message_id}",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "m4a",
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as videoDwnld:

                coro = asyncio.to_thread(videoDwnld.download, data["link"])
                task = asyncio.create_task(coro)

                await task

                file = glob.glob(f"./files/{call.message.message_id}.*")[0]

                if path.isfile(file):
                    await mess.delete()
                    await call.message.answer_audio(
                        FSInputFile(file),
                        title=data["title"],
                        performer=data["artist"],
                        thumbnail=URLInputFile(data["thumbnail"]),
                    )
                    remove(file)

        else:
            ydl_opts = {
                "format": f"bestvideo[height={call.data}]+bestaudio/best",
                "outtmpl": f"./files/{call.message.message_id}.mp4",
                "age_limit": 45,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as videoDwnld:

                coro = asyncio.to_thread(videoDwnld.download, data["link"])
                task = asyncio.create_task(coro)

                await task

                file = glob.glob(f"./files/{call.message.message_id}.*")[0]

                if path.isfile(file):
                    await mess.delete()
                    await call.message.answer_video(
                        FSInputFile(file),
                        title=data["title"],
                        thumbnail=URLInputFile(data["thumbnail"]),
                    )
                    remove(file)

    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await call.message.answer("Произошла ошибка отправки видео!")

    await state.clear()


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
