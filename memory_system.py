#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система памяти и логики для Open Interpreter
"""

import os
import json
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from typing import Dict, List, Any, Optional

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠️ Библиотеки памяти недоступны")

class MemorySystem:
    """Система памяти для Open Interpreter"""
    
    def __init__(self, memory_dir: str = None):
        if memory_dir is None:
            memory_dir = Path.home() / ".open_interpreter" / "memory"
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # База данных для структурированной памяти
        self.db_path = self.memory_dir / "memory.db"
        self.init_database()
        
        # Векторная база для семантического поиска
        if MEMORY_AVAILABLE:
            self.chroma_client = chromadb.PersistentClient(path=str(self.memory_dir / "chroma"))
            self.collection = self.chroma_client.get_or_create_collection("memory")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Кэш недавних команд
        self.recent_commands = []
        self.max_recent = 50
        
    def init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    command TEXT,
                    result TEXT,
                    context TEXT,
                    success BOOLEAN,
                    tags TEXT,
                    hash TEXT UNIQUE
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT,
                    response TEXT,
                    frequency INTEGER DEFAULT 1,
                    last_used DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def remember_command(self, command: str, result: str, context: str = "", success: bool = True, tags: List[str] = None):
        """Запоминает выполненную команду"""
        if tags is None:
            tags = []
        
        # Создаем хэш для избежания дубликатов
        content_hash = hashlib.md5(f"{command}{result}".encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("""
                    INSERT INTO memories (command, result, context, success, tags, hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (command, result, context, success, json.dumps(tags), content_hash))
            except sqlite3.IntegrityError:
                # Обновляем существующую запись
                conn.execute("""
                    UPDATE memories 
                    SET timestamp = CURRENT_TIMESTAMP, result = ?, context = ?, success = ?
                    WHERE hash = ?
                """, (result, context, success, content_hash))
        
        # Добавляем в векторную базу для семантического поиска
        if MEMORY_AVAILABLE:
            try:
                embedding = self.model.encode([command]).tolist()[0]
                self.collection.add(
                    embeddings=[embedding],
                    documents=[f"{command} -> {result}"],
                    metadatas=[{"timestamp": datetime.now().isoformat(), "success": success}],
                    ids=[content_hash]
                )
            except Exception as e:
                print(f"⚠️ Ошибка добавления в векторную базу: {e}")
        
        # Кэш недавних команд
        self.recent_commands.append({
            "command": command,
            "result": result,
            "timestamp": datetime.now(),
            "success": success
        })
        
        if len(self.recent_commands) > self.max_recent:
            self.recent_commands.pop(0)
    
    def find_similar_commands(self, query: str, limit: int = 5) -> List[Dict]:
        """Находит похожие команды"""
        results = []
        
        # Поиск в векторной базе
        if MEMORY_AVAILABLE:
            try:
                query_embedding = self.model.encode([query]).tolist()[0]
                search_results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=limit
                )
                
                for doc, metadata in zip(search_results['documents'][0], search_results['metadatas'][0]):
                    results.append({
                        "document": doc,
                        "metadata": metadata,
                        "source": "vector"
                    })
            except Exception as e:
                print(f"⚠️ Ошибка векторного поиска: {e}")
        
        # Поиск в SQL базе
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT command, result, timestamp, success 
                FROM memories 
                WHERE command LIKE ? OR result LIKE ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            for row in cursor.fetchall():
                results.append({
                    "command": row[0],
                    "result": row[1],
                    "timestamp": row[2],
                    "success": row[3],
                    "source": "sql"
                })
        
        return results
    
    def get_recent_context(self, limit: int = 10) -> str:
        """Получает контекст недавних команд"""
        context = []
        for cmd in self.recent_commands[-limit:]:
            status = "✅" if cmd["success"] else "❌"
            context.append(f"{status} {cmd['command']} -> {cmd['result']}")
        
        return "\n".join(context)
    
    def save_preference(self, key: str, value: str):
        """Сохраняет пользовательские предпочтения"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO user_preferences (key, value, updated)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Получает пользовательские предпочтения"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else default
    
    def learn_pattern(self, pattern: str, response: str):
        """Изучает паттерн поведения"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT frequency FROM learned_patterns WHERE pattern = ?
            """, (pattern,))
            
            result = cursor.fetchone()
            if result:
                conn.execute("""
                    UPDATE learned_patterns 
                    SET frequency = frequency + 1, last_used = CURRENT_TIMESTAMP
                    WHERE pattern = ?
                """, (pattern,))
            else:
                conn.execute("""
                    INSERT INTO learned_patterns (pattern, response)
                    VALUES (?, ?)
                """, (pattern, response))
    
    def get_learned_response(self, pattern: str) -> Optional[str]:
        """Получает изученный ответ на паттерн"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT response FROM learned_patterns 
                WHERE pattern = ? 
                ORDER BY frequency DESC, last_used DESC
                LIMIT 1
            """, (pattern,))
            
            result = cursor.fetchone()
            return result[0] if result else None
    
    def cleanup_old_memories(self, days: int = 30):
        """Очищает старые воспоминания"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                DELETE FROM memories 
                WHERE timestamp < ? AND success = 0
            """, (cutoff_date.isoformat(),))
            
            # Сохраняем только успешные команды старше 30 дней
            conn.execute("""
                DELETE FROM memories 
                WHERE timestamp < ? AND success = 1
                AND id NOT IN (
                    SELECT id FROM memories 
                    WHERE timestamp < ? AND success = 1
                    ORDER BY timestamp DESC 
                    LIMIT 1000
                )
            """, (cutoff_date.isoformat(), cutoff_date.isoformat()))
    
    def get_stats(self) -> Dict[str, Any]:
        """Получает статистику памяти"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM memories")
            total_memories = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM memories WHERE success = 1")
            successful_memories = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM user_preferences")
            preferences_count = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM learned_patterns")
            patterns_count = cursor.fetchone()[0]
        
        return {
            "total_memories": total_memories,
            "successful_memories": successful_memories,
            "success_rate": successful_memories / total_memories if total_memories > 0 else 0,
            "preferences_count": preferences_count,
            "learned_patterns": patterns_count,
            "recent_commands": len(self.recent_commands)
        }
    
    def get_relevant_context(self, query: str) -> str:
        """Получает релевантный контекст для запроса"""
        try:
            similar_commands = self.find_similar_commands(query, limit=3)
            context = ""
            for cmd in similar_commands:
                if "document" in cmd:
                    context += f"{cmd['document']}\n"
            return context.strip()
        except Exception as e:
            print(f"⚠️ Ошибка получения контекста: {e}")
            return ""
    
    def get_recent_commands(self, limit: int = 5) -> List[Dict]:
        """Получает недавние команды"""
        return self.recent_commands[-limit:] if self.recent_commands else []

# Глобальный экземпляр системы памяти
memory_system = MemorySystem()
