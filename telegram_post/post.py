import os
import logging
import shutil
from config import API_ID, API_HASH, SESSION_PATH, CHANNEL_USERNAME, CHANNEL_ID, CHANNEL_TITLE, STATUS_PUBLISHED
from telethon import TelegramClient
from telethon.tl.types import InputMediaUploadedPhoto
from telegram_post.database import get_random_approved_photo, get_photo_path, update_photo_status

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_session_file():
    """
    Проверяет наличие локального файла сессии и при необходимости копирует его из SESSION_PATH
    
    Returns:
        str: Путь к файлу сессии для использования
    """
    local_session = 'tg-post.session'
    
    # Проверяем наличие локального файла сессии
    if os.path.exists(local_session):
        logger.info(f"Найден локальный файл сессии: {local_session}")
        return local_session
    
    # Если локального файла нет, проверяем SESSION_PATH
    if os.path.exists(SESSION_PATH):
        logger.info(f"Копируем файл сессии из {SESSION_PATH} в {local_session}")
        try:
            shutil.copy2(SESSION_PATH, local_session)
            logger.info("Файл сессии успешно скопирован")
            return local_session
        except Exception as e:
            logger.error(f"Ошибка при копировании файла сессии: {str(e)}")
            return SESSION_PATH
    
    logger.info(f"Файл сессии не найден, будет создан новый: {local_session}")
    return local_session

async def post_to_channel(text: str, media_path: str = None, parse_mode: str = 'html'):
    """
    Публикует пост в Telegram канал
    
    Args:
        text (str): Текст поста
        media_path (str, optional): Путь к медиафайлу (изображение, видео и т.д.)
        parse_mode (str, optional): Режим разбора текста ('html' или 'md')
    
    Returns:
        int: ID сообщения, если пост успешно опубликован, None в случае ошибки
    """
    try:
        logger.info(f"Используемые параметры:")
        logger.info(f"API_ID: {API_ID}")
        logger.info(f"CHANNEL_USERNAME: {CHANNEL_USERNAME}")
        logger.info(f"CHANNEL_ID: {CHANNEL_ID}")
        
        # Получаем путь к файлу сессии
        session_file = get_session_file()
        logger.info(f"Используется файл сессии: {session_file}")
        
        # Инициализация клиента
        client = TelegramClient(session_file, API_ID, API_HASH)
        logger.info("Клиент Telegram инициализирован")
        
        await client.start()
        logger.info("Клиент Telegram успешно запущен")
        
        # Определение канала для публикации
        if CHANNEL_ID:
            # Для закрытого канала нужно получить access_hash
            channel = await client.get_entity(int(CHANNEL_ID))
            logger.info(f"Получен доступ к каналу: {channel.title}")
        else:
            channel = CHANNEL_USERNAME
            logger.info(f"Используется CHANNEL_USERNAME: {CHANNEL_USERNAME}")
        
        # Публикация поста
        if media_path:
            logger.info(f"Публикация поста с медиафайлом: {media_path}")
            message = await client.send_file(
                channel,
                media_path,
                caption=text,
                parse_mode=parse_mode
            )
        else:
            logger.info("Публикация текстового поста")
            message = await client.send_message(
                channel,
                text,
                parse_mode=parse_mode
            )
        
        msg_id = message.id
        logger.info(f"Пост успешно опубликован в канал {CHANNEL_TITLE} с ID: {msg_id}")
        await client.disconnect()
        return msg_id
        
    except Exception as e:
        logger.error(f"Ошибка при публикации поста: {str(e)}")
        return None

async def post_random_photo(text: str = None):
    """
    Публикует пост со случайным одобренным фото
    
    Args:
        text (str, optional): Текст поста. Если не указан, будет использован текст по умолчанию
    
    Returns:
        int: ID сообщения, если пост успешно опубликован, None в случае ошибки
    """
    # Получаем случайное фото
    photo_data = get_random_approved_photo()
    if not photo_data:
        logger.error("Не удалось получить фото из базы данных")
        return None
    
    # Получаем путь к фото
    photo_path = get_photo_path(photo_data)
    if not photo_path or not os.path.exists(photo_path):
        logger.error(f"Файл фото не найден: {photo_path}")
        return None
    
    # Если текст не указан, используем текст по умолчанию
    if text is None:
        text = """
Доброе утро!

Ph: <a href="https://t.me/+YnW98uCRC6ZkNjAy">Homoludens</a>
        """
    
    # Публикуем пост
    msg_id = await post_to_channel(text, photo_path)
    
    # Если пост успешно опубликован, обновляем статус фото
    if msg_id:
        photo_path = photo_data.get('path')
        if photo_path:
            logger.info(f"Обновление статуса фото {photo_path} на {STATUS_PUBLISHED}")
            if update_photo_status(photo_path, STATUS_PUBLISHED, msg_id):
                logger.info(f"Статус фото {photo_path} успешно обновлен на {STATUS_PUBLISHED}")
            else:
                logger.error(f"Не удалось обновить статус фото {photo_path}")
    
    return msg_id

# Пример использования
if __name__ == "__main__":
    import asyncio
    
    async def main():
        logger.info("Начинаем публикацию поста со случайным фото...")
        result = await post_random_photo()
        
        if result:
            logger.info("Пост со случайным фото успешно опубликован!")
        else:
            logger.error("Не удалось опубликовать пост")
    
    asyncio.run(main()) 