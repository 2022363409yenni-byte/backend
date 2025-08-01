"""
Optional database module for future expansion
Currently using in-memory storage in main.py
"""

import sqlite3
from typing import List, Dict, Any
import json
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "wellness.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                message TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user preferences table (for future use)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                preferences TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_feedback(self, feedback_data: Dict[str, Any]) -> int:
        """Add feedback to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (name, email, message, category)
            VALUES (?, ?, ?, ?)
        ''', (
            feedback_data['name'],
            feedback_data.get('email'),
            feedback_data['message'],
            feedback_data.get('category', 'general')
        ))
        
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return feedback_id
    
    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """Get all feedback from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        feedback_list = [dict(row) for row in rows]
        conn.close()
        
        return feedback_list
    
    def save_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Save user preferences (for future use)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, preferences, updated_at)
            VALUES (?, ?, ?)
        ''', (user_id, json.dumps(preferences), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences (for future use)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT preferences FROM user_preferences WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return json.loads(row[0])
        return {}