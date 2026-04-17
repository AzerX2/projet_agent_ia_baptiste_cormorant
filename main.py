from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor, tool
from langchain_tavily import TavilySearch

from langchain_experimental.tools import PythonREPLTool

from tools.database import rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action

load_dotenv()


def _clean_env_key(name: str) -> str:
    raw = os.getenv(name, "")
    if not raw:
        return ""
    cleaned = raw.strip().strip('"').strip("'").replace("\r", "").replace("\n", "")
    os.environ[name] = cleaned
    return cleaned


openai_api_key = _clean_env_key("OPENAI_API_KEY")
_clean_env_key("TAVILY_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY est manquante ou vide dans l'environnement.")

llm = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4o",
    temperature=0
)

@tool
def get_stock_price(symbole: str) -> str:
    """Retourne le cours d'une action a partir de son symbole (ex: AAPL, MSFT)."""
    return obtenir_cours_action(symbole)

tavily_tool = TavilySearch(
    max_results=3,
    topic="finance",
    description="Utile pour répondre aux questions sur l'actualité financière et les entreprises."
)

python_tool = PythonREPLTool()
python_tool.description = (
    "Exécute du code Python pour des calculs complexes. "
    "Entrée: code Python valide. Utilisez print() pour voir le résultat."
    "Utilise python_tool avec print() pour afficher les résultats des calculs."
)

tools = [
    get_stock_price, 
    tavily_tool, 
    python_tool, 
    rechercher_client, 
    rechercher_produit
]

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "Tu es un assistant analyste financier expert.\n"
     "- Pour les recommandations, propose TOUJOURS un produit réel de ta base (ex: 'PEA Performance' ou 'Assurance Vie Alpha').\n"
     "- Utilise python_tool pour les calculs de prix TTC.\n"
     "- Souviens-toi des échanges précédents."),
    MessagesPlaceholder(variable_name="chat_history"), 
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

chat_history = []


def run_agent(user_input: str):
    result = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    output = result.get("output", "")
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=output))
    return result

if __name__ == "__main__":
    print("\n=== Test A3 – Actualités (Tavily) ===")
    run_agent("Quelles sont les dernières actualités sur les résultats trimestriels de LVMH ?")

    print("\n=== Test B2 – Calcul (PythonREPL) ===")
    run_agent("Si j'investis 5000€ sur Apple et que l'action augmente de 8.5% par an pendant 3 ans, quel sera mon capital final ?")

    print("\n=== Test C2 – Scénario Mémoire en 3 étapes ===")
    
    print("\n-- Étape 1 --")
    run_agent("Donne-moi les infos du client Sophie Bernard")
    
    print("\n-- Étape 2 --")
    run_agent("Quel produit lui recommandes-tu ?")
    
    print("\n-- Étape 3 --")
    response = run_agent("Calcule le prix TTC et dis-moi si elle peut se le permettre avec son solde actuel.")
    print(response["output"])