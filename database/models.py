"""
Database models for TokenShift bot
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from cryptography.fernet import Fernet
import base64
import os

class DatabaseManager:
    """Database manager for handling encrypted storage"""
    
    def __init__(self, db_path: str = 'tokenshift.db'):
        self.db_path = db_path
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        self._init_database()
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Wallets table (encrypted private keys)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wallets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    network TEXT NOT NULL,
                    address TEXT NOT NULL,
                    encrypted_private_key TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    transaction_type TEXT NOT NULL,
                    from_token TEXT,
                    to_token TEXT,
                    amount REAL,
                    network TEXT,
                    transaction_hash TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Portfolio table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    token_symbol TEXT NOT NULL,
                    amount REAL NOT NULL,
                    network TEXT,
                    average_price REAL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Add or update user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
    
    def add_wallet(self, user_id: int, network: str, address: str, private_key: str):
        """Add encrypted wallet"""
        encrypted_key = self.encrypt_data(private_key)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO wallets (user_id, network, address, encrypted_private_key)
                VALUES (?, ?, ?, ?)
            ''', (user_id, network, address, encrypted_key))
            conn.commit()
    
    def get_wallet(self, user_id: int, network: str) -> Optional[Dict[str, Any]]:
        """Get user's wallet for specific network"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT address, encrypted_private_key FROM wallets
                WHERE user_id = ? AND network = ?
            ''', (user_id, network))
            result = cursor.fetchone()
            if result:
                return {
                    'address': result[0],
                    'private_key': self.decrypt_data(result[1])
                }
            return None
    
    def get_user_wallets(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all user's wallets"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT network, address FROM wallets
                WHERE user_id = ?
            ''', (user_id,))
            return [{'network': row[0], 'address': row[1]} for row in cursor.fetchall()]
    
    def add_transaction(self, user_id: int, transaction_type: str, from_token: str = None, 
                       to_token: str = None, amount: float = None, network: str = None, 
                       transaction_hash: str = None):
        """Add transaction record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, from_token, to_token, 
                                       amount, network, transaction_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, transaction_type, from_token, to_token, amount, network, transaction_hash))
            conn.commit()
    
    def update_portfolio(self, user_id: int, token_symbol: str, amount: float, 
                        network: str = None, average_price: float = None):
        """Update user's portfolio"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO portfolio (user_id, token_symbol, amount, network, 
                                                average_price, last_updated)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, token_symbol, amount, network, average_price))
            conn.commit()
    
    def get_portfolio(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's portfolio"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT token_symbol, amount, network, average_price, last_updated
                FROM portfolio WHERE user_id = ? AND amount > 0
            ''', (user_id,))
            return [{
                'token_symbol': row[0],
                'amount': row[1],
                'network': row[2],
                'average_price': row[3],
                'last_updated': row[4]
            } for row in cursor.fetchall()]
    
    def delete_user_wallets(self, user_id: int):
        """Delete all user's wallets"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM wallets WHERE user_id = ?', (user_id,))
            conn.commit()
    
    def has_wallets(self, user_id: int) -> bool:
        """Check if user has any wallets"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM wallets WHERE user_id = ?', (user_id,))
            return cursor.fetchone()[0] > 0
