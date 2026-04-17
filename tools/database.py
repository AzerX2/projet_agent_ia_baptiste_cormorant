import sqlite3
from langchain_core.tools import tool

@tool
def rechercher_client(nom_client: str) -> str:
    """Recherche un client dans la base SQLite par son nom. (A1)"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Requête SQL pour récupérer les infos de Sophie Bernard [cite: 185, 186]
    cursor.execute("SELECT nom, type, solde FROM clients WHERE nom LIKE ?", (f"%{nom_client}%",))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"Client : {row[0]} | Type : {row[1]} | Solde : {row[2]:.2f} €"
    return f"Aucun client trouvé pour : {nom_client}"

@tool
def rechercher_produit(nom_produit: str) -> str:
    """Recherche un produit dans la base SQLite. (A1)"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nom, prix FROM produits WHERE nom LIKE ?", (f"%{nom_produit}%",))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"Produit : {row[0]} | Prix HT : {row[1]:.2f} €"
    return "Produit non trouvé."