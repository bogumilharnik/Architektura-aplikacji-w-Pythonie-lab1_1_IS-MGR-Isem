import numpy as np

# "Baza" filmów z embeddingami (3-wymiarowe wektory cech)
filmy = {
    "Incepcja":          np.array([0.8, 0.3, 0.9]),
    "Matrix":            np.array([0.75, 0.35, 0.85]),
    "Toy Story":         np.array([0.2, 0.9, 0.1]),
    "Shrek":             np.array([0.25, 0.85, 0.15]),
    "Szeregowiec Ryan":  np.array([0.6, 0.1, 0.7]),
}

def semantic_search(query_vec, database, top_k=3):
    results = []
    
    # Normalizacja wektora zapytania (obliczamy jego długość/normę)
    norm_query = np.linalg.norm(query_vec)
    
    for title, doc_vec in database.items():
        # Obliczamy iloczyn skalarny (dot product)
        dot_product = np.dot(query_vec, doc_vec)
        
        # Obliczamy normę wektora dokumentu
        norm_doc = np.linalg.norm(doc_vec)
        
        # Podobieństwo cosinusowe: dot_product / (norm1 * norm2)
        # To chroni nas przed wpływem długości wektora na wynik
        similarity = dot_product / (norm_query * norm_doc)
        
        results.append((title, similarity))
    
    # Sortujemy od największego podobieństwa (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:top_k]

# Testowanie wyszukiwarki
query = np.array([0.7, 0.3, 0.8])  # Zapytanie sugerujące "coś poważnego/sci-fi"
print(f"Wyniki wyszukiwania dla wektora {query}:")

results = semantic_search(query, filmy, top_k=3)

for i, (title, sim) in enumerate(results, 1):
    print(f"{i}. {title:18} | Podobieństwo: {sim:.4f}")
