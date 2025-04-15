import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
import random
from config import PG_CONNECTION_PARAMS, TABLE_NAME, STATUS_PUBLISHED

def get_table_structure():
    """
    Получает структуру таблицы из базы данных
    
    Returns:
        list: Список полей таблицы
    """
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(**PG_CONNECTION_PARAMS)
        cur = conn.cursor()
        
        # Получаем структуру таблицы
        query = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{TABLE_NAME}'
            ORDER BY ordinal_position
        """
        
        cur.execute(query)
        columns = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return columns
        
    except Exception as e:
        print(f"Ошибка при получении структуры таблицы: {str(e)}")
        return []

def get_random_approved_photo():
    """
    Получает случайное одобренное фото из базы данных
    
    Returns:
        dict: Информация о фото или None, если фото не найдено
    """
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(**PG_CONNECTION_PARAMS)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Получаем случайное фото со статусом 'approved'
        query = f"""
            SELECT *
            FROM {TABLE_NAME}
            WHERE status = 'approved'
            ORDER BY RANDOM()
            LIMIT 1
        """
        
        cur.execute(query)
        photo = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return photo
        
    except Exception as e:
        print(f"Ошибка при получении фото из базы данных: {str(e)}")
        return None

def get_photo_path(photo_data):
    """
    Получает путь к фото из данных базы
    
    Args:
        photo_data (dict): Данные о фото из базы данных
    
    Returns:
        str: Путь к файлу фото
    """
    if not photo_data:
        return None
        
    # Используем поле path из базы данных
    return photo_data.get('path')

def update_photo_status(photo_path, new_status=STATUS_PUBLISHED, msg_id=None):
    """
    Обновляет статус фото в базе данных
    
    Args:
        photo_path (str): Путь к фото в базе данных
        new_status (str): Новый статус фото (по умолчанию STATUS_PUBLISHED из конфига)
        msg_id (int, optional): ID сообщения в Telegram
    
    Returns:
        bool: True если статус успешно обновлен, False в случае ошибки
    """
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(**PG_CONNECTION_PARAMS)
        cur = conn.cursor()
        
        # Обновляем статус фото и msg_id
        query = f"""
            UPDATE {TABLE_NAME}
            SET status = %s,
                msg_id = %s
            WHERE path = %s
        """
        
        cur.execute(query, (new_status, msg_id, photo_path))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Ошибка при обновлении статуса фото: {str(e)}")
        return False

# Выводим структуру таблицы при импорте модуля
if __name__ == "__main__":
    print(f"Структура таблицы {TABLE_NAME}:")
    columns = get_table_structure()
    for column in columns:
        print(f"  {column[0]}: {column[1]}") 