# 🤖 Agent Analyste Financier Intelligent

Assistant intelligent spécialisé dans l'analyse financière combinant GPT-4o, base de données SQL, données boursières en temps réel et exécution de code Python.

---

## ⚙️ Installation

### 1. Cloner le projet
git clone <votre-lien-github>
cd "Projet Agent IA"

### 2. Créer l'environnement virtuel
python -m venv venv

# Activation sur Windows :
venv\Scripts\activate

# Activation sur macOS/Linux :
source venv/bin/activate

### 3. Installer les dépendances
pip install -r requirements.txt

---

## 🚀 Configuration et Lancement

### 1. Variables d'environnement
Créez un fichier .env à la racine du projet sur le modèle du fichier .env.example :
OPENAI_API_KEY=votre_cle_ici
TAVILY_API_KEY=votre_cle_ici

### 2. Initialiser la Base de Données
Avant de lancer l'agent, vous devez créer et remplir la base SQLite :
python init_db.py

### 3. Lancer l'Agent
L'application peut être lancée en mode console ou via l'interface web :

Mode Console :
python main.py

Mode Web (Streamlit) :
streamlit run app.py

---

## 🧪 Scénario de Test (Mémoire)

L'agent est configuré pour gérer le contexte sur plusieurs échanges :
1. Q1 : "Donne-moi les infos du client Sophie Bernard" (Récupération du profil et solde).
2. Q2 : "Quel produit lui recommandes-tu ?" (Suggère un produit adapté comme l'Assurance Vie Alpha).
3. Q3 : "Calcule le prix TTC et dis-moi si elle peut se le permettre" (Calcul via PythonREPL et vérification du solde stocké en mémoire).

---

## 📂 Structure du Projet
* main.py : Logique de l'agent et tests console.
* app.py : Interface utilisateur Streamlit.
* init_db.py : Script d'initialisation SQL.
* tools/ : Modules techniques (finance, database, calculs).
* .env.example : Modèle de configuration des clés API.