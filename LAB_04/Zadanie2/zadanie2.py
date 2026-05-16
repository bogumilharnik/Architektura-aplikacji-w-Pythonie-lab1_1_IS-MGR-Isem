from pymongo import MongoClient
import requests

# 1. Połącz z MongoDB
# Zakładamy, że MongoDB działa lokalnie na standardowym porcie.
# Jeśli używasz Atlasa, wklej tutaj swój Connection String.
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client.lab4
    networks_col = db["networks"]
    
    # Opcjonalnie: czyścimy kolekcję, żeby nie dublować danych przy każdym uruchomieniu
    networks_col.delete_many({})
    print("Połączono z MongoDB.")
except Exception as e:
    print(f"Błąd połączenia: {e}")
    exit()

# 2. Pobierz dane z API GeckoTerminal
print("Pobieranie danych o sieciach...")
url = "https://api.geckoterminal.com/api/v2/networks"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["data"] # API zwraca listę w kluczu "data"
else:
    print(f"Błąd API: {response.status_code}")
    exit()

# 3. Wstaw dokumenty
# insert_many jest wydajniejsze niż pętla z insert_one
if data:
    result = networks_col.insert_many(data)
    print(f"Wstawiono {len(result.inserted_ids)} dokumentów.")

# 4. Agregacja -- ile sieci per typ
# Pipeline działa jak taśmociąg: najpierw grupujemy, potem sortujemy
print("\n--- WYNIKI AGREGACJI (Sieci per typ) ---")

pipeline = [
    {
        "$group": {
            "_id": "$type",           # Grupowanie po głównym polu 'type'
            "count": {"$sum": 1}      # Liczenie wystąpień
        }
    },
    {
        "$sort": {"count": -1}        # Sortowanie od największej liczby
    }
]

# UWAGA: Jeśli w strukturze API typ jest głębiej (np. w attributes), 
# należy zmienić "_id" na "$attributes.type". 
# W GeckoTerminal pole "type" jest zazwyczaj na najwyższym poziomie dokumentu.

for doc in networks_col.aggregate(pipeline):
    typ = doc['_id']
    liczba = doc['count']
    print(f"Typ: {typ:15} | Liczba sieci: {liczba}")

# Zamknij połączenie
client.close()
