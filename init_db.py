import sqlite3

def init_db():
    # Création du fichier database.db [cite: 9]
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Création des tables clients et produits [cite: 9, 10]
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients 
                      (id INTEGER PRIMARY KEY, nom TEXT, type TEXT, solde REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS produits 
                      (id INTEGER PRIMARY KEY, nom TEXT, prix REAL, categorie TEXT)''')

    # Insertion des données initiales [cite: 10]
    clients = [(1, 'Sophie Bernard', 'VIP', 28900.0), (2, 'Jean Dupont', 'Standard', 1500.0)]
    produits = [(1, 'Assurance Vie Alpha', 500.0, 'Épargne'), (2, 'PEA Performance', 1000.0, 'Bourse')]
    
    cursor.executemany('INSERT OR IGNORE INTO clients VALUES (?,?,?,?)', clients)
    cursor.executemany('INSERT OR IGNORE INTO produits VALUES (?,?,?,?)', produits)
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()