import sqlite3
import json
import os

if os.path.exists("quiz.db"):
    print("Baza danych juz istnieje – pytania będą napisane, statystki i użytkownicy zostaną zachowani.")

    conn = sqlite3.connect("quiz.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM questions")
else:
    conn = sqlite3.connect("quiz.db")
    cur = conn.cursor()
    cur.executescript('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        correct TEXT NOT NULL,
        question_set TEXT NOT NULL
    );
    CREATE TABLE stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    ''')

quizes = [
    "Questions/quiz-inf.02.json",
    "Questions/quiz-inf.03.json",
    "Questions/quiz-inf.04.json",
    'Questions/quiz-german.json',
    'Questions/quiz-english.json',
    'Questions/quiz-it.json',
]

default_set = "inf.03"

for quiz in quizes:
    set_name = os.path.splitext(os.path.basename(quiz))[0] 
    with open(quiz, encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        cur.execute('''
        INSERT INTO questions (question, option_a, option_b, correct, question_set)
        VALUES (?, ?, ?, ?, ?)''',
        (item["name"], item["a"], item["b"], item["correct"], item.get("set", set_name)))

conn.commit()
conn.close()
print("✅ Pytania zaimportowane (nadpisane).")