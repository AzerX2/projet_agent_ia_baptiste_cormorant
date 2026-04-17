# TODO: Implémenter les outils financiers avec yfinance
# - get_stock_price(ticker: str) -> str
# - get_stock_news(ticker: str) -> str

import yfinance as yf
import datetime

def get_stock_price(ticker: str) -> str:
    """Récupère le cours réel, la variation et le volume via yfinance[cite: 13, 15]."""
    ticker = ticker.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        # On récupère les données du jour
        data = stock.history(period="1d")
        
        if data.empty:
            return f"Symbole '{ticker}' non trouvé ou pas de données disponibles[cite: 16]."
        
        cours = data['Close'].iloc[-1]
        ouverture = data['Open'].iloc[-1]
        variation_pct = ((cours - ouverture) / ouverture) * 100
        volume = data['Volume'].iloc[-1]
        tendance = '📈' if variation_pct >= 0 else '📉'
        
        # Affichage conforme aux attentes : cours réel, variation et volume [cite: 16]
        return f"{ticker} {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%) | Volume: {volume}"
    except Exception as e:
        return f"Erreur lors de la récupération pour {ticker}: {e} [cite: 16]"

def get_stock_news(ticker: str) -> str:
    """Récupère les dernières actualités pour un titre donné."""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news[:3] # On prend les 3 dernières news
        if not news:
            return f"Aucune actualité trouvée pour {ticker}."
        
        res = f"Actualités pour {ticker} :\n"
        for n in news:
            res += f"- {n['title']} (Source: {n['publisher']})\n"
        return res
    except Exception as e:
        return f"Erreur news: {e}"

# TODO: Importer les outils depuis tools/
# from tools.finance import get_stock_price, get_stock_news
# from tools.calculs import python_tool

# TODO: Initialiser le LLM
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0)

# TODO: Définir le prompt avec MessagesPlaceholder("agent_scratchpad")

# TODO: Créer l'agent avec create_tool_calling_agent + AgentExecutor

# TODO: Tests 1 à 4

import random, datetime

ACTIONS = {
    "AAPL":  { "nom": "Apple Inc.",       "prix_base": 182.50 },
    "MSFT":  { "nom": "Microsoft Corp.",   "prix_base": 415.20 },
    "GOOGL": { "nom": "Alphabet (Google)", "prix_base": 175.80 },
    "LVMH":  { "nom": "LVMH Moët Hennessy","prix_base": 750.00 },
    "TSLA":  { "nom": "Tesla Inc.",         "prix_base": 248.00 },
    "AIR":   { "nom": "Airbus SE",          "prix_base": 168.40 },
}

CRYPTOS = {
    "BTC": { "nom": "Bitcoin",  "prix_base": 67500.00 },
    "ETH": { "nom": "Ethereum", "prix_base": 3200.00  },
    "SOL": { "nom": "Solana",   "prix_base": 175.00   },
}

def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours simulé d'une action avec sa variation (+/-3%)."""
    symbole = symbole.strip().upper()
    if symbole not in ACTIONS:
        return f"Action '{symbole}' non trouvée."
    action = ACTIONS[symbole]
    variation_pct = random.uniform(-3.0, 3.0)   # Variation aléatoire
    cours = action['prix_base'] * (1 + variation_pct / 100)
    tendance = '📈' if variation_pct >= 0 else '📉'
    return f"{symbole} {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%)"
