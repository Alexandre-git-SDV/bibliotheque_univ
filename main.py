import os
from LIVRE.livre import menu_bibliothecaire
from ETUDIANT.etudiant import menu_etudiant
from dotenv import load_dotenv  # pip install python-dotenv
import psycopg2  # pip install psycopg2-binary
from sqlalchemy import create_engine  # pip install sqlalchemy
from sqlalchemy.orm import sessionmaker

# Charge le fichier .env
load_dotenv()

# Variables simples depuis .env
host = os.getenv('DB_HOST')      # ex: localhost
port = os.getenv('DB_PORT')      # ex: 5432
dbname = os.getenv('DB_NAME')    # ex: biblio_test
user = input("Entrer votre nom d'utilisateur: ")      # ex: 
password = input("Entrer votre mot de passe: ")  # ton mot de passe

print("Variables chargées depuis .env")
print(f"User est connecté : {user}")
print(f"Connexion à : {host}:{port}/{dbname}")

# Définition du menu (doit être avant son appel)
def menu():
    print("\n=== Menu principal ===")
    print(f"Connecté en tant que: {user}")
    
    match user:
        case 'postgres':
            menu_bibliothecaire()
        case 'etudiant_ro':
            menu_etudiant()
        case 'bibliothecaire':
            menu_bibliothecaire()
        case _:
            print(f"Utilisateur '{user}' non reconnu. Connexion terminée.")

# Connection via psycopg2
try:
    # Crée la connexion psycopg2 (adaptateur direct)
    connexion = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    # Cursor = "pointeur" pour exécuter SQL
    curseur = connexion.cursor()
    
    # Test simple : version PostgreSQL
    curseur.execute("SELECT version();")
    resultat = curseur.fetchone()
    print("SUCCESS")
    print(f"PostgreSQL : {resultat[0][:10]}")
    
    # Test table biblio
    curseur.execute("SELECT COUNT(*) FROM etudiants;")
    nb_etudiants = curseur.fetchone()[0]
    print(f"{nb_etudiants} étudiants chargés")
    
    # Test table livre
    curseur.execute("SELECT COUNT(*) FROM livre;")
    nb_livres = curseur.fetchone()[0]
    print(f"\n{nb_livres} livres chargés")
    
    # Test table emprunt
    curseur.execute("SELECT COUNT(*) FROM emprunt;")
    nb_emprunts = curseur.fetchone()[0]
    print(f"\n{nb_emprunts} emprunts chargés")
    
    # Ferme proprement
    curseur.close()
    connexion.close()
    
    # Initialisation des sessions SQLAlchemy après connexion réussie
    import LIVRE.crud_livre as crud_livre
    import ETUDIANT.crud_etudiant as crud_etudiant
    import EMPRUNT.emprunt as crud_emprunt
    
    # Créer les engines avec les credentials
    livre_engine = crud_livre.get_engine(user, password)
    etudiant_engine = crud_etudiant.get_engine(user, password)
    emprunt_engine = crud_emprunt.get_engine(user, password)
    
    # Créer les sessions
    crud_livre.Session = sessionmaker(bind=livre_engine)
    crud_livre.session = crud_livre.Session()
    
    crud_etudiant.Session = sessionmaker(bind=etudiant_engine)
    crud_etudiant.session = crud_etudiant.Session()
    
    crud_emprunt.Session = sessionmaker(bind=emprunt_engine)
    crud_emprunt.session = crud_emprunt.Session()
    
    print("\nSessions SQLAlchemy initialisées avec succès!")
    
    # Lancer le menu
    menu()
    
except psycopg2.OperationalError as erreur:
    print("Erreur connexion : vérifie .env/PostgreSQL")
    print(erreur)
except Exception as e:
    print(f"Erreur : {e}")
