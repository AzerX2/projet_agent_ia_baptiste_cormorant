from langchain_experimental.tools import PythonREPLTool # [cite: 37, 41]

python_repl = PythonREPLTool()
python_repl.description = (
    "Exécute du code Python pour des calculs complexes ou traitements "
    "de données non couverts par les autres outils. "
    "Entrée: code Python valide sous forme de chaîne."
) # [cite: 44, 46, 47, 48]

# ATTENTION SECURITE : cet outil exécute du code arbitraire.
# Ne jamais utiliser en production sans sandbox. [cite: 40, 49]