import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8244607659:AAHs_RU3fjnCINY3nh-OjVevq1Tc_vrJDAI"
CHANNEL_ID = -1003174286262 

# Bot va Dispatcher yaratish
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

students_db = {
    "12345": {
        "parol": "qwerty",
        "ism": "Abdulloh",
        "familiya": "Karimov",
        "guruh": "Python-1",
        "coin": 150
    },
    "67890": {
        "parol": "pass123",
        "ism": "Malika",
        "familiya": "Toshmatova",
        "guruh": "Frontend-2",
        "coin": 280
    },
    "11111": {
        "parol": "test",
        "ism": "Jasur",
        "familiya": "Aliyev",
        "guruh": "SMM-1",
        "coin": 95
    }
}

class LoginState(StatesGroup):
    waiting_for_id = State()
    waiting_for_password = State()

class ReviewState(StatesGroup):
    waiting_for_review = State()

user_sessions = {}

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧑‍🎓 Profil"), KeyboardButton(text="🪙 Mening coinlarim")],
            [KeyboardButton(text="💥 Space Shop"), KeyboardButton(text="🏫 Maktab haqida")],
            [KeyboardButton(text="✍️ Izoh qoldirish")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_sessions.pop(message.from_user.id, None)
    
    await message.answer(
        "🎓 <b>Mars IT School botiga xush kelibsiz!</b>\n\n"
        "Iltimos, ID raqamingizni kiriting:",
        parse_mode="HTML"
    )
    
    await message.answer(str(students_db))
    
    await state.set_state(LoginState.waiting_for_id)

@dp.message(LoginState.waiting_for_id)
async def process_id(message: types.Message, state: FSMContext):
    student_id = message.text.strip()
    
    if student_id in students_db:
        await state.update_data(student_id=student_id)
        await message.answer("🔑 Parolni kiriting:")
        await state.set_state(LoginState.waiting_for_password)
    else:
        await message.answer(
            "❌ <b>Bunday o'quvchi topilmadi!</b>\n\n"
            "Iltimos, ID raqamingizni qayta tekshiring va qaytadan kiriting:",
            parse_mode="HTML"
        )

# Parol kiritish
@dp.message(LoginState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    student_id = data.get("student_id")
    parol = message.text.strip()
    
    student = students_db[student_id]
    
    if student["parol"] == parol:
        user_sessions[message.from_user.id] = student_id
        
        await message.answer(
            f"✅ <b>Xush kelibsiz, {student['ism']} {student['familiya']}!</b>\n\n"
            f"👥 Guruh: {student['guruh']}\n"
            f"🪙 Coinlar: {student['coin']}",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )
        await state.clear()
    else:
        await message.answer(
            "❌ <b>Parol noto'g'ri!</b>\n\n"
            "Iltimos, parolni qaytadan kiriting:",
            parse_mode="HTML"
        )

# Profil ko'rish
@dp.message(F.text == "🧑‍🎓 Profil")
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
        return
    
    student_id = user_sessions[user_id]
    student = students_db[student_id]
    
    await message.answer(
        f"👤 <b>Shaxsiy ma'lumotlar</b>\n\n"
        f"🆔 ID: {student_id}\n"
        f"👨‍💼 Ism: {student['ism']}\n"
        f"👨‍💼 Familiya: {student['familiya']}\n"
        f"👥 Guruh: {student['guruh']}\n"
        f"🪙 Coinlar: {student['coin']}",
        parse_mode="HTML"
    )

# Coinlar ko'rish
@dp.message(F.text == "🪙 Mening coinlarim")
async def show_coins(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
        return
    
    student_id = user_sessions[user_id]
    student = students_db[student_id]
    
    await message.answer(
        f"🪙 <b>Sizning coinlaringiz</b>\n\n"
        f"Jami: <b>{student['coin']}</b> coin\n\n"
        f"💡 Coinlarni darsga qatnashish, topshiriqlar va aktivlik uchun olasiz!",
        parse_mode="HTML"
    )

# Space Shop
@dp.message(F.text == "💥 Space Shop")
async def space_shop(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
        return
    
    await message.answer(
        "🛍 <b>Space Shop - Mars IT School do'koni</b>\n\n"
        "Coinlaringizni Mars IT mahsulotlariga almashtiring!\n"
        "Futbolkalar, stikerlar, sumkalar va boshqa ajoyib narsalar!\n\n"
        "🔗 https://space.marsit.uz/shop-page",
        parse_mode="HTML"
    )

# Maktab haqida
@dp.message(F.text == "🏫 Maktab haqida")
async def about_school(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
        return
    
    await message.answer_photo(
        photo="https://mars.uz/storage/photos/shares/ogp.jpg",
        caption=(
            "🚀 <b>Mars IT School haqida</b>\n\n"
            "Mars IT School - O'zbekistondagi yetakchi IT ta'lim markazi!\n\n"
            "📚 <b>Yo'nalishlarimiz:</b>\n"
            "• Frontend Development\n"
            "• Backend Development (Python, Node.js)\n"
            "• Mobile Development (Flutter, React Native)\n"
            "• UX/UI Design\n"
            "• Digital Marketing & SMM\n"
            "• Grafik Dizayn\n\n"
            "👨‍🏫 Tajribali mentorlar\n"
            "💼 Amaliy loyihalar\n"
            "🎓 Sertifikatlar\n"
            "🤝 Ish bilan ta'minlash\n\n"
            "📍 Manzil: Toshkent, Chilonzor tumani\n"
            "📞 Telefon: +998 (90) 123-45-67\n"
            "🌐 Web: https://mars.uz"
        ),
        parse_mode="HTML"
    )

# Izoh qoldirish
@dp.message(F.text == "✍️ Izoh qoldirish")
async def leave_review(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
        return
    
    await message.answer(
        "✍️ <b>Izoh qoldirish</b>\n\n"
        "Mars IT School haqida fikr-mulohazalaringizni yozing!\n"
        "Sizning fikringiz biz uchun juda muhim 💙",
        parse_mode="HTML"
    )
    await state.set_state(ReviewState.waiting_for_review)

# Izohni qabul qilish va kanalga yuborish
@dp.message(ReviewState.waiting_for_review)
async def process_review(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
        await state.clear()
        return
    
    student_id = user_sessions[user_id]
    student = students_db[student_id]
    review_text = message.text
    
    # Telegram username olish
    username = message.from_user.username
    username_text = f"@{username}" if username else "Username yo'q"
    
    # Kanalga izohni yuborish
    try:
        channel_message = (
            "📝 <b>Yangi izoh!</b>\n\n"
            f"👤 <b>O'quvchi:</b> {student['ism']} {student['familiya']}\n"
            f"🆔 <b>ID:</b> {student_id}\n"
            f"👥 <b>Guruh:</b> {student['guruh']}\n"
            f"📱 <b>Telegram:</b> {username_text}\n"
            f"🆔 <b>User ID:</b> {user_id}\n\n"
            f"💬 <b>Izoh:</b>\n{review_text}"
        )
        
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=channel_message,
            parse_mode="HTML"
        )
        
        await message.answer(
            f"✅ <b>Rahmat, {student['ism']}!</b>\n\n"
            "Sizning izohingiz muvaffaqiyatli qabul qilindi! 💙\n"
            "Bizni rivojlantirishga yordam berganingiz uchun tashakkur!",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )
        logging.info(f"Izoh kanalga yuborildi: {student_id}")
    except Exception as e:
        logging.error(f"Kanalga izoh yuborishda xato: {e}")
        await message.answer(
            "❌ Izohni yuborishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.",
            reply_markup=get_main_keyboard()
        )
    
    await state.clear()

# Noto'g'ri xabarlar uchun
@dp.message()
async def unknown_message(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("❌ Avval /start buyrug'ini bosing!")
    else:
        await message.answer(
            "🤔 Noto'g'ri buyruq. Iltimos, quyidagi tugmalardan foydalaning:",
            reply_markup=get_main_keyboard()
        )

# Botni ishga tushirish
async def main():
    print("🚀 Bot ishga tushdi!")
    print(f"📊 Bazada {len(students_db)} ta o'quvchi mavjud")
    print(f"📢 Kanal ID: {CHANNEL_ID}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())