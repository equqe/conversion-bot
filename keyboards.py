from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

size_buttons = [
    [
        InlineKeyboardButton(text="512*512",
                             callback_data="size_512"),
        InlineKeyboardButton(text="100*100",
                             callback_data="size_100")
    ],

    [
        InlineKeyboardButton(text="custom size",
                             callback_data="custom_size")
    ]
]
keyboard_size = InlineKeyboardMarkup(inline_keyboard=size_buttons)

lang_buttons = [
    [
        InlineKeyboardButton(text="ru",
                             callback_data="ru"),
        InlineKeyboardButton(text="en",
                             callback_data="en")
    ]
]
keyboard_lang = InlineKeyboardMarkup(inline_keyboard=lang_buttons)
