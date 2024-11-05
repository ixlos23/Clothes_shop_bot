import json

from aiogram import Router, F
from aiogram import types
from aiogram.fsm import state

from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, LabeledPrice
from aiogram.types import InputMediaPhoto
from aiogram.types import Message, CallbackQuery

from bot import states
from utils.conf import Config as conf
from bot.buttons.inline import pagination_btn, buy_now_button, shoes_button
from utils import conf
from utils.conf import Config

product_router = Router()


@product_router.message(F.text == "👕 List of clothes")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    with open('products.json', 'r') as f:
        products: list[dict] = json.load(f)
    await state.update_data({'products': products})
    first_product = products[0]
    product_index = 0
    caption = f"Title: {first_product.get('title')}\nPrice: {first_product.get('price')}"
    await message.answer_photo(
        photo=first_product.get('images')[0],
        caption=caption,
        reply_markup=await pagination_btn(product_index)
    )


@product_router.callback_query(F.data.startswith('next_'))
async def next_product(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    products = data['products']
    product_index = data.get('product_index', 0) + 1

    if product_index < len(products):
        product = products[product_index]
        caption = f"Title: {product.get('title')}\nPrice: {product.get('price')}"
        await callback_query.message.edit_media(
            InputMediaPhoto(media=product.get('images')[0], caption=caption),
            reply_markup=await pagination_btn(product_index)
        )
        await state.update_data({'product_index': product_index})
    await callback_query.answer()


@product_router.callback_query(F.data.startswith('prev_'))
async def prev_product(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    products = data['products']
    product_index = data.get('product_index', 0) - 1

    if product_index >= 0:
        product = products[product_index]
        caption = f"Title: {product.get('title')}\nPrice: {product.get('price')}"
        await callback_query.message.edit_media(
            InputMediaPhoto(media=product.get('images')[0], caption=caption),
            reply_markup=await pagination_btn(product_index)
        )
        await state.update_data({'product_index': product_index})
    await callback_query.answer()


@product_router.callback_query(F.data.startswith('session_'))
async def add_to_cart(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    products = data['products']
    product_index = int(callback_query.data.split('_')[1])
    product = products[product_index]
    cart = data.get('cart', [])
    cart.append(product)
    await state.update_data({'cart': cart})

    await callback_query.answer("Mahsulot savatga qo'shildi!")


@product_router.message(F.text == "🛒 View Cart")
async def view_cart(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    cart = data.get('cart', [])

    if cart:
        cart_items = "\n\n".join(
            [f"Title: {item.get('title')}\nPrice: {item.get('price')}" for item in cart]
        )
        await message.answer(f"Savatdagi mahsulotlar:\n\n{cart_items}", reply_markup=await buy_now_button())
    else:
        await message.answer("Savatda mahsulot yo'q.")


#
# shoes_data = {
#     "1_shoe": {"title": "Nike Air Max", "price": "$120",
#                "image_url": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes1.jpeg"},
#     "2_shoe": {"title": "Adidas UltraBoost", "price": "$150",
#                "image_url": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes2.jpeg"},
#     "3_shoe": {"title": "Puma RS-X", "price": "$110",
#                "image_url": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes3.jpeg"},
#     "4_shoe": {"title": "Reebok Classic", "price": "$90",
#                "image_url": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes4.jpeg"},
#     "5_shoe": {"title": "New Balance 990", "price": "$130",
#                "image_url": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes5.jpeg"},
#     "6_shoe": {"title": "Converse Chuck Taylor", "price": "$70",
#                "image_url": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes6.jpeg"},
# }

@product_router.message(F.text == '👟 shoes')
async def shoes_handler(message: Message, state: FSMContext):
    await message.answer("Quyidagi poyafzallardan birini tanlang:", reply_markup=await shoes_button())


@product_router.callback_query(F.callback_data.startswith("shoe_"))
async def shoe_detail_callback(query: types.CallbackQuery):
    shoe_number = query.data.split("_")[1]

    shoe_data = {
        "1": {"title": "Birinci poyabzal", "price": "100$",
              "photo": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes1.jpeg"},
        "2": {"title": "Ikkinchi poyabzal", "price": "120$",
              "photo": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes2.jpeg"},
        "3": {"title": "Uchinchi poyabzal", "price": "90$",
              "photo": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes3.jpeg"},
        "4": {"title": "To'rtinchi poyabzal", "price": "110$",
              "photo": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes4.jpeg"},
        "5": {"title": "Beshinchi poyabzal", "price": "105$",
              "photo": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes5.jpeg"},
        "6": {"title": "Oltinchi poyabzal", "price": "95$",
              "photo": "/home/ixlos/PycharmProjects/Clothes_shop_botTG/picture_collector/shoes6.jpeg"},
    }

    shoe_info = shoe_data.get(shoe_number, {"title": "Noma'lum", "price": "Noma'lum"})
    response_text = f"{shoe_info['title']}\nNarxi: {shoe_info['price']}"

    # Tanlangan poyabzal haqida rasm va ma'lumot jo'natish
    photo_path = shoe_info['photo']
    if photo_path:
        try:
            photo_file = InputFile(photo_path)
            await query.message.answer_photo(photo=photo_file, caption=response_text)
        except FileNotFoundError:
            await query.message.answer("Kechirasiz, rasmni yuklab bo‘lmadi.")
    else:
        await query.message.answer(response_text)
    await query.answer()
    await query.answer()



# Router yaratish


@product_router.callback_query(F.data.startswith("buy_"))
async def shoe_detail_callback(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()  # Bu yerda state ma'lumotlari olinadi
    cart = data.get('cart', [])
    card_count = len(cart)

    prices = [
        LabeledPrice(label='Essence Mascara Lash Princess', amount=9_900 * 1 * 100),
    ]

    await query.message.answer_invoice(
        title='Product',
        description=f"Jami {card_count} mahsulot buyurtma qilindi",
        payload='1',
        provider_token=conf.Bot.PAYMENT_CLICK_TOKEN,
        currency="UZS",
        prices=prices
    )


"""
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ixlos23/Clothes_shop_bot.git
git push -u origin main
"""