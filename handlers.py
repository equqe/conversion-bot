import re
import asyncio
import requests

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile

from pil import resize_512, resize_100, resize_custom, remove_bg
from db import create_profile, check_locale, edit_locale
from localisation import get_translation
from config import API_TOKEN
import keyboards

router = Router()

URI = f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id="
URI_path = f"https://api.telegram.org/file/bot{API_TOKEN}/"


class BotStatesGroup(StatesGroup):
    rembg_st = State()
    resize_st = State()
    resize_photo = State()
    resize_custom = State()

    rembg_photo = State()
    photo_512 = State()
    photo_100 = State()
    photo_custom = State()

    extension_st = State()
    jpg_st = State()
    png_st = State()
    lang_st = State()


async def process(photo_file_id):
    """getting image URI path"""
    response = requests.get(URI + photo_file_id)
    photos_filepath = response.json()["result"]["file_path"]
    image = requests.get(URI_path + photos_filepath)
    return image


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await create_profile(user_id=message.from_user.id,
                         language_code=message.from_user.language_code)
    await check_locale(user_id=message.from_user.id)
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    await message.answer_sticker(sticker="CAACAgIAAxkBAAEBi1VlMpCbLe6zb2zWFsU0yxQnH-rpWQACdDwAAmFemEkVkujTvaF0HjAE")
    await message.answer(_("hi!\n"
                           "this is a bot that can help you with editing "
                           "a picture to telegram sticker"
                           " format OR editing by picking a custom resolution.\n"
                           "you can create your pack with official bot @Stickers."))
    await message.answer(_("<b>sticker format requirements from @Stickers:</b>\n"
                           "\n"
                           "<i>The image file should be in PNG or WEBP format, with "
                           "a transparent background(optionally) and must fit into a 512x512 square "
                           "(each side must be greater than or equal to 512px).</i>\n"
                           "\n"
                           "you can take a look at command list, get a project github link "
                           "and view some additional info about project with /help command."),
                         parse_mode="HTML")


@router.message(Command("help"))
async def help_handler(message: Message):
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    await message.answer_sticker(sticker="CAACAgIAAxkBAAELBBZlhdWKHKBACubKkd13SUnIZ9p6KAACTkMAAmSQMEgHSEkRieKKmjME")
    await message.answer(_("<b>INFO</b>\n"
                           "\n"
                           "<b>available commands</b>\n"
                           "/help — to get info about bot(commands, q&a, author)\n"
                           "/resize — to resize an image. the command has few options: "
                           "512*512(sticker), 100*100(sticker pack cover) and custom(max 5000*5000).\n"
                           "/rembg — to remove image background\n"
                           "/lang — to change a locale(ru/eng)\n"
                           "\n"
                           "<b>sticker format requirements from @Stickers</b>\n"
                           "The image file should be in PNG or WEBP format with "
                           "a transparent background(optionally) and must fit into a 512x512 square "
                           "(one of the sides must be 512px and the other 512px or less).\n"
                           "\n"
                           "<b>about code</b>\n"
                           "you can take a look at bot's code on github: "
                           "https://github.com/equqe/conversion-bot\n"
                           "\n"
                           "<b>about project & author</b>\n"
                           "this is a open-source project.\n"
                           "\n"
                           "if you have any ideas, you can message me on tg(@html_F5F5F5)\n"
                           "OR do a commit on github to make code work and look better if you want.\n"
                           "\n"
                           "if bot works INCORRECTLY, feel free to message me too."),
                         parse_mode="HTML")


@router.message(Command("rembg"))
async def rembg_handler(message: Message, state: FSMContext):
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    await message.answer(_("send the photo to remove its background!"))
    await state.set_state(BotStatesGroup.rembg_photo)


@router.message(F.photo, BotStatesGroup.rembg_photo)
async def rembg_photo_process(message: Message):
    photo_file_id = message.photo[-1].file_id

    image = await process(photo_file_id)

    image_name = await remove_bg(image)
    photo = FSInputFile(f"photo/{image_name}.png")
    await message.answer_document(document=photo)


@router.message(Command("resize"))
async def resize_handler(message: Message, state: FSMContext):
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    await message.answer(_("select one resolution below:"),
                         reply_markup=keyboards.keyboard_size)
    await state.set_state(BotStatesGroup.resize_st)


@router.callback_query(BotStatesGroup.resize_st)
async def resize_callback(callback: CallbackQuery, state: FSMContext):
    task = asyncio.create_task(get_translation(user_id=callback.from_user.id))
    _ = await task

    if callback.data == "size_512":
        await callback.message.answer(_("okay! you chose 512*512.\n"
                                        "now send me a picture"))
        await state.set_state(BotStatesGroup.photo_512)

    elif callback.data == "size_100":
        await callback.message.answer(_("okay! you chose 100*100.\n"
                                        "now send me a picture\n"
                                        "\n"
                                        "<i>remark: results might look kinda cursed, so i recommend to "
                                        "crop an image to square-like form, because 100*100 is a square.\n"
                                        "otherwise your image will be shrank</i>"),
                                      parse_mode="HTML")
        await state.set_state(BotStatesGroup.photo_100)

    elif callback.data == "custom_size":
        await callback.message.answer(_("okay! you chose custom size.\n"
                                        "now send me size in pixels. "
                                        "you send it in 'width height' format(e.g. 1920 1080. "
                                        "limits: MIN 1 1. MAX 5000 5000)"))
        await state.set_state(BotStatesGroup.resize_custom)


@router.message(F.photo, BotStatesGroup.photo_512)
async def resizing_512(message: Message):
    photo_file_id = message.photo[-1].file_id

    image = await process(photo_file_id)

    image_name = await resize_512(image)
    photo = FSInputFile(f"photo/{image_name}.png")
    await message.answer_document(document=photo)


@router.message(F.photo, BotStatesGroup.photo_100)
async def resizing_100(message: Message):
    photo_file_id = message.photo[-1].file_id

    image = await process(photo_file_id)

    image_name = await resize_100(image)
    photo = FSInputFile(f"photo/{image_name}.png")
    await message.answer_document(document=photo)


@router.message(F.text, BotStatesGroup.resize_custom)
async def custom_size(message: Message, state: FSMContext):
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    size = message.text
    pattern = r"\d+"
    matches = list(map(int, re.findall(pattern, size)))
    if len(matches) != 2:
        await message.answer(_("you did something wrong.."))
    elif matches[1] > 5000 or matches[0] > 5000 or matches[1] < 1 or matches[0] < 1:
        await message.answer(_("out of range!"))
    else:
        await message.answer(_("the custom size is ") + str(matches) + "\n" + _("send the photo you want to resize"))
        await state.set_state(BotStatesGroup.photo_custom)
        await state.update_data(pic_size_data=message.text)


@router.message(F.photo, BotStatesGroup.photo_custom)
async def custom_process(message: Message, state: FSMContext):
    await state.update_data(photo_file_id=message.photo[-1].file_id)

    data = await state.get_data()

    size = data["pic_size_data"].split(" ")
    photo_id = data["photo_file_id"]

    x_axis = int(size[0])
    y_axis = int(size[1])

    image = await process(photo_id)

    image_name = await resize_custom(image, x_axis, y_axis)
    photo = FSInputFile(f"photo/{image_name}.png")
    await message.answer_document(document=photo)


@router.message(Command("lang"))
async def lang_handler(message: Message, state: FSMContext):
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    await message.answer(_("select the language:"),
                         reply_markup=keyboards.keyboard_lang)
    await state.set_state(BotStatesGroup.lang_st)


@router.callback_query(BotStatesGroup.lang_st)
async def lang_callback(callback: CallbackQuery):
    task = asyncio.create_task(get_translation(user_id=callback.from_user.id))
    _ = await task

    if callback.data == "ru":
        await edit_locale(user_id=callback.from_user.id, language_code=callback.data)
        await callback.message.answer("отлично! вы сменили язык на русский.")
    elif callback.data == "en":
        await edit_locale(user_id=callback.from_user.id, language_code=callback.data)
        await callback.message.answer("okay! you set your language to english.")


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    task = asyncio.create_task(get_translation(user_id=message.from_user.id))
    _ = await task

    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer(_("command canceled.\n"
                               "you can use /help to take a look at command list"))
    else:
        await message.answer(_("no commands to cancel!"))
