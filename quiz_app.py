import sqlite3
import hashlib
import getpass
import random
import string
import sys

conn = None
cur = None

conn = sqlite3.connect("quiz.db")
cur = conn.cursor()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_username():
    return "user" + ''.join(random.choices(string.digits, k=5))

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def input_with_exit(prompt):
    val = input(prompt)
    if val.strip().lower() == "exit":
        print("👋 Zakończono program.")
        if conn:
            conn.close()
        sys.exit(0)
    return val

def getpass_with_exit(prompt):
    val = getpass.getpass(prompt)
    if val.strip().lower() == "exit":
        print("👋 Zakończono program.")
        if conn:
            conn.close()
        sys.exit(0)
    return val

def register():
    print("\n[Rejestracja]")
    while True:
        username = input_with_exit("Nazwa użytkownika (Enter = wygeneruj): ").strip()
        if not username:
            username = generate_username()
            print(f"🔹 Wygenerowano nazwę: {username}")

        try:
            cur.execute("SELECT 1 FROM users WHERE username=?", (username,))
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            continue

        if cur.fetchone():
            print("❌ Taki użytkownik już istnieje. Wybierz inną nazwę.")
            continue
        password = getpass_with_exit("Hasło (Enter = wygeneruj): ").strip()
        if not password:
            password = generate_password()
            print(f"🔹 Wygenerowano hasło: {password}")
        print(f"Twoje dane:\n  Nazwa: {username}\n  Hasło: {password}")
        confirm = input_with_exit("Czy na pewno chcesz się zarejestrować? (t/n): ").strip().lower()
        if confirm != "t":
            print("❌ Rejestracja anulowana.")
            return
        hashed = hash_password(password)
        try:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
            conn.commit()
            print("✅ Zarejestrowano.")
            break
        except sqlite3.IntegrityError:
            print("❌ Użytkownik już istnieje.")
            break
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            break

def login():
    print("\n[Logowanie]")
    username = input_with_exit("Nazwa użytkownika: ").strip()
    if not username:
        print("❌ Nazwa użytkownika nie może być pusta.")
        return None
    password = getpass_with_exit("Hasło: ").strip()
    if not password:
        print("❌ Hasło nie może być puste.")
        return None
    hashed = hash_password(password)
    try:
        cur.execute("SELECT id FROM users WHERE username=? AND password_hash=?", (username, hashed))
        row = cur.fetchone()
    except Exception as e:
        print(f"❌ Błąd bazy danych: {e}")
        return None
    if row:
        print("✅ Zalogowano.")
        confirm = input_with_exit("Czy na pewno chcesz się zalogować na to konto? (t/n): ").strip().lower()
        if confirm != "t":
            print("❌ Logowanie anulowane.")
            return None
        return row[0]
    else:
        print("❌ Błędne dane.")
        return None

def change_password(user_id):
    print("\n[Zmiana hasła]")
    while True:
        old_pass = getpass_with_exit("Podaj stare hasło: ").strip()
        if not old_pass:
            print("❌ Hasło nie może być puste.")
            continue
        hashed_old = hash_password(old_pass)
        try:
            cur.execute("SELECT 1 FROM users WHERE id=? AND password_hash=?", (user_id, hashed_old))
            if not cur.fetchone():
                print("❌ Stare hasło nieprawidłowe.")
                continue
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
        new_pass = getpass_with_exit("Nowe hasło (Enter = wygeneruj): ").strip()
        if not new_pass:
            new_pass = generate_password()
            print(f"🔹 Wygenerowano hasło: {new_pass}")
        confirm_pass = getpass_with_exit("Powtórz nowe hasło: ").strip()
        if new_pass != confirm_pass:
            print("❌ Hasła nie są takie same.")
            continue
        try:
            cur.execute("UPDATE users SET password_hash=? WHERE id=?", (hash_password(new_pass), user_id))
            conn.commit()
            print("✅ Hasło zmienione.")
            break
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            break

def run_quiz(user_id):
    print("\n[Wybierz zestaw pytań]")
    try:
        cur.execute("SELECT DISTINCT question_set FROM questions")
        sets = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"❌ Błąd bazy danych: {e}")
        return
    if not sets:
        print("❌ Brak dostępnych zestawów pytań.")
        return
    for i, s in enumerate(sets, 1):
        print(f"{i}. {s}")
    choice = input_with_exit("Podaj numer zestawu lub Enter dla wszystkich: ").strip()

    if choice and (not choice.isdigit() or not (1 <= int(choice) <= len(sets))):
        print("❌ Nieprawidłowy wybór zestawu. Wybrano wszystkie pytania.")
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions ORDER BY RANDOM() LIMIT 10")
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
    elif choice.isdigit() and 1 <= int(choice) <= len(sets):
        selected = sets[int(choice) - 1]
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions WHERE question_set=? ORDER BY RANDOM() LIMIT 10", (selected,))
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
    else:
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions ORDER BY RANDOM() LIMIT 10")
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return

    questions = cur.fetchall()
    if not questions:
        print("❌ Brak pytań w wybranym zestawie.")
        return

    score = 0
    user_answers = []
    for i, q in enumerate(questions, 1):
        print(f"\nPytanie {i}: {q[0]}")
        print(f"a) {q[1]}")
        print(f"b) {q[2]}")
        print("Wpisz 'menu' aby przerwać quiz i wrócić do panelu użytkownika.")
        while True:
            answer = input_with_exit("Odpowiedź (a/b): ").lower().strip()
            if answer == "menu":
                print("🔙 Powrót do panelu użytkownika.")
                return
            if answer not in ('a', 'b'):
                print("❌ Wpisz 'a' lub 'b'.")
            else:
                break
        user_answers.append((q[0], answer, q[3]))
        if answer == q[3]:
            print("✅ Dobrze!")
            score += 1
        else:
            print(f"❌ Źle. Poprawna: {q[3]}")

    print(f"\nWynik: {score}/{len(questions)}")
    try:
        cur.execute("INSERT INTO stats (user_id, score, total_questions) VALUES (?, ?, ?)",
                    (user_id, score, len(questions)))
        conn.commit()
    except Exception as e:
        print(f"❌ Błąd zapisu wyniku: {e}")

    print("\nPoprawne odpowiedzi:")
    for idx, (pytanie, odp, poprawna) in enumerate(user_answers, 1):
        status = "✅" if odp == poprawna else "❌"
        print(f"{idx}. {pytanie}\n   Twoja: {odp} | Poprawna: {poprawna} {status}")
    print("\n[Wybierz zestaw pytań]")
    try:
        cur.execute("SELECT DISTINCT question_set FROM questions")
        sets = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"❌ Błąd bazy danych: {e}")
        return
    if not sets:
        print("❌ Brak dostępnych zestawów pytań.")
        return
    for i, s in enumerate(sets, 1):
        print(f"{i}. {s}")
    choice = input_with_exit("Podaj numer zestawu lub Enter dla wszystkich: ").strip()

    if choice and (not choice.isdigit() or not (1 <= int(choice) <= len(sets))):
        print("❌ Nieprawidłowy wybór zestawu. Wybrano wszystkie pytania.")
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions")
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
    elif choice.isdigit() and 1 <= int(choice) <= len(sets):
        selected = sets[int(choice) - 1]
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions WHERE question_set=?", (selected,))
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
    else:
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions")
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return

    questions = cur.fetchall()
    if not questions:
        print("❌ Brak pytań w wybranym zestawie.")
        return
    random.shuffle(questions)
    questions = questions[:10]

    score = 0
    user_answers = []
    for i, q in enumerate(questions, 1):
        print(f"\nPytanie {i}: {q[0]}")
        print(f"a) {q[1]}")
        print(f"b) {q[2]}")
        print("Wpisz 'menu' aby przerwać quiz i wrócić do panelu użytkownika.")
        while True:
            answer = input_with_exit("Odpowiedź (a/b): ").lower().strip()
            if answer == "menu":
                print("🔙 Powrót do panelu użytkownika.")
                return
            if answer not in ('a', 'b'):
                print("❌ Wpisz 'a' lub 'b'.")
            else:
                break
        user_answers.append((q[0], answer, q[3]))
        if answer == q[3]:
            print("✅ Dobrze!")
            score += 1
        else:
            print(f"❌ Źle. Poprawna: {q[3]}")

    print(f"\nWynik: {score}/{len(questions)}")
    try:
        cur.execute("INSERT INTO stats (user_id, score, total_questions) VALUES (?, ?, ?)",
                    (user_id, score, len(questions)))
        conn.commit()
    except Exception as e:
        print(f"❌ Błąd zapisu wyniku: {e}")

    print("\nPoprawne odpowiedzi:")
    for idx, (pytanie, odp, poprawna) in enumerate(user_answers, 1):
        status = "✅" if odp == poprawna else "❌"
        print(f"{idx}. {pytanie}\n   Twoja: {odp} | Poprawna: {poprawna} {status}")
    print("\n[Wybierz zestaw pytań]")
    try:
        cur.execute("SELECT DISTINCT question_set FROM questions")
        sets = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"❌ Błąd bazy danych: {e}")
        return
    if not sets:
        print("❌ Brak dostępnych zestawów pytań.")
        return
    for i, s in enumerate(sets, 1):
        print(f"{i}. {s}")
    choice = input_with_exit("Podaj numer zestawu lub Enter dla wszystkich: ").strip()

    if choice and (not choice.isdigit() or not (1 <= int(choice) <= len(sets))):
        print("❌ Nieprawidłowy wybór zestawu. Wybrano wszystkie pytania.")
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions")
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
    elif choice.isdigit() and 1 <= int(choice) <= len(sets):
        selected = sets[int(choice) - 1]
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions WHERE question_set=?", (selected,))
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return
    else:
        try:
            cur.execute("SELECT question, option_a, option_b, correct FROM questions")
        except Exception as e:
            print(f"❌ Błąd bazy danych: {e}")
            return

    questions = cur.fetchall()
    if not questions:
        print("❌ Brak pytań w wybranym zestawie.")
        return
    random.shuffle(questions)
    questions = questions[:10]

    score = 0
    user_answers = []
    for i, q in enumerate(questions, 1):
        print(f"\nPytanie {i}: {q[0]}")
        print(f"a) {q[1]}")
        print(f"b) {q[2]}")
        while True:
            answer = input_with_exit("Odpowiedź (a/b): ").lower().strip()
            if answer not in ('a', 'b'):
                print("❌ Wpisz 'a' lub 'b'.")
            else:
                break
        user_answers.append((q[0], answer, q[3]))
        if answer == q[3]:
            print("✅ Dobrze!")
            score += 1
        else:
            print(f"❌ Źle. Poprawna: {q[3]}")

    print(f"\nWynik: {score}/{len(questions)}")
    try:
        cur.execute("INSERT INTO stats (user_id, score, total_questions) VALUES (?, ?, ?)",
                    (user_id, score, len(questions)))
        conn.commit()
    except Exception as e:
        print(f"❌ Błąd zapisu wyniku: {e}")

    print("\nPoprawne odpowiedzi:")
    for idx, (pytanie, odp, poprawna) in enumerate(user_answers, 1):
        status = "✅" if odp == poprawna else "❌"
        print(f"{idx}. {pytanie}\n   Twoja: {odp} | Poprawna: {poprawna} {status}")

def show_stats(user_id):
    print("\n[Twoje statystyki]")
    try:
        cur.execute("SELECT COUNT(*), AVG(score), MAX(score) FROM stats WHERE user_id=?", (user_id,))
        count, avg, max_score = cur.fetchone()
    except Exception as e:
        print(f"❌ Błąd bazy danych: {e}")
        return
    print(f"Rozegranych quizów: {count}")
    print(f"Średni wynik: {round(avg or 0, 2)}")
    print(f"Najlepszy wynik: {max_score or 0}")

def show_instructions():
    print("""
📝 Instrukcja obsługi:
- W dowolnym momencie możesz wpisać 'exit', aby zakończyć program.
- W menu wybierz odpowiednią opcję wpisując jej numer.
- Podczas rejestracji możesz wygenerować nazwę użytkownika i hasło.
- Po zalogowaniu możesz zmienić hasło, rozwiązać quiz lub sprawdzić statystyki.
- Po każdym quizie zobaczysz poprawne odpowiedzi do wszystkich pytań.
""")

def main():
    show_instructions()
    while True:
        print("\n[MENU]")
        print("1. Zaloguj się")
        print("2. Zarejestruj się")
        print("3. Wyjdź")
        choice = input_with_exit("Wybór: ").strip()

        if choice == '1':
            user_id = login()
            if user_id:
                while True:
                    print("\n[Panel użytkownika]")
                    print("1. Rozpocznij quiz")
                    print("2. Statystyki")
                    print("3. Zmień hasło")
                    print("4. Wyloguj")
                    sub = input_with_exit("Wybór: ").strip()
                    if sub == '1':
                        run_quiz(user_id)
                    elif sub == '2':
                        show_stats(user_id)
                    elif sub == '3':
                        change_password(user_id)
                    elif sub == '4':
                        break
                    else:
                        print("❌ Nieprawidłowy wybór.")
        elif choice == '2':
            register()
        elif choice == '3':
            print("👋 Do widzenia!")
            if conn:
                conn.close()
            break
        else:
            print("❌ Nieprawidłowy wybór.")

    if conn:
        conn.close()

if __name__ == "__main__":
    main()