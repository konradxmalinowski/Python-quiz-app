# 📝 Quiz App

![SQLite](https://img.shields.io/badge/SQLite-quiz--db-lightgrey?logo=sqlite)
![MIT License](https://img.shields.io/badge/license-MIT-green)

---

## Quiz App – Console Quiz Application

Quiz App is a modern, user-friendly console application for solving quizzes in various fields (IT, languages, and more). It supports user registration, login, random question selection, statistics, and password management. All data is stored locally in a SQLite database.

---

### 📚 Used Libraries

This project uses only Python standard libraries:

- **sqlite3**  
  Handles the local SQLite database where users, questions, and quiz statistics are stored.

- **json**  
  Loads and saves questions in JSON files (for importing questions and adding new ones via the admin panel).

- **os**  
  File and path operations (e.g., checking if question files exist).

- **hashlib**  
  Hashes user passwords using the SHA-256 algorithm.

- **getpass**  
  Securely collects passwords from the user (without displaying them on the screen).

- **random**  
  Randomly selects quiz questions and generates random usernames and passwords.

- **string**  
  Generates random characters for usernames and passwords.

- **sys**  
  Handles program exit (`exit`).

No external libraries or additional packages are required.

---

### ✨ Features

-  **User registration and login**  
  Secure account creation with password hashing.

-  **Random questions**  
  Get 10 random questions from a selected set or from all available sets.

-  **Multiple question sets**  
  Easily add your own JSON question sets in the `Pytania/` folder.

-  **User statistics**  
  Track your quiz history, average score, and best result.

-  **Password management**  
  Change your password at any time.

-  **Local SQLite database**  
  All user data and quiz results are stored locally.

- 🖥 **Simple console interface**  
  Intuitive navigation and clear instructions.

---

### 🚀 Getting Started

#### 1. Requirements

- Python 3.8 or newer
- No external dependencies required (uses Python standard library)

#### 2. Installation

Clone or download this repository and make sure you have the following structure:

```
QuizApp/
├── quiz_app.py
├── init_db.py
├── Questions/
│   ├── quiz-inf.02.json
│   ├── quiz-inf.03.json
│   ├── quiz-inf.04.json
│   ├── quiz-german.json
│   ├── quiz-english.json
│   └── quiz-it.json
```

#### 3. Initialize the database

Run the following command to create the database and import questions:

```bash
python init_db.py
```

You should see:  
`✅ Zaimportowano pytania.`

#### 4. Run the application

```bash
python quiz_app.py
```

---

### 🕹️ Usage

- **Register**: Create a new user account (username and password can be generated automatically).
- **Login**: Log in with your credentials.
- **Start Quiz**: Choose a question set or use all available questions. 10 random questions will be selected.
- **Answering**: Type `a` or `b` to answer. Type `menu` to return to the user panel, or `exit` to quit the app at any time.
- **Statistics**: View your quiz history, average score, and best result.
- **Change Password**: Update your password securely.

---

### 📦 Adding Your Own Questions

#### Option 1: Via the Admin Panel in the Application

1. Run the application and select **Admin panel** from the main menu.
2. Enter the administrator password (`admin123` by default).
3. Follow the instructions – provide the set name (e.g., `quiz-inf.02`), question text, answers `a` and `b`, and indicate the correct answer (`a` or `b`).
4. The question will be automatically saved to the appropriate JSON file in the `Pytania/` folder.

#### Option 2: Manually in a JSON File

1. Add a new JSON file to the `Pytania/` directory.  
   The file should be an array of objects, for example:

   ```json
   [
     {
       "name": "What is the capital of France?",
       "a": "Berlin",
       "b": "Paris",
       "correct": "b",
       "set": "quiz-geography"
     }
   ]
   ```

2. Add the file name to the `quizes` list in the `init_db.py` file.
3. Run `python init_db.py` again to import the new questions into the database.

---

**Tip:**  
You can add questions either via the admin panel or manually – both methods are equivalent.  
Questions must have the fields: `name`, `a`, `b`, `correct` (`a` or `b`), and `set` (set name).

### 🛠️ Customization

- **Question sets**: Organize questions by topic or language using separate JSON files.
- **Database**: All data is stored in `quiz.db` (SQLite). You can browse it with any SQLite viewer.
- **Extending**: The code is modular and easy to extend with new features (e.g., more answer options, categories, etc.).

---

### 💡 Tips

- Type `exit` at any prompt to quit the application.
- Type `menu` during a quiz to return to the user panel without finishing the quiz.
- All passwords are securely hashed using SHA-256.

---

### 📄 License

```
MIT License
Copyright (c) 2025 Konrad Malinowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
