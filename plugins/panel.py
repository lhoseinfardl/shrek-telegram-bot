import os
import json
from pyrogram import Client, filters
from pyrogram.types import *
import random


DATABASE_FILE = "databaseDEV.json"


def load_db():
    if not os.path.exists(DATABASE_FILE):
        return {"admins": [], "users": [], "settings": {"broadcast_enabled": True}}

    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_admin(func):
    async def wrapper(client: Client, message: Message):
        db = load_db()
        user_id = message.from_user.id

        if user_id in db["admins"]:
            await func(client, message)
        else:
            await message.reply("❌ دسترسی غیرمجاز!")

    return wrapper



async def send_random_image(message):
    quotes = [
        "https://img.netzwelt.de/dw1200_dh675_sw1920_sh1080_sx0_sy0_sr16x9_nu0/picture/original/2020/04/shrek-tollkuehne-held-273660.jpeg",
        "https://wallpapers.com/images/high/funny-shrek-meme-png-74-x5j7tc4pq56gavug.png",
        "https://wallpapers.com/images/high/meme-faces-funny-pictures-wxyog2adisn7rddu.webp",
        "https://wallpapersok.com/images/high/shrek-making-a-funny-face-1lawv7i17eeg10xw.webp",
        "https://wallpapersok.com/images/high/funny-shrek-pout-in-sunglasses-3q0oc9esvyjow7uk.webp",
        "https://wallpapersok.com/images/high/shrek-ing-it-up-b9kaxd3yp96ezr0q-2.webp",
        "https://wallpapersok.com/images/high/funny-shrek-and-donkey-welcome-to-duloc-kcn8nv60431sny2u-2.webp",
        "https://wallpapersok.com/images/high/don-t-i-look-funny-in-this-hat-p3u4885t4gqf0s9m-2.webp",
    ]
    random_image = random.choice(quotes)

    await message.reply_photo(
        random_image,
        caption="💚 LOVE SHREK, LIVE SHREK 💚"
    )

@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    dbdev = load_db()
    user_id = message.from_user.id

    if user_id not in dbdev["users"]:
        dbdev["users"].append(user_id)
        save_db(dbdev)

    await send_random_image(message)

    await message.reply_text(
        """🔹 به ربات خوش آمدید! 🔹
این یک ربات مدیریتی ساده است. برای شروع از دکمه‌های زیر استفاده کنید یا دستورات را ارسال کنید.

🚀 مدیریت آسان، عملکرد سریع!""",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["سیب", "سیب"]
            ],
            resize_keyboard=True,
        )
    )


# دستور برای اضافه کردن ادمین جدید
@Client.on_message(filters.command("addadmin") & filters.private)
@is_admin
async def add_admin(client: Client, message: Message):
    try:
        target_id = int(message.text.split()[1])
        dbdev = load_db()

        if target_id not in dbdev["admins"]:
            dbdev["admins"].append(target_id)
            save_db(dbdev)
            await message.reply(f"✅ کاربر {target_id} به ادمین‌ها اضافه شد.")
        else:
            await message.reply("⚠️ کاربر از قبل ادمین است.")

    except (IndexError, ValueError):
        await message.reply("⚠️ فرمت دستور نادرست!\nمثال: `/addadmin 123456789`")


# دستور برای حذف ادمین
@Client.on_message(filters.command("removeadmin") & filters.private)
@is_admin
async def remove_admin(client: Client, message: Message):
    try:
        target_id = int(message.text.split()[1])
        dbdev = load_db()

        if target_id in dbdev["admins"]:
            dbdev["admins"].remove(target_id)
            save_db(dbdev)
            await message.reply(f"✅ کاربر {target_id} از ادمین‌ها حذف شد.")
        else:
            await message.reply("⚠️ کاربر ادمین نیست.")

    except (IndexError, ValueError):
        await message.reply("⚠️ فرمت دستور نادرست!\nمثال: `/removeadmin 123456789`")


# دستور برای نمایش ادمین‌ها
@Client.on_message(filters.command("admins") & filters.private)
@is_admin
async def list_admins(client: Client, message: Message):
    dbdev = load_db()
    admins = "\n".join([f"👤 {admin_id}" for admin_id in db["admins"]])
    await message.reply(f"**لیست ادمین‌ها:**\n{admins}")


# دستور برای نمایش آمار ربات
@Client.on_message(filters.command("stats") & filters.private)
@is_admin
async def bot_stats(client: Client, message: Message):
    dbdev = load_db()
    total_users = len(dbdev["users"])
    total_admins = len(dbdev["admins"])

    await message.reply(
        f"📊 **آمار ربات:**\n"
        f"👥 کاربران کل: {total_users}\n"
        f"👤 ادمین‌ها: {total_admins}"
    )


# دستور برای برودکست پیام
@Client.on_message(filters.command("sendall") & filters.private)
@is_admin
async def broadcast_message(client: Client, message: Message):
    dbdev = load_db()

    if not message.reply_to_message:
        await message.reply("⚠️ لطفا به یک پیام ریپلای کنید.")
        return

    success = 0
    failed = 0

    for user_id in dbdev["users"]:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
        except:
            failed += 1

    await message.reply(
        f"**sendall انجام شد!**\n"
        f"✅ موفق: {success}\n"
        f"❌ ناموفق: {failed}"
    )


# --- ذخیره کاربران جدید ---
if not os.path.exists(DATABASE_FILE):
    initial_data = {
        "admins": [7607409231],  # آیدی شما
        "users": [],
        "settings": {"broadcast_enabled": True}
    }
    save_db(initial_data)
