import sqlite3
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_file="expenses.db"):
        self.conn = sqlite3.connect(db_file)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )""")
        self.conn.commit()

    def add_expense(self, expense: Dict):
        self.conn.execute(
            "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
            (expense['category'], expense['amount'], expense['date'])
        )
        self.conn.commit()

    def get_expenses(self, filters: Optional[Dict] = None) -> List[tuple]:
        query = "SELECT id, category, amount, date FROM expenses"
        params = []
        
        if filters:
            conditions = []
            if filters.get('start_date'):
                conditions.append("date >= ?")
                params.append(filters['start_date'])
            if filters.get('end_date'):
                conditions.append("date <= ?")
                params.append(filters['end_date'])
            if filters.get('date'):
                conditions.append("date = ?")
                params.append(filters['date'])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY date DESC"
        return self.conn.execute(query, params).fetchall()

    def __del__(self):
        self.conn.close()