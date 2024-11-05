from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def pagination_btn(product_index):
    design = [
        [
            InlineKeyboardButton(text='prev', callback_data=f'prev_{product_index - 1}'),
            InlineKeyboardButton(text=str(product_index + 1), callback_data=f'session_{product_index}'),
            InlineKeyboardButton(text="next", callback_data=f'next_{product_index + 1}'),
        ],
        [
            InlineKeyboardButton(text='🛒', callback_data=f'session_{product_index}'),
        ]

    ]
    if product_index == 0:
        del design[0][0]  # Agar birinchi mahsulot bo'lsa, "prev" tugmasini olib tashlaymiz
    return InlineKeyboardMarkup(inline_keyboard=design)


async def buy_now_button():
    design1 = [
        InlineKeyboardButton(text='Buy now!', callback_data="buy_now"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[design1])


async def shoes_button():
    design2 = [
        InlineKeyboardButton(text='1. shoe', callback_data="shoe_1"),
        InlineKeyboardButton(text='2. shoe', callback_data="shoe_2"),
        InlineKeyboardButton(text='3. shoe', callback_data="shoe_3"),
        InlineKeyboardButton(text='4. shoe', callback_data="shoe_4"),
        InlineKeyboardButton(text='5. shoe', callback_data="shoe_5"),
        InlineKeyboardButton(text='6. shoe', callback_data="shoe_6"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[design2])
