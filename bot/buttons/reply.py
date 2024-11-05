from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def main_button():
    design = [
        [
            KeyboardButton(text=_('👕 List of clothes')),
            KeyboardButton(text=_('👟 shoes'))
        ],
        [
            KeyboardButton(text=_('🥼 sweater & hoodie')),
            KeyboardButton(text=_('👖 trousers'))
        ],
        [
            KeyboardButton(text='🛒 View Cart', callback_data='view_cart'),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)