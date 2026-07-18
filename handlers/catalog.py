import os
import threading

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command

from config import CATEGORIES, PRODUCTS, KEYS_POOL
from database import save_purchase, get_user_purchases

router = Router()

# Для быстрого поиска категории по id товара
_product_to_cat = {}
for ck, prods in PRODUCTS.items():
    for p in prods:
        _product_to_cat[p["id"]] = ck

_keys_lock = threading.Lock()


def main_keyboard():
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛍 Каталог")]],
        resize_keyboard=True,
    )


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🛒 Добро пожаловать в магазин цифровых товаров!\n\n"
        "Нажмите «Каталог», чтобы посмотреть товары.",
        reply_markup=main_keyboard(),
    )


@router.message(Command("my_purchases"))
async def cmd_my_purchases(message: Message):
    purchases = get_user_purchases(message.from_user.id)
    if not purchases:
        await message.answer("У вас пока нет покупок.")
        return
    lines = ["<b>📦 Ваши покупки:</b>\n"]
    for p in purchases:
        lines.append(f"• {p['product_name']} — {p['price']} руб. ({p['purchased_at']})")
    await message.answer("\n".join(lines))


@router.message(F.text == "🛍 Каталог")
async def catalog(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"cat_{key}")]
            for name, key in CATEGORIES.items()
        ]
    )
    await message.answer("Выберите категорию:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("cat_"))
async def show_products(callback: CallbackQuery):
    cat_key = callback.data.replace("cat_", "")
    products = PRODUCTS.get(cat_key, [])
    if not products:
        await callback.answer("В этой категории пока нет товаров.")
        return
    buttons = [
        [InlineKeyboardButton(
            text=f"{p['name']} — {p['price']} руб.",
            callback_data=f"prod_{p['id']}",
        )]
        for p in products
    ]
    buttons.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back_catalog")])
    await callback.message.edit_text(
        f"📂 {dict((v, k) for k, v in CATEGORIES.items()).get(cat_key, cat_key)}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("prod_"))
async def show_product_card(callback: CallbackQuery):
    product_id = int(callback.data.replace("prod_", ""))
    cat_key = _product_to_cat.get(product_id)
    if cat_key is None:
        await callback.answer("Товар не найден.")
        return
    for p in PRODUCTS[cat_key]:
        if p["id"] == product_id:
            text = (
                f"<b>{p['name']}</b>\n\n"
                f"{p['description']}\n\n"
                f"💰 Цена: {p['price']} руб."
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💳 Купить", callback_data=f"buy_{p['id']}")],
                    [InlineKeyboardButton(text="⬅ Назад", callback_data=f"cat_{cat_key}")],
                ]
            )
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
            await callback.answer()
            return
    await callback.answer("Товар не найден.")


@router.callback_query(F.data == "back_catalog")
async def back_to_catalog(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"cat_{key}")]
            for name, key in CATEGORIES.items()
        ]
    )
    await callback.message.edit_text("Выберите категорию:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery):
    product_id = int(callback.data.replace("buy_", ""))
    cat_key = _product_to_cat.get(product_id)
    if cat_key is None:
        await callback.answer("Товар не найден.")
        return
    product = None
    for p in PRODUCTS[cat_key]:
        if p["id"] == product_id:
            product = p
            break
    if not product:
        await callback.answer("Товар не найден.")
        return

    with _keys_lock:
        keys = KEYS_POOL.get(product_id, [])
        if not keys and cat_key != "guides":
            await callback.answer("К сожалению, товар закончился.", show_alert=True)
            return

        content = None
        if cat_key == "guides":
            file_path = os.path.join("media", f"guide_{product_id}.pdf")
            if not os.path.exists(file_path):
                await callback.answer("Файл временно недоступен.", show_alert=True)
                return
            content = file_path
        else:
            content = keys.pop(0)
            KEYS_POOL[product_id] = keys

    save_purchase(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        product_id=product_id,
        product_name=product["name"],
        price=product["price"],
        content=content,
    )

    await callback.answer("✅ Оплата прошла успешно!", show_alert=True)

    if cat_key == "guides":
        await callback.message.answer_document(
            FSInputFile(content),
            caption=f"📘 Ваш гайд: {product['name']}\nСпасибо за покупку!",
        )
    else:
        await callback.message.answer(
            f"✅ <b>{product['name']}</b>\n\n"
            f"Ваш ключ:\n<code>{content}</code>\n\n"
            f"Сохраните его в надёжном месте.",
            parse_mode="HTML",
        )

    await callback.message.answer("Можете продолжить покупки:", reply_markup=main_keyboard())
