
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ===== НАСТРОЙКИ - ЗАМЕНИТЕ НА СВОИ ДАННЫЕ =====
BOT_TOKEN = "8625836687:AAG2Z5D8Xurt6uWbGZul795hy887htUu2Wg"  # Сюда вставьте токен

# ID администраторов (оба получат сообщения)
ADMIN_USER_ID_1 = 5832334851  # ID первого админа
ADMIN_USER_ID_2 = 8026545733  # ID второго админа

# Список админов
ADMINS = [ADMIN_USER_ID_1, ADMIN_USER_ID_2]
# =============================================

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает сообщение ВСЕМ админам (с реальными фото/видео) и отвечает пользователю"""
    user = update.effective_user
    if not user:
        return
    
    # Формируем информацию об отправителе
    user_info = f"👤 {user.full_name}\n🆔 {user.id}"
    if user.username:
        user_info += f"\n📛 @{user.username}"
    
    # Отправляем ВСЕМ админам
    for admin_id in ADMINS:
        try:
            # ТЕКСТОВОЕ СООБЩЕНИЕ
            if update.message.text:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"{user_info}\n\n📝 {update.message.text}"
                )
            
            # ФОТО
            elif update.message.photo:
                photo = update.message.photo[-1]  # Берём фото в лучшем качестве
                caption = f"{user_info}\n\n📸 Фото"
                if update.message.caption:
                    caption += f"\n\n📝 Подпись: {update.message.caption}"
                await context.bot.send_photo(
                    chat_id=admin_id,
                    photo=photo.file_id,
                    caption=caption
                )
            
            # ВИДЕО
            elif update.message.video:
                caption = f"{user_info}\n\n🎬 Видео"
                if update.message.caption:
                    caption += f"\n\n📝 Подпись: {update.message.caption}"
                await context.bot.send_video(
                    chat_id=admin_id,
                    video=update.message.video.file_id,
                    caption=caption
                )
            
            # ДОКУМЕНТЫ (PDF, ZIP, и т.д.)
            elif update.message.document:
                caption = f"{user_info}\n\n📄 Документ: {update.message.document.file_name}"
                if update.message.caption:
                    caption += f"\n\n📝 Подпись: {update.message.caption}"
                await context.bot.send_document(
                    chat_id=admin_id,
                    document=update.message.document.file_id,
                    caption=caption
                )
            
            # АУДИО
            elif update.message.audio:
                caption = f"{user_info}\n\n🎵 Аудио"
                if update.message.caption:
                    caption += f"\n\n📝 Подпись: {update.message.caption}"
                await context.bot.send_audio(
                    chat_id=admin_id,
                    audio=update.message.audio.file_id,
                    caption=caption
                )
            
            # ГОЛОСОВЫЕ
            elif update.message.voice:
                await context.bot.send_voice(
                    chat_id=admin_id,
                    voice=update.message.voice.file_id,
                    caption=f"{user_info}\n\n🎙 Голосовое сообщение"
                )
            
            # СТИКЕРЫ
            elif update.message.sticker:
                await context.bot.send_sticker(
                    chat_id=admin_id,
                    sticker=update.message.sticker.file_id
                )
                # Дополнительно отправляем информацию о стикере текстом
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"{user_info}\n\n🖼 Стикер: {update.message.sticker.emoji if update.message.sticker.emoji else 'без эмодзи'}"
                )
            
            # ЛОКАЦИЯ
            elif update.message.location:
                await context.bot.send_location(
                    chat_id=admin_id,
                    latitude=update.message.location.latitude,
                    longitude=update.message.location.longitude
                )
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"{user_info}\n\n📍 Отправил локацию"
                )
            
            # КОНТАКТ
            elif update.message.contact:
                contact = update.message.contact
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"{user_info}\n\n📇 Контакт\n👤 {contact.first_name} {contact.last_name or ''}\n📞 {contact.phone_number}"
                )
            
            # ВСЁ ОСТАЛЬНОЕ
            else:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"{user_info}\n\n❓ Неизвестный тип сообщения"
                )
                
        except Exception as e:
            logging.error(f"Не удалось отправить админу {admin_id}: {e}")
    
    # Ответ пользователю
    await update.message.reply_text("Сообщение получено ✅")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - отправляет приветствие ТОЛЬКО пользователю"""
    await update.message.reply_text("Напишите ваше сообщение")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики
    app.add_handler(MessageHandler(filters.COMMAND, start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_admin))
    
    print("✅ Бот запущен!")
    print(f"👥 Администраторов: {len(ADMINS)}")
    print("📸 Админы получают реальные фото/видео/документы")
    app.run_polling()

if __name__ == "__main__":
    main()
