import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
SESSION_PATH = os.getenv("TG_SESSION", "tg-post.session")


# Channel configuration
CHANNEL_USERNAME = os.getenv("TG_CHANNEL_USERNAME", "")
CHANNEL_ID = os.getenv("TG_CHANNEL_ID", "2594554974")  # ID для закрытых каналов
CHANNEL_TITLE = os.getenv("TG_CHANNEL_TITLE", "новый канал")

# Logging configuration
LOG_LEVEL = os.getenv("TG_LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("TG_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = os.getenv("TG_LOG_FILE", "telegram-post.log")

# Параметры PostgreSQL
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '192.168.2.228')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'DB')
POSTGRES_USER = os.getenv('POSTGRES_USER', '')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')


TABLE_NAME = os.getenv('TABLE_NAME', "photos_ok")

# Параметры подключения к PostgreSQL в виде словаря
PG_CONNECTION_PARAMS = {
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT,
    'database': POSTGRES_DB,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD
} 

# Статусы фотографий
STATUS_REVIEW = os.getenv('STATUS_REVIEW', "review")
STATUS_APPROVED = os.getenv('STATUS_APPROVED', "approved")
STATUS_REJECTED = os.getenv('STATUS_REJECTED', "rejected")
STATUS_PUBLISHED = os.getenv('STATUS_PUBLISHED', "published")
STATUS_NORMAL = os.getenv('STATUS_NORMAL', "normal")
STATUS_NUDE_WITH_FACE = os.getenv('STATUS_NUDE_WITH_FACE', "nude_with_face")
