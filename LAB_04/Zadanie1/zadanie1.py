import sqlite3
import requests

# 1. Pobierz dane z API
print("Pobieranie danych z API...")
response = requests.get("https://randomuser.me/api/?results=30")
users = response.json()["results"]

# Połącz się z bazą danych (stworzy plik users.db w folderze projektu)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 2. Stwórz tabelę Users
# Najpierw usuwamy starą tabelę, jeśli istnieje, żeby móc uruchamiać skrypt wielokrotnie
cursor.execute("DROP TABLE IF EXISTS Users")

cursor.execute('''
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    age INTEGER,
    gender TEXT,
    country TEXT
)
''')

# 3. Wstaw dane z parametryzacją
print("Wstawianie danych do bazy...")
insert_query = """
INSERT INTO Users (first_name, last_name, email, age, gender, country)
VALUES (?, ?, ?, ?, ?, ?)
"""

for u in users:
    # Wyciągamy dane zagnieżdżone w strukturze JSON-a API
    data_tuple = (
        u['name']['first'],
        u['name']['last'],
        u['email'],
        u['dob']['age'],
        u['gender'],
        u['location']['country']
    )
    cursor.execute(insert_query, data_tuple)

# Zapisujemy zmiany w bazie
conn.commit()

# 4. Zapytania analityczne
print("\n--- WYNIKI ANALIZY ---")

# A. Ile jest mężczyzn, a ile kobiet?
print("\nPodział według płci:")
cursor.execute("SELECT gender, COUNT(*) FROM Users GROUP BY gender")
for row in cursor.fetchall():
    print(f"{row[0].capitalize()}: {row[1]}")

# B. Jaki jest średni wiek?
cursor.execute("SELECT AVG(age) FROM Users")
avg_age = cursor.fetchone()[0]
print(f"\nŚredni wiek użytkowników: {avg_age:.2f} lat")

# C. W ilu krajach mieszkają? (unikalne kraje)
cursor.execute("SELECT COUNT(DISTINCT country) FROM Users")
unique_countries = cursor.fetchone()[0]
print(f"Użytkownicy mieszkają w tylu różnych krajach: {unique_countries}")

# Bonus: Podział na kraje (top 5)
print("\nTop 5 krajów:")
cursor.execute("SELECT country, COUNT(*) FROM Users GROUP BY country ORDER BY COUNT(*) DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} osób")

# Zamknij połączenie
conn.close()
