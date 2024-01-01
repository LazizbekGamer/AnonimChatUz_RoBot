from loader import dp
from database.admindb.db import execute
import asyncio



async def create_table(dp):
    execute('''
    CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_one TEXT,
    chat_two TEXT
    );
    ''')
    
    execute('''
    CREATE TABLE IF NOT EXISTS queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    gender TEXT
    );
    ''')
    
    execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    active TEXT,
    gender TEXT,
    balance INTEGER DEFAULT 0,
    yosh INTEGER DEFAULT 0
    );
    ''')



def create_table_start(dp):
    execute('''
    CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_one TEXT,
    chat_two TEXT
    );
    ''')
    
    execute('''
    CREATE TABLE IF NOT EXISTS queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    gender TEXT
    );
    ''')
    
    execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    active TEXT,
    gender TEXT,
    balance INTEGER DEFAULT 0,
    yosh INTEGER DEFAULT 0
    );
    ''')
